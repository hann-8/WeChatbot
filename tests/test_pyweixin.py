import asyncio
import importlib.util
import json
from dataclasses import replace
from pathlib import Path
import subprocess
import sys
import tempfile
import unittest
from types import SimpleNamespace
from unittest.mock import patch

from wechatbot.config import ROOT, Config, load_config
from wechatbot.contracts import NormalizedEvent
from wechatbot.gate import Gate
from wechatbot.pyweixin_probe import (
    ProbeSession, ObservationLimits, capability_report, mock_probe, inspect_candidate,
)
from wechatbot.transports.pyweixin_adapter import (
    BoundWindowPrimitives, MockPrimitives, PyweixinAdapter, Snapshot,
    VisibleItem, WindowBinding, image_capability, keypress_result,
    open_real_observation,
)


def binding():
    return WindowBinding('synthetic-account', 12, 123.0, 24, (1,), (2,), 'epoch-1')


def snapshot(*ids, bind=None):
    return Snapshot(bind or binding(), tuple(VisibleItem((n,)) for n in ids))


class FakeWindow:
    """Raises on any operation outside the reviewed read-only surface."""
    def __init__(self):
        self.handle = 24
        self.element_info = SimpleNamespace(runtime_id=(1,))
        self.list = SimpleNamespace(element_info=SimpleNamespace(runtime_id=(2,)))
        self.list.children = self.children
        self.list.wrapper_object = lambda: self.list
        self.queries = []
        self.reads = 0
        self.ids = (10,)
        self.on_children = lambda: None

    def wrapper_object(self):
        return self

    def process_id(self):
        return 12

    def child_window(self, **kwargs):
        self.queries.append(kwargs)
        return self.list

    def children(self, **kwargs):
        self.reads += 1
        self.queries.append(kwargs)
        self.on_children()
        return [SimpleNamespace(element_info=SimpleNamespace(runtime_id=(n,)),
                                class_name=lambda: 'mmui::ChatBubbleItemView') for n in self.ids]

    def __getattr__(self, _):
        raise AssertionError('non_readonly_operation')


