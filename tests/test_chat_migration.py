"""Section 10 combinations. Synthetic messages only, no real framework/model/network."""
import asyncio
from dataclasses import asdict, replace
import json
import os
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
from types import SimpleNamespace

from wechatbot.config import Config, ROOT, load_config
from wechatbot.chat_model import ChatCliModel
from wechatbot.chat_session import ChatBinding, ChatSession
from wechatbot.transports.wxauto4_adapter import Wxauto4Client
from wechatbot.model_facade import ModelFacade
from wechatbot.offline_backend import OfflineSpawn
from qqbot_gateway.backends import BackendResult
from qqbot_gateway.errors import GatewayError
from qqbot_gateway.group_memory import MemoryStore
from qqbot_gateway.token_budget import InputBudget
from qqbot_gateway.cli_web_policy import native_contract


class FakeFramework:
    def __init__(self):
        self.chat = ('synthetic-group', 'group')
        self.messages = [self.message('0', 'bot old')]
        self.sent = []
        self.response = {'status': '成功'}

    @staticmethod
    def message(identity, text, sender='tester', attr='friend'):
        return SimpleNamespace(id=identity, attr=attr, type='text', sender=sender, content=text)

    def ChatInfo(self):
        return dict(zip(('chat_name', 'chat_type'), self.chat))

    def GetAllMessage(self):
        return self.messages

    def SendMsg(self, msg):
        self.sent.append(msg)
        if isinstance(self.response, Exception):
            raise self.response
        return self.response


class FakeRunner:
    def __init__(self):
        self.calls = []
        self.updates = {}
        self.receipt = False
        self.parameters = {}
        self.wait = None

    async def run(self, system, prompt, request_id):
        self.calls.append((system, prompt, request_id))
        if self.wait:
            await self.wait.wait()
        return BackendResult(json.dumps(dict(wechat_reply=1, text='**合成回复**',
                                             memory_updates=self.updates, memory_receipt=self.receipt)),
                             parameters=self.parameters)


