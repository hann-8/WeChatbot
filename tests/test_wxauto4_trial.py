import json
import tempfile
import unittest
from pathlib import Path
from types import SimpleNamespace
from unittest.mock import patch

from wechatbot.wxauto4_trial import TrialBinding, observe, run_trial


def msg(i, sender='tester', content='challenge', attr='friend', kind='text'):
    return SimpleNamespace(id=i, sender=sender, content=content, attr=attr, type=kind)


class Clock:
    def __init__(self): self.t = 0
    def now(self): return self.t
    def sleep(self, seconds): self.t += seconds


class Fake:
    def __init__(self, snapshots, chats=None, failure=None):
        self.snapshots = iter(snapshots); self.last = []
        self.chats = iter(chats or []); self.chat = ('room', 'group')
        self.calls = []; self.failure = failure
    def ChatInfo(self):
        self.chat = next(self.chats, self.chat)
        return dict(chat_name=self.chat[0], chat_type=self.chat[1])
    def GetAllMessage(self):
        self.last = next(self.snapshots, self.last); return self.last
    def SendMsg(self, **kwargs):
        self.calls.append(kwargs)
        if self.failure: raise self.failure
        return object()


class TrialTests(unittest.TestCase):
    def setUp(self):
        self.temp = tempfile.TemporaryDirectory(); self.addCleanup(self.temp.cleanup)
        self.root = Path(self.temp.name); self.clock = Clock()
        self.binding = TrialBinding('test1', 'alias', 'room', 'group', 'tester', ['blocked'], 'challenge', 'reply', True)
    def run_fake(self, fake, binding=None, **kwargs):
        return run_trial(binding or self.binding, lambda: fake, self.root, self.clock.now, self.clock.sleep, **kwargs)
    def test_baseline_and_new_once_unknown_blocks_other_trial(self):
        old = msg('old'); new = msg('new')
        f = Fake([[old], [old], [old, new]])
        result = self.run_fake(f)
        self.assertTrue(result['new_test_received']); self.assertTrue(result['outcome_unknown'])
        self.assertEqual(f.calls, [{'msg': 'reply'}])
        record = json.loads((self.root / 'test1.json').read_text())
        self.assertEqual((record['state'], record['send_count']), ('unknown', 1))
        second = Fake([[old], [old, new]])
        b = TrialBinding('test2', 'alias', 'room', 'group', 'tester', [], 'challenge', 'reply', True)
        self.assertEqual(self.run_fake(second, b)['reason'], 'pending_or_used')
        self.assertEqual(second.calls, [])
        observe(self.root, 'test1')
        self.assertEqual(json.loads((self.root / 'test1.json').read_text())['ack'], 'operator_observed')
    def test_rejected_sources_and_candidate_limit(self):
        old = msg('old'); rejected = [msg('a', attr='self'), msg('b', attr='system'), msg('c', kind='image'), msg('d', sender='blocked'), msg('e', sender='other')]
        f = Fake([[old], [old] + rejected])
        result = self.run_fake(f, limit=4)
        self.assertEqual(result['reason'], 'candidate_limit'); self.assertEqual(f.calls, [])
    def test_wrong_window_at_baseline_and_before_send(self):
        for chats in [[('wrong', 'group')], [('room','group')]*4 + [('wrong','group')]]:
            with self.subTest(chats=chats), tempfile.TemporaryDirectory() as d:
                f = Fake([[msg('old')], [msg('old'), msg('new')]], chats)
                result = run_trial(self.binding, lambda: f, d, self.clock.now, self.clock.sleep)
                self.assertEqual(result['reason'], 'chat_mismatch'); self.assertEqual(f.calls, [])
    def test_rebuilt_ids_and_timeout(self):
        for snapshots, expected in [([[msg('old')], [msg('new')]], 'ambiguous_ids'), ([[msg('old')]], 'timeout')]:
            with self.subTest(expected=expected), tempfile.TemporaryDirectory() as d:
                f = Fake(snapshots); c = Clock()
                self.assertEqual(run_trial(self.binding, lambda: f, d, c.now, c.sleep, timeout=4)['reason'], expected)
                self.assertEqual(f.calls, [])
    def test_exception_and_cancel_after_submission_do_not_retry(self):
        for exc in (RuntimeError(), KeyboardInterrupt()):
            with self.subTest(exc=type(exc)), tempfile.TemporaryDirectory() as d:
                f = Fake([[msg('old')], [msg('old'), msg('new')]], failure=exc); c = Clock()
                result = run_trial(self.binding, lambda: f, d, c.now, c.sleep)
                self.assertTrue(result['outcome_unknown']); self.assertEqual(len(f.calls), 1)
                self.assertEqual(run_trial(self.binding, lambda: self.fail('factory called'), d, c.now, c.sleep)['reason'], 'pending_or_used')
    def test_send_count_is_persisted_before_side_effect(self):
        f = Fake([[msg('old')], [msg('old'), msg('new')]])
        def send(**kwargs):
            record = json.loads((self.root / 'test1.json').read_text())
            self.assertEqual((record['state'], record['send_count']), ('submitted', 1))
            f.calls.append(kwargs)
        f.SendMsg = send
        self.run_fake(f); self.assertEqual(len(f.calls), 1)
    def test_local_success_does_not_clear_pending(self):
        f = Fake([[msg('old')], [msg('old'), msg('new')]])
        f.SendMsg = lambda **kwargs: {'status': '成功'}
        result = self.run_fake(f)
        self.assertTrue(result['framework_reported_success'])
        self.assertTrue(result['outcome_unknown'])
        self.assertEqual(json.loads((self.root / 'test1.json').read_text())['ack'], 'local_reported')
    def test_multiple_matching_messages_are_ambiguous(self):
        f = Fake([[msg('old')], [msg('old'), msg('a'), msg('b')]])
        self.assertEqual(self.run_fake(f)['reason'], 'ambiguous_messages')
        self.assertEqual(f.calls, [])
    def test_burst_over_limit_and_slow_read_do_not_send(self):
        for slow in (False, True):
            with self.subTest(slow=slow), tempfile.TemporaryDirectory() as d:
                c = Clock(); f = Fake([[msg('old')], [msg('old'), msg('new'), msg('extra', sender='other')]])
                original = f.GetAllMessage
                def read():
                    result = original()
                    if slow and f.last and len(f.last) > 1: c.t += 120
                    return result
                f.GetAllMessage = read
                result = run_trial(self.binding, lambda: f, d, c.now, c.sleep, limit=1 if not slow else 10)
                self.assertEqual(result['reason'], 'timeout' if slow else 'candidate_limit')
                self.assertEqual(f.calls, [])
    def test_output_and_ledger_hide_inputs(self):
        f = Fake([[msg('old')], [msg('old'), msg('new')]])
        out = self.run_fake(f)
        serialized = json.dumps(out) + (self.root / 'test1.json').read_text()
        for secret in ('room', 'tester', 'challenge', 'reply', 'alias'):
            self.assertNotIn(secret, serialized)

if __name__ == '__main__': unittest.main()
