import asyncio
from dataclasses import asdict, replace
import json
from pathlib import Path
import shutil
import socket
import tempfile
import unittest
from unittest.mock import patch
import yaml

from wechatbot.config import ROOT, Config, load_config, local_path
from wechatbot.contracts import NormalizedEvent, decode_batch
from wechatbot.delivery import deliver
from wechatbot.model_facade import ModelFacade
from wechatbot.offline_backend import OfflineSpawn
from wechatbot.router import Router
from wechatbot.status import inspect, make_health_server
from wechatbot.store import Store
from wechatbot.transports.mock import MockAdapter, SendResult
from qqbot_gateway.errors import GatewayError
from qqbot_gateway.workbuddy_cli_runner import ResultParser


def wire_dialog(process):
    # low effort now uses a control handshake then exactly one stream-json user frame.
    frames = [json.loads(line) for line in process.stdin.data.splitlines()]
    users = [frame for frame in frames if isinstance(frame, dict) and frame.get('type') == 'user']
    if users:
        assert len(users) == 1
        return json.loads(users[0]['message']['content'])
    return json.loads(process.stdin.data)


class CoreTests(unittest.IsolatedAsyncioTestCase):
    @classmethod
    def setUpClass(cls):
        cls.temp = tempfile.TemporaryDirectory(prefix='wx01-synthetic-')
        cls.root = Path(cls.temp.name)
        shutil.copytree(ROOT / 'config', cls.root / 'config', ignore=shutil.ignore_patterns('local'))
        shutil.copytree(ROOT / 'runtime/cli', cls.root / 'runtime/cli')

    @classmethod
    def tearDownClass(cls):
        cls.temp.cleanup()

    async def asyncSetUp(self):
        # Each test has a fresh synthetic ledger; never delete the project ledger.
        state = self.root / 'state'
        assert state.resolve().is_relative_to(self.root.resolve())
        if state.exists():
            shutil.rmtree(state)
        d = load_config(self.root).data
        d['bot']['allowed_groups'] = ['synthetic-group', 'other-group']
        d['bot']['blocked_users'] = ['blocked-user']
        self.config = Config(self.root, d)
        self.adapter = MockAdapter()
        self.spawn = OfflineSpawn('**合成回复**')
        self.model = ModelFacade(self.config, offline_spawn=self.spawn)
        self.store = Store(self.root)
        self.router = Router(self.config, self.adapter, self.store, self.model)
        self.seq = 0

    async def asyncTearDown(self):
        await self.model.close()
        self.store.close()

    def event(self, **changes):
        self.seq += 1
        cap = self.adapter.capabilities
        e = NormalizedEvent(1, 'wechat', cap.transport, cap.account, 'group',
                            'synthetic-group', 'synthetic-user', f'message-{self.seq}',
                            'server_stable', self.seq, float(self.seq), cap.epoch,
                            False, '自造文本', cap.digest, True, display_name='同名')
        return replace(e, **changes)

    async def handle(self, event=None):
        event = event or self.event()
        self.adapter.current_target = event.target
        return await self.router.handle(event)

    def assert_no_effects(self):
        self.assertEqual(self.spawn.calls, [])
        self.assertEqual(self.adapter.calls, [])
        self.assertEqual(self.router.windows, {})
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_full_pinned_runner_budget_ack_history(self):
        e = self.event()
        self.assertEqual(await self.handle(e), 'accepted')
        self.assertEqual(self.model.runner.attempts, 1)
        self.assertEqual(self.model.runner.user_messages_sent, 1)
        self.assertEqual(len(self.spawn.calls), 1)
        self.assertEqual(self.adapter.calls[0][0], e.target)
        self.assertEqual(self.adapter.calls[0][1], '合成回复')
        self.assertEqual(self.store.history(e), [dict(role='user', content=e.text), dict(role='assistant', content='合成回复')])
        self.assertEqual(self.store.record(self.router.last_trace), dict(state='accepted', phase='delivery', ack='api_accepted'))
        self.assertFalse(self.model.status()['blocked'])
        args, kw = self.spawn.calls[0]
        for option, value in [('--tools', ''), ('--permission-mode', 'dontAsk'),
                              ('--setting-sources', 'none'), ('--no-session-persistence', None)]:
            self.assertIn(option, args)
            if value is not None:
                self.assertEqual(args[args.index(option) + 1], value)
        self.assertIn('--strict-mcp-config', args)
        self.assertEqual(Path(args[0]), self.root / 'runtime/cli/node.exe')
        self.assertTrue(Path(kw['cwd']).is_relative_to(self.root / 'runtime/requests'))
        self.assertEqual(kw['env']['CODEBUDDY_MEMORY_ENABLED'], 'false')
        self.assertFalse(any((self.root / 'runtime/requests').iterdir()))
        self.assertTrue((self.root / 'state/cli-cleanup').exists())

    async def test_authorization_before_every_sink(self):
        for event, reason in [(self.event(conversation_id='unbound'), 'unauthorized_group'),
                              (self.event(sender_id='blocked-user'), 'blocked_sender'),
                              (self.event(conversation_kind='direct'), 'direct_disabled_or_unbound'),
                              (self.event(account_id='wrong-account'), 'transport_or_account'),
                              (self.event(sender_is_self=True), 'self_loop')]:
            event = replace(event, first_image_handle='synthetic-image')
            self.assertEqual(await self.handle(event), reason)
            self.assert_no_effects()
        self.assertEqual(self.store.counts()['seen'], 0)

    async def test_mentions_display_names_and_rename(self):
        self.assertEqual(await self.handle(self.event(text='@助手 你好', mention_self=None)), 'mention_unverified_or_absent')
        self.assertEqual(await self.handle(self.event(text='@助手 你好', mention_self=False)), 'mention_unverified_or_absent')
        self.assert_no_effects()
        self.assertEqual(await self.handle(self.event(sender_id='blocked-user', display_name='改名')), 'blocked_sender')
        self.assertEqual(await self.handle(self.event(display_name='改名')), 'accepted')

    async def test_untrusted_capability_claim_cannot_enable(self):
        self.assertEqual(await self.handle(self.event(capabilities_digest='passed')), 'transport_or_account')
        self.adapter.capabilities = replace(self.adapter.capabilities, stable_identity=False)
        self.assertEqual(await self.handle(), 'identity_unverified')
        self.assert_no_effects()

    async def test_stable_dedup_same_text_new_id_and_restart(self):
        e = self.event()
        self.assertEqual(await self.handle(e), 'accepted')
        self.assertEqual(await self.handle(self.event(source_message_id=e.source_message_id)), 'duplicate')
        self.assertEqual(await self.handle(), 'accepted')
        self.assertEqual(len(self.spawn.calls), 2)
        self.store.close()
        self.store = Store(self.root)
        self.router = Router(self.config, self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(self.event(source_message_id=e.source_message_id)), 'duplicate')
        self.assertEqual(len(self.spawn.calls), 2)

    async def test_direct_requires_both_bindings_and_isolated_history(self):
        d = self.config.data
        d['chat']['direct'].update(enabled=True, allowed_users=['synthetic-user'], allowed_conversations=['synthetic-direct'])
        self.config = Config(self.root, d)
        self.router = Router(self.config, self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(self.event(conversation_kind='direct')), 'direct_disabled_or_unbound')
        self.assertEqual(await self.handle(self.event(conversation_kind='direct', conversation_id='synthetic-direct', sender_id='blocked-user')), 'blocked_sender')
        direct = self.event(conversation_kind='direct', conversation_id='synthetic-direct', mention_self=None)
        self.assertEqual(await self.handle(direct), 'accepted')
        group = self.event()
        self.assertEqual(self.store.history(group), [])
        self.assertEqual(await self.handle(group), 'accepted')
        self.assertEqual(self.store.history(replace(group, sender_id='another-user')), [])
        self.assertEqual(len(self.store.history(direct)), 2)

    async def test_bounded_history_and_actual_wire_contains_only_scope(self):
        self.store.turns = 2
        for _ in range(3):
            self.assertEqual(await self.handle(), 'accepted')
        e = self.event(sender_id='other-user', text='另一位自造用户')
        self.assertEqual(await self.handle(e), 'accepted')
        payload = wire_dialog(self.spawn.processes[-1])
        self.assertEqual(payload, [dict(role='user', content=e.text)])
        self.assertEqual(len(self.store.history(self.event())), 4)

    async def test_old_epoch_sequence_and_wrong_transport(self):
        self.assertEqual(await self.handle(self.event(adapter_epoch='old')), 'stale_epoch')
        self.assertEqual(await self.handle(self.event(transport='pyweixin')), 'transport_or_account')
        e = self.event()
        self.assertEqual(await self.handle(e), 'accepted')
        self.assertEqual(await self.handle(replace(e, source_message_id='new-id')), 'stale_sequence')

    async def test_silence_precedes_mention_reconnect_retains_then_true_at_resumes(self):
        self.assertEqual(await self.handle(self.event(text='请先不要说话')), 'silenced')
        self.assert_no_effects()
        self.adapter.capabilities = replace(self.adapter.capabilities, epoch='reconnected')
        self.assertEqual(await self.handle(self.event(mention_self=None)), 'mention_unverified_or_absent')
        self.assertTrue(self.router.gate.muted)
        self.assertEqual(await self.handle(self.event(text='恢复交流')), 'accepted')
        self.assertFalse(self.router.gate.muted)

    async def test_silence_during_model_invalidates_output(self):
        original = self.model.generate
        started, resume = asyncio.Event(), asyncio.Event()
        async def slow(*args):
            started.set()
            await resume.wait()
            return await original(*args)
        self.model.generate = slow
        e = self.event()
        task = asyncio.create_task(self.handle(e))
        await started.wait()
        self.assertEqual(await self.handle(self.event(text='不要说话')), 'silenced')
        resume.set()
        self.assertEqual(await task, 'cancelled_target')
        self.assertEqual(self.adapter.calls, [])
        self.assertEqual(self.store.history(e), [])

    async def test_switch_account_epoch_or_target_withholds(self):
        original = self.model.generate
        async def changed(*args):
            result = await original(*args)
            self.adapter.current_target = ('synthetic-account', 'group', 'other-group')
            return result
        self.model.generate = changed
        self.assertEqual(await self.handle(), 'cancelled_target')
        self.assertEqual(self.adapter.calls, [])
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_unknown_send_blocks_new_events_without_retry(self):
        self.adapter.next_state = 'unknown'
        e = self.event()
        self.assertEqual(await self.handle(e), 'unknown')
        self.assertEqual(await self.handle(), 'target_blocked')
        self.assertEqual(len(self.spawn.calls), 1)
        self.assertEqual(len(self.adapter.calls), 1)
        self.assertEqual(self.store.history(e), [])

    async def test_failed_send_consumes_original_but_next_event_allowed(self):
        self.adapter.next_state = 'failed'
        e = self.event()
        self.assertEqual(await self.handle(e), 'failed')
        self.assertEqual(await self.handle(self.event(source_message_id=e.source_message_id)), 'duplicate')
        self.adapter.next_state = 'accepted'
        self.assertEqual(await self.handle(), 'accepted')

    async def test_none_ack_or_wrong_trace_is_unknown(self):
        async def bad(target, text, trace, check):
            return SendResult('accepted', 'none', trace)
        self.adapter.send_text = bad
        self.assertEqual(await self.handle(), 'unknown')
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_wrong_trace_is_not_ack(self):
        async def bad(target, text, trace, check):
            return SendResult('accepted', 'api_accepted', 'other-task')
        self.adapter.send_text = bad
        self.assertEqual(await self.handle(), 'unknown')

    async def test_send_cancelled_after_submit_unknown_and_no_history(self):
        started = asyncio.Event()
        async def pending(target, text, trace, check):
            self.adapter.calls.append((target, text, trace))
            started.set()
            await asyncio.Event().wait()
        self.adapter.send_text = pending
        task = asyncio.create_task(self.handle())
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(self.store.record(self.router.last_trace)['state'], 'unknown')
        self.assertEqual(await self.handle(), 'target_blocked')
        self.assertEqual(self.store.counts()['history'], 0)
        self.assertEqual(len(self.adapter.calls), 1)

    async def test_restart_prepared_and_submitted_are_unknown_without_replay(self):
        self.store.prepare('aaaaaaaaaa', self.event().target)
        self.store.close()
        self.store = Store(self.root)
        self.assertEqual(self.store.record('aaaaaaaaaa')['state'], 'unknown')
        self.router = Router(self.config, self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(), 'target_blocked')
        self.assert_no_effects()

    async def test_partial_model_output_withheld_and_no_retry(self):
        self.spawn.partial = True
        self.assertEqual(await self.handle(), 'model_unknown')
        self.assertEqual(await self.handle(), 'target_blocked')
        self.assertEqual(len(self.spawn.calls), 1)
        self.assertEqual(self.adapter.calls, [])
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_actual_parser_rejects_tool_initialization_and_markup(self):
        self.spawn.tools = ['Read']
        self.assertEqual(await self.handle(), 'model_unknown')
        self.assertEqual(self.adapter.calls, [])
        parser = ResultParser('synthetic-model')
        parser.line(json.dumps(dict(type='system', subtype='init', tools=[], mcp_servers=[], model='synthetic-model')))
        with self.assertRaises(GatewayError):
            parser.line(json.dumps(dict(type='result', subtype='success', is_error=False, result='<tool_call>Read</tool_call>')))

    async def test_input_budget_rejects_before_spawn_and_no_media_redeemed(self):
        self.model.budget = replace(self.model.budget, limit=2050)
        self.assertEqual(await self.handle(self.event(first_image_handle='image-once', text='文' * 2000)), 'model_failed')
        self.assertEqual(self.spawn.calls, [])
        self.assertEqual(self.adapter.calls, [])
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_queue_bound_and_waiter_cancel_has_no_generation(self):
        d = self.config.data
        d['models']['llm']['queue_limit'] = 1
        self.router = Router(Config(self.root, d), self.adapter, self.store, self.model)
        entered, release = asyncio.Event(), asyncio.Event()
        original = self.model.generate
        async def slow(*args):
            entered.set()
            await release.wait()
            return await original(*args)
        self.model.generate = slow
        first = asyncio.create_task(self.handle())
        await entered.wait()
        second = asyncio.create_task(self.handle())
        await asyncio.sleep(0)
        self.assertEqual(await self.handle(), 'queue_full')
        second.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await second
        self.assertEqual(self.router.waiting, 0)
        release.set()
        self.assertEqual(await first, 'accepted')
        self.assertEqual(len(self.spawn.calls), 1)

    async def test_model_cancelled_once_is_unknown(self):
        started = asyncio.Event()
        async def slow(*args):
            started.set()
            await asyncio.Event().wait()
        self.model.generate = slow
        task = asyncio.create_task(self.handle())
        await started.wait()
        task.cancel()
        with self.assertRaises(asyncio.CancelledError):
            await task
        self.assertEqual(self.store.record(self.router.last_trace)['state'], 'unknown')
        self.assertEqual(await self.handle(), 'target_blocked')

    async def test_cleanup_unknown_blocks_all_model_targets(self):
        owner = self.model.runner.cleanup_owner()
        owner.reserve('bbbbbbbbbb')
        self.assertEqual(await self.handle(), 'target_or_model_blocked')
        self.assert_no_effects()

    async def test_second_owner_refused(self):
        with self.assertRaises(ValueError):
            Store(self.root)

    async def test_real_model_requires_explicit_offline_replacement(self):
        with self.assertRaisesRegex(ValueError, 'real_model_closed'):
            ModelFacade(self.config)

    async def test_default_empty_authorization_and_real_flags_cannot_enable(self):
        d = load_config(self.root).data
        d['bot']['enabled'] = True
        d['runtime']['sends_enabled'] = True
        self.router = Router(Config(self.root, d), self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(), 'unauthorized_group')
        self.assertFalse(self.adapter.capabilities.production_eligible)
        self.assert_no_effects()

    async def test_real_transport_remains_closed_with_flags_and_claimed_capabilities(self):
        d = self.config.data
        d['bot'].update(enabled=True, transport='pyweixin')
        d['runtime']['sends_enabled'] = True
        self.adapter.capabilities = replace(self.adapter.capabilities, transport='pyweixin')
        self.router = Router(Config(self.root, d), self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(), 'real_channel_closed')
        self.assert_no_effects()

    async def test_account_or_epoch_change_after_model_cancels(self):
        original = self.model.generate
        async def changed(*args):
            result = await original(*args)
            self.adapter.capabilities = replace(self.adapter.capabilities, account='another-account', epoch='new-epoch')
            return result
        self.model.generate = changed
        self.assertEqual(await self.handle(), 'cancelled_target')
        self.assertEqual(self.adapter.calls, [])

    async def test_ack_target_switch_or_submit_exception_stays_unknown(self):
        async def bad(target, text, trace, check):
            self.adapter.current_target = ('synthetic-account', 'group', 'other-group')
            return SendResult('accepted', 'api_accepted', trace)
        self.adapter.send_text = bad
        self.assertEqual(await self.handle(), 'unknown')
        self.assertEqual(self.store.counts()['history'], 0)

    async def test_restart_submitted_is_unknown(self):
        e = self.event()
        self.store.prepare('cccccccccc', e.target)
        self.store.transition('cccccccccc', 'submitted', 'delivery')
        self.store.close()
        self.store = Store(self.root)
        self.router = Router(self.config, self.adapter, self.store, self.model)
        self.assertEqual(await self.handle(), 'target_blocked')
        self.assertEqual(self.store.record('cccccccccc')['state'], 'unknown')
        self.assert_no_effects()

    async def test_queued_events_generate_serially_with_updated_history(self):
        self.adapter.current_target = self.event().target
        results = await asyncio.gather(*(self.router.handle(self.event()) for _ in range(3)))
        self.assertEqual(results, ['accepted'] * 3)
        self.assertEqual([len(wire_dialog(p)) for p in self.spawn.processes], [1, 3, 5])
        self.assertEqual(self.router.waiting, 0)

    async def test_no_image_context_can_cross_into_text_runner(self):
        from qqbot_gateway.vision import CURRENT
        token = CURRENT.set(object())
        try:
            self.assertEqual(await self.handle(self.event(first_image_handle='not-redeemed')), 'accepted')
            payload = wire_dialog(self.spawn.processes[0])
            self.assertIsInstance(payload[-1]['content'], str)
        finally:
            CURRENT.reset(token)

    async def test_ollama_runner_uses_only_explicit_fake_transport(self):
        d = self.config.data
        d['models']['llm']['backend'] = 'ollama_ssh'
        calls = []
        model_name = d['models']['llm']['profiles']['ollama_ssh']['model']
        class Transport:
            def __init__(self, root, access_file):
                self.root = root  # Do not open access_file or construct SSHTransport.
            def request(self, method, path, payload=None, *, deadline, before_send=None):
                calls.append((method, path, payload))
                if path == '/api/tags':
                    return {'models': [{'name': model_name, 'digest': None}]}
                if before_send:
                    before_send()
                return dict(done=True, model=model_name, done_reason='stop', message={'role': 'assistant', 'content': '家庭路线合成回复'})
            def close(self):
                pass
        other = ModelFacade(Config(self.root, d), offline_transport_factory=Transport)
        self.router = Router(Config(self.root, d), self.adapter, self.store, other)
        with patch('socket.create_connection', side_effect=AssertionError('no SSH')):
            self.assertEqual(await self.handle(), 'accepted')
        self.assertEqual(other.runner.post_attempts, 1)
        payload = calls[-1][2]
        self.assertFalse(payload['think'])
        self.assertEqual(payload['options']['num_ctx'], 16384)
        self.assertEqual(payload['options']['num_predict'], 1024)
        self.assertFalse((self.root / 'secrets').exists())
        self.assertFalse(other.runner.marker.exists())

    async def test_readonly_status_does_not_expose_private_fields(self):
        text = json.dumps(self.router.status())
        for private in ('synthetic-account', 'synthetic-group', 'synthetic-user', '自造文本', str(self.root)):
            self.assertNotIn(private, text)


class ContractConfigTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(prefix='wx01-config-')
        self.root = Path(self.temp.name)
        shutil.copytree(ROOT / 'config/examples', self.root / 'config/examples')

    def tearDown(self):
        self.temp.cleanup()

    def mutate(self, name, transform):
        file = self.root / f'config/examples/{name}.yaml'
        d = yaml.safe_load(file.read_text(encoding='utf-8'))
        transform(d)
        file.write_text(yaml.safe_dump(d), encoding='utf-8')

    def test_default_inspect_zero_side_effects_and_independent_root(self):
        with patch('asyncio.create_subprocess_exec', side_effect=AssertionError('no processes')), patch('socket.socket', side_effect=AssertionError('no network')):
            cfg = load_config(self.root)
            result = inspect(cfg)
        self.assertFalse(result['enabled'])
        self.assertFalse(result['sends_enabled'])
        self.assertFalse(result['production_eligible'])
        self.assertFalse((self.root / 'state').exists())
        self.assertFalse((self.root / 'secrets').exists())
        d = cfg.data
        d['bot']['enabled'] = True
        self.assertFalse(cfg.data['bot']['enabled'])

    def test_unknown_duplicate_wrong_types_and_yaml_alias_rejected(self):
        file = self.root / 'config/examples/bot.yaml'
        original = file.read_text(encoding='utf-8')
        for extra in ('\nunknown: true\n', '\nenabled: true\n', '\nallowed_groups: &x [a]\nblocked_users: *x\n'):
            file.write_text(original + extra, encoding='utf-8')
            with self.assertRaises(ValueError):
                load_config(self.root)
        file.write_text(original.replace('enabled: false', 'enabled: 0'), encoding='utf-8')
        with self.assertRaises(ValueError):
            load_config(self.root)

    def test_malformed_yaml_and_native_sampling_rejected(self):
        file = self.root / 'config/examples/bot.yaml'
        original = file.read_bytes()
        file.write_text('platform: [unterminated', encoding='utf-8')
        with self.assertRaisesRegex(ValueError, 'config_syntax'):
            load_config(self.root)
        file.write_bytes(original)
        self.mutate('models', lambda d: d['llm']['profiles']['ollama_ssh'].update(temperature=-1.0))
        with self.assertRaisesRegex(ValueError, 'native_sampling'):
            load_config(self.root)

    def test_free_media_and_native_window_cannot_be_enabled(self):
        for name, field, value in [('chat', 'participation', {'mode': 'free'}),
                                    ('features', 'vision', {'enabled': True})]:
            original = (self.root / f'config/examples/{name}.yaml').read_bytes()
            self.mutate(name, lambda d: d.update({field: value}))
            with self.assertRaises(ValueError):
                load_config(self.root)
            (self.root / f'config/examples/{name}.yaml').write_bytes(original)
        self.mutate('models', lambda d: d['llm']['profiles']['codebuddy_cli'].update(context_window_tokens=10000))
        with self.assertRaises(ValueError):
            load_config(self.root)

    def test_path_escape_and_wrong_qq_port_refused(self):
        with self.assertRaises(ValueError):
            local_path(self.root, '../QQbot/secrets')
        with self.assertRaises(ValueError):
            load_config(self.root, directory=str(ROOT / 'config/examples'))
        self.mutate('runtime', lambda d: d.update(health_port=8765))
        with self.assertRaises(ValueError):
            load_config(self.root)

    def test_port_conflict_does_not_fallback(self):
        with socket.socket() as held:
            held.bind(('127.0.0.1', 0))
            held.listen()
            port = held.getsockname()[1]
            self.mutate('runtime', lambda d: d.update(health_port=port))
            with self.assertRaises(OSError):
                make_health_server(load_config(self.root))

    def test_strict_events_unknown_duplicate_limits_control_and_nan(self):
        row = dict(version=1, platform='wechat', transport='mock', account_id='account',
                   conversation_kind='group', conversation_id='group', sender_id='sender',
                   source_message_id='message', id_scope='server_stable', received_seq=1,
                   received_monotonic=1, adapter_epoch='epoch', sender_is_self=False,
                   text='synthetic', capabilities_digest='digest')
        self.assertIsNone(decode_batch(json.dumps([row]).encode())[0].mention_self)
        for changed in [dict(row, unknown=True), dict(row, sender_id='../QQ'),
                        dict(row, received_seq=True), dict(row, mention_self='true'),
                        dict(row, text='a\x00b'), dict(row, text='x' * 4001),
                        dict(row, received_monotonic=float('nan'))]:
            with self.assertRaises(ValueError):
                decode_batch(json.dumps([changed]).encode())
        for raw in [b'[{"text":"a","text":"b"}]', b'[]', b' ' * 65537, json.dumps([row] * 33).encode()]:
            with self.assertRaises(ValueError):
                decode_batch(raw)


if __name__ == '__main__':
    unittest.main()