class ProbeTests(unittest.TestCase):
    def session(self, *frames, limits=None, clock=None):
        primitive = MockPrimitives(frames)
        kwargs = {} if clock is None else {'clock': clock}
        return ProbeSession(primitive, binding(), limits=limits, **kwargs), primitive

    def test_baseline_is_discarded_and_same_snapshot_not_replayed(self):
        s, _ = self.session(snapshot(1, 2), snapshot(1, 2), snapshot(1, 2, 3), snapshot(1, 2, 3))
        self.assertEqual(s.poll()['state'], 'baseline_discarded')
        self.assertEqual([s.poll()['new_runtime_samples'] for _ in range(3)], [0, 1, 0])

    def test_burst_counts_separate_runtime_items_without_text_hash(self):
        s, _ = self.session(snapshot(), snapshot(*range(10)), snapshot(*range(11)))
        s.poll()
        self.assertEqual(s.poll()['new_runtime_samples'], 10)
        self.assertTrue(s.closed)
        self.assertEqual(s.poll()['state'], 'closed')

    def test_burst_exceeding_remaining_budget_fails_whole_batch(self):
        s, _ = self.session(snapshot(), snapshot(*range(11)))
        s.poll()
        self.assertEqual(s.poll()['state'], 'sample_budget_exceeded')
        self.assertEqual(s.count, 0)

    def test_budget_is_cumulative_not_per_poll(self):
        s, _ = self.session(snapshot(), snapshot(*range(6)), snapshot(*range(11)))
        s.poll(); s.poll()
        self.assertEqual(s.poll()['state'], 'sample_budget_exceeded')
        self.assertEqual(s.count, 6)

    def test_virtualized_removal_is_not_new_message(self):
        for next_frame in (snapshot(2, 3), snapshot(40, 41), snapshot()):
            s, _ = self.session(snapshot(1, 2), next_frame)
            s.poll()
            self.assertEqual(s.poll()['state'], 'virtual_list_or_reconstruction_unverified')
            self.assertEqual(s.count, 0)

    def test_reconnect_invalidates_old_runtime_ids(self):
        s, _ = self.session(snapshot(1), snapshot(1, 2, bind=replace(binding(), epoch='epoch-2')))
        s.poll()
        self.assertEqual(s.poll()['state'], 'window_changed')

    def test_each_window_binding_component_is_checked(self):
        for change in ({'account_reference': 'other'}, {'pid': 13}, {'hwnd': 25},
                       {'process_started': 124.0}, {'root_runtime_id': (3,)},
                       {'list_runtime_id': (4,)}):
            s, _ = self.session(snapshot(1), snapshot(1, 2, bind=replace(binding(), **change)))
            s.poll()
            self.assertEqual(s.poll()['state'], 'window_changed')

    def test_runtime_duplicates_are_ambiguous(self):
        s, _ = self.session(snapshot(1, 1))
        self.assertEqual(s.poll()['state'], 'ambiguous_runtime_ids')

    def test_no_tree_and_source_exceptions_are_closed(self):
        s, _ = self.session()
        self.assertEqual(s.poll()['state'], 'ui_unavailable')

    def test_oversized_and_invalid_snapshots_are_closed(self):
        for frame in (snapshot(*range(33)), None, Snapshot(binding(), (), True),
                      Snapshot(binding(), [VisibleItem((1,))])):
            s, _ = self.session(frame)
            self.assertEqual(s.poll()['state'], 'invalid_or_overflow' if frame is not None else 'window_changed')

    def test_deadline_prevents_another_read(self):
        now = [0.0]
        s, p = self.session(snapshot(), clock=lambda: now[0])
        now[0] = 120
        self.assertEqual(s.poll()['state'], 'deadline')
        self.assertEqual(p.calls, 0)

    def test_slow_read_result_is_discarded(self):
        ticks = iter([0, 0, 121])
        s, p = self.session(snapshot(), clock=lambda: next(ticks))
        self.assertEqual(s.poll()['state'], 'deadline')
        self.assertEqual(p.calls, 1)

    def test_limits_are_strict(self):
        for kwargs in ({'seconds': 121}, {'seconds': float('nan')}, {'seconds': True},
                       {'samples': 11}, {'samples': 0}, {'samples': True}):
            with self.assertRaises(ValueError):
                ObservationLimits(**kwargs)

    def test_live_provider_cannot_enter_offline_session(self):
        with self.assertRaisesRegex(ValueError, 'real_observation_closed'):
            ProbeSession(object(), binding())

    def test_real_entry_never_imports_any_ui_package(self):
        with patch('builtins.__import__', side_effect=AssertionError('unexpected_import')):
            with self.assertRaisesRegex(ValueError, 'observation_not_authorized'):
                open_real_observation()
        with self.assertRaisesRegex(ValueError, 'real_observation_closed'):
            open_real_observation(mode='observe', authorized=True, binding=binding(), synthetic_samples=True)

    def test_explicit_mode_binding_and_sample_declaration_required(self):
        for kwargs in ({'authorized': True}, {'mode': 'observe'},
                       {'mode': 'observe', 'authorized': True},
                       {'mode': 'observe', 'authorized': True, 'synthetic_samples': True}):
            with self.assertRaises(ValueError):
                open_real_observation(**kwargs)

    def test_primitives_only_read_bound_list_runtime_metadata(self):
        root = FakeWindow()
        p = BoundWindowPrimitives(root, binding(), process_identity=lambda _: 123., foreground=lambda: 24)
        result = p.snapshot()
        self.assertEqual(result, snapshot(10))
        self.assertEqual(root.queries, [{'title': '消息', 'control_type': 'List'},
                                      {'control_type': 'CheckBox'},
                                      {'title': '消息', 'control_type': 'List'}])
        self.assertEqual(root.reads, 1)

    def test_primitives_wrong_focus_does_not_read_items(self):
        root = FakeWindow()
        p = BoundWindowPrimitives(root, binding(), process_identity=lambda _: 123., foreground=lambda: 99)
        with self.assertRaisesRegex(ValueError, 'window_changed'):
            p.snapshot()
        self.assertEqual(root.reads, 0)

    def test_process_reuse_does_not_read_items(self):
        root = FakeWindow()
        p = BoundWindowPrimitives(root, binding(), process_identity=lambda _: 999., foreground=lambda: 24)
        with self.assertRaisesRegex(ValueError, 'window_changed'):
            p.snapshot()
        self.assertEqual(root.reads, 0)

    def test_switch_during_read_discards_result(self):
        root = FakeWindow()
        root.on_children = lambda: setattr(root.element_info, 'runtime_id', (99,))
        p = BoundWindowPrimitives(root, binding(), process_identity=lambda _: 123., foreground=lambda: 24)
        with self.assertRaisesRegex(ValueError, 'window_changed'):
            p.snapshot()

    def test_primitive_list_reconstruction_is_rejected(self):
        root = FakeWindow()
        root.list.element_info.runtime_id = (999,)
        p = BoundWindowPrimitives(root, binding(), process_identity=lambda _: 123., foreground=lambda: 24)
        with self.assertRaisesRegex(ValueError, 'window_changed'):
            p.snapshot()
        self.assertEqual(root.reads, 0)

    def test_same_names_renames_plain_at_and_self_are_not_identities(self):
        adapter = PyweixinAdapter()
        d = load_config().data
        d['bot']['transport'] = 'pyweixin'
        config = Config(ROOT, d)
        store = SimpleNamespace(claim=lambda _: self.fail('identity must precede store'))
        gate = Gate(config, adapter, store)
        cap = adapter.capabilities
        for name, text, self_flag in [('同名', '@助手 hi', False), ('同名', 'hi', False),
                                     ('改名', 'hi', False), ('自己', '@助手 hi', True)]:
            e = NormalizedEvent(1, 'wechat', 'pyweixin', cap.account, 'group', 'declared-group',
                                'declared-sender', 'runtime-1', 'process_local', 1, 1., cap.epoch,
                                self_flag, text, cap.digest, None, display_name=name)
            self.assertEqual(gate.admit(e), (None, 'identity_unverified'))

    def test_single_image_never_gets_pixels_or_current_message_handle(self):
        # A refer bubble cannot distinguish an image from video, a quote or old media.
        frame = Snapshot(binding(), (VisibleItem((11,), 'mmui::ChatBubbleReferItemView'),))
        s, _ = self.session(snapshot(), frame)
        s.poll(); result = s.poll()
        self.assertNotIn('first_image_handle', result)
        self.assertEqual(image_capability()['pixels'], 'unsupported')
        self.assertIsNone(image_capability()['material_handle'])

    def test_keypress_and_correlated_acceptance_are_separate(self):
        self.assertEqual(keypress_result(), {'state': 'unknown', 'ack_level': 'none', 'reason': 'delivery_unverified'})
        adapter = PyweixinAdapter()
        result = asyncio.run(adapter.send_text(None, 'synthetic', 'trace', lambda: self.fail('check called')))
        self.assertEqual((result.state, result.ack_level), ('failed', 'none'))
        self.assertFalse(adapter.capabilities.production_eligible)
        self.assertEqual(adapter.capabilities.status()['identity'], 'identity_unverified')

    def test_report_is_closed_metadata_and_never_synthetic_passed(self):
        r = capability_report()
        for key in ('stable_account_id', 'stable_conversation_id', 'stable_sender_id', 'stable_message_id'):
            self.assertEqual(r[key], 'unverified')
        self.assertFalse(r['real_observed'])
        self.assertNotIn('passed', json.dumps(r))
        self.assertEqual(mock_probe()['evidence'], 'offline_synthetic')

    def test_default_cli_and_imports_cannot_touch_ui_model_or_network(self):
        code = '''
import sys,json
class Block:
 def find_spec(self, name, *args):
  if name in {'wechatbot.model_facade','qqbot_gateway.workbuddy_cli_runner','qqbot_gateway.ollama_ssh_runner'} or name.split('.')[0] in {'pyweixin','pywechat','pywinauto','pyautogui','win32gui','win32clipboard','comtypes'}:
   raise AssertionError('forbidden import')
sys.meta_path.insert(0, Block())
import socket, subprocess
class NoSocket(socket.socket):
 def __new__(cls, *a, **k):
  raise AssertionError('network')
socket.socket=NoSocket
class NoSpawn(subprocess.Popen):
 def __init__(self, *a, **k):
  raise AssertionError('spawn')
subprocess.Popen=NoSpawn
from wechatbot.__main__ import main
sys.argv=['wechatbot',sys.argv[1]] + sys.argv[2:]
raise SystemExit(main())
'''
        for args in (['inspect'], ['probe'], ['probe', '--mode', 'mock']):
            p = subprocess.run([sys.executable, '-c', code, *args], cwd=ROOT,
                               capture_output=True, text=True)
            self.assertEqual(p.returncode, 0, p.stderr)
            self.assertNotIn('synthetic-account', p.stdout)
            self.assertFalse(json.loads(p.stdout).get('production_eligible', False))

    def test_live_cli_mode_is_not_exposed(self):
        p = subprocess.run([sys.executable, '-m', 'wechatbot', 'probe', '--mode', 'observe'],
                           cwd=ROOT, capture_output=True, text=True)
        self.assertEqual(p.returncode, 2)

    def test_audit_evidence_detects_tampering(self):
        spec = importlib.util.spec_from_file_location('source_check', ROOT / 'scripts/check_pyweixin_source.py')
        checker = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(checker)
        self.assertEqual(checker.check()['dependency_artifacts'], 4)
        import shutil
        with tempfile.TemporaryDirectory() as tmp:
            root = Path(tmp)
            shutil.copytree(ROOT / 'vendor/pyweixin', root / 'vendor/pyweixin')
            (root / 'vendor/pyweixin/upstream/LICENSE').write_text('changed', encoding='utf-8')
            with self.assertRaises(AssertionError):
                checker.check(root)
            self.assertEqual(inspect_candidate(root)['local_evidence'], 'unavailable_or_invalid')

    def test_inspect_evidence_is_local_not_real_observation(self):
        r = inspect_candidate()
        self.assertEqual(r['local_evidence'], 'hash_verified_not_runtime_observed')
        self.assertFalse(r['real_observed'])