class MigrationTests(unittest.IsolatedAsyncioTestCase):
    async def asyncSetUp(self):
        self.tmp = tempfile.TemporaryDirectory(prefix='wx-mig-synthetic-')
        self.root = Path(self.tmp.name)
        (self.root / 'config').mkdir()
        (self.root / 'config/persona.md').write_text('角色材料' * 3000, encoding='utf-8')
        self.config = Config(self.root, load_config().data)
        self.binding = ChatBinding('synthetic-account', 'synthetic-conversation', 'synthetic-group',
                                   ['blocked'])
        self.framework = FakeFramework()
        self.runner = FakeRunner()
        self.model = ChatCliModel(self.config, runner=self.runner)
        self.notices = []
        self.session = ChatSession(self.config, self.binding, Wxauto4Client(lambda: self.framework),
                                   self.model, notify=self.notices.append)
        self.assertTrue(self.session.baseline())

    async def asyncTearDown(self):
        await self.session.close()
        self.tmp.cleanup()

    async def turn(self, identity='1', text='bot 测试', sender='tester'):
        self.framework.messages.append(self.framework.message(identity, text, sender=sender))
        self.session.poll()
        await self.session.advance()
        await asyncio.sleep(0)
        await self.session.advance()

    async def test_baseline_filter_two_turns_single_plain_send_and_local_commands(self):
        self.session.poll(); await self.session.advance()
        self.assertFalse(self.runner.calls)
        self.framework.messages.extend([self.framework.message('self', 'bot self', attr='self'),
                                       self.framework.message('blocked', 'bot blocked', sender='blocked'),
                                       self.framework.message('other', 'ordinary text', sender='other'),
                                       self.framework.message('no-prefix', 'hello')])
        await self.turn()
        await self.turn('2', 'bot 第二轮')
        self.assertEqual(len(self.runner.calls), 2)
        self.assertEqual(self.framework.sent, ['合成回复', '合成回复'])
        self.assertEqual(self.session.status()['history_turns'], 2)
        self.assertIn('测试', self.runner.calls[1][1])
        self.session.command('pause')
        await self.turn('3')
        self.assertEqual(len(self.runner.calls), 2)
        self.session.command('resume')
        self.session.command('reset')
        self.assertEqual(self.session.history, [])
        await self.turn('4', 'bot pause')  # Ordinary text never performs local control.
        self.assertFalse(self.session.paused)
        self.assertEqual(len(self.runner.calls), 3)

    async def test_all_members_trigger_and_legacy_allowlist_does_not_restrict(self):
        path = self.root / 'binding.json'
        path.write_text(json.dumps(asdict(self.binding) | {'allowed_senders': ['tester']}), encoding='utf-8')
        binding = ChatBinding.read(path)
        self.assertFalse(hasattr(binding, 'allowed_senders'))
        self.session.binding = binding
        await self.turn(sender='new-member')
        self.assertEqual(len(self.runner.calls), 1)
        self.assertEqual(self.framework.sent, ['合成回复'])
        self.assertIn('new-member', self.runner.web_private_ids)
        await self.turn('2', sender='blocked')
        await self.turn('3', text='没有前缀', sender='another-member')
        self.assertEqual(len(self.runner.calls), 1)

    async def test_unknown_no_retry_retained_on_restart_and_operator_resolves(self):
        self.framework.response = None
        await self.turn()
        self.assertTrue(self.session.paused)
        await self.turn('2')
        self.assertEqual(len(self.framework.sent), 1)
        restarted = ChatSession(self.config, self.binding, self.session.client, self.model, notify=lambda _: None)
        self.assertTrue(restarted.unresolved)
        self.assertTrue(restarted.paused)
        self.session.command('resume')
        self.assertTrue(self.session.paused)
        self.session.command('mark-not-sent')
        self.session.command('resume')
        self.assertFalse(self.session.paused)
        self.assertEqual(len(self.framework.sent), 1)
        self.assertEqual(len(list(self.session.root.glob('*.json'))), 1)

    async def test_switch_or_pause_discards_old_result_before_save_and_send(self):
        for action in ('pause', 'switch'):
            self.runner.wait = asyncio.Event()
            self.runner.updates = {'new_1': '不能保存的旧结果'}
            self.framework.messages.append(self.framework.message(action, 'bot test'))
            self.session.poll(); await self.session.advance(); await asyncio.sleep(0)
            if action == 'pause':
                self.session.command('pause')
            else:
                self.framework.chat = ('other-group', 'group')
            self.runner.wait.set(); await asyncio.sleep(0); await self.session.advance()
            self.assertEqual(self.framework.sent, [])
            self.assertEqual(self.session.memory.manage(self.binding.conversation_key, 'inspect')['records'], 0)
            self.framework.chat = ('synthetic-group', 'group')
            self.session.command('resume')

    async def test_schema2_full_memory_reset_new_store_update_delete_and_isolation(self):
        self.runner.updates = {'new_1': '自造称呼小青' + '经历' * 1000}
        self.runner.receipt = True
        await self.turn()
        self.assertIn('已保存到本群长期记忆', self.framework.sent[-1])
        self.session.command('reset')
        new = MemoryStore(self.root, self.binding.account_alias, [self.binding.conversation_key, 'another'],
                          cfg=self.config.data['features']['memory'])
        source = {}
        context = new.prepare(self.binding.conversation_key, '1'*64, source, {}, [])
        records = source['memory']['records']
        self.assertEqual(len(next(iter(records.values()))), 2006)
        record_id = next(iter(records))
        self.runner.updates = {record_id: '改为清茶'}
        await self.turn('2')
        self.assertIn('经历' * 1000, self.runner.calls[-1][1])
        self.runner.updates = {record_id: None}
        await self.turn('3')
        self.assertEqual(self.session.memory.manage(self.binding.conversation_key, 'inspect')['records'], 0)
        other = {}; new.prepare('another', '2'*64, other, {}, [])
        self.assertEqual(other['memory']['records'], {})
        new.close(context)

    async def test_failed_atomic_save_keeps_original_and_receipt(self):
        self.runner.updates = {'new_1': '原始内容'}; self.runner.receipt = True
        await self.turn()
        path = self.session.memory.path(self.binding.conversation_key)
        original = path.read_bytes()
        real_replace = os.replace
        def fail_memory_only(source, target):
            if Path(target).name == 'memory.json':
                raise OSError('synthetic failure')
            return real_replace(source, target)
        with patch('qqbot_gateway.group_memory.os.replace', side_effect=fail_memory_only):
            await self.turn('2')
        self.assertEqual(path.read_bytes(), original)
        self.assertIn('没有保存成功', self.framework.sent[-1])
        self.assertEqual(len(self.runner.calls), 2)
        self.assertFalse(self.session.paused)

    async def test_budget_keeps_current_full_memory_only_removes_whole_history(self):
        self.model.budget = InputBudget(limit=20000, overhead=2048, output=2048)
        self.model.system = '政策'
        source = dict(memory=dict(records={'a'*32: '记忆全文' * 1000}))
        history = [dict(role='user', content='旧历史'*3000), dict(role='assistant', content='旧回复'*3000)]
        await self.model.generate('当前请求', 'p_'+'a'*16, source, history, 'synthetic')
        prompt = self.runner.calls[-1][1]
        self.assertIn('记忆全文'*1000, prompt)
        self.assertIn('当前请求', prompt)
        self.assertNotIn('旧历史', prompt)
        self.assertEqual(len(json.loads(prompt)), 1)
        self.model.budget = replace(self.model.budget, limit=3000)
        with self.assertRaises(GatewayError):
            await self.model.generate('当前请求', 'p_'+'a'*16, source, [], 'synthetic2')
        self.assertEqual(len(self.runner.calls), 1)

    async def test_native_proof_and_no_tool_learning(self):
        self.runner.parameters = dict(native_web=dict(calls=1, urls=['https://example.com/source']))
        self.runner.updates = {'new_1': '网页不能学进群友记忆'}
        await self.turn()
        self.assertIn('https://example.com/source', self.framework.sent[-1])
        self.assertEqual(self.session.memory.manage(self.binding.conversation_key, 'inspect')['records'], 0)
        self.runner.parameters = dict(native_web=dict(calls=1, urls=['file:///private', 'http://127.0.0.1/']))
        await self.turn('2')
        self.assertIn('未取得可核实', self.framework.sent[-1])
        self.assertNotIn('file://', self.framework.sent[-1])
        contract = native_contract(self.config.data['features']['web'], [], self.model.budget)
        self.assertEqual(contract['allowed_tools'], ['WebSearch','WebFetch'])
        self.assertEqual((contract['max_calls'],contract['max_turns'],contract['result_bytes'],contract['total_result_bytes']),
                         (3,4,8000,12000))
        self.assertEqual(native_contract(self.config.data['features']['web'],[],self.model.budget,'不要联网')['allowed_tools'], [])

    async def test_existing_runner_relative_paths_and_spawn_seam(self):
        cfg = load_config()
        spawn = OfflineSpawn('合成回复')
        model = ModelFacade(cfg, offline_spawn=spawn)
        self.assertTrue(model.runner.node.is_absolute())
        self.assertTrue(model.runner.entry.is_absolute())
        answer = await model.generate(SimpleNamespace(text='合成问题'), [], 'synthetic-migration')
        self.assertEqual(answer, '合成回复')
        self.assertEqual(len(spawn.calls), 1)
        args = spawn.calls[0][0]
        self.assertEqual(json.loads(args[args.index('--settings')+1])['alwaysThinkingEnabled'], False)
        self.assertEqual(args[args.index('--effort')+1], 'low')
        self.assertEqual(args[args.index('--tools')+1], '')
        await model.close()


if __name__ == '__main__':
    unittest.main()
