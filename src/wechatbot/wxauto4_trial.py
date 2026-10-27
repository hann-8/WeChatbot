"""Explicit, supervised one-message trial; no production event or model path."""
import argparse
import json
import os
import re
import tempfile
import time
from contextlib import contextmanager
from dataclasses import dataclass
from pathlib import Path

from .transports.wxauto4_adapter import Wxauto4Client, inspect_dependency, live_factory


@dataclass(frozen=True)
class TrialBinding:
    trial_id: str
    account_alias: str
    chat_name: str
    chat_type: str
    tester: str
    blacklist: list[str]
    challenge: str
    reply: str
    tester_unambiguous: bool

    def validate(self):
        if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', self.trial_id):
            raise ValueError('invalid_binding')
        if self.chat_type not in ('group', 'friend') or self.tester_unambiguous is not True:
            raise ValueError('invalid_binding')
        if not all(isinstance(v, str) and v.strip() for v in
                   (self.account_alias, self.chat_name, self.tester, self.challenge, self.reply)):
            raise ValueError('invalid_binding')
        if not isinstance(self.blacklist, list) or not all(isinstance(v, str) for v in self.blacklist):
            raise ValueError('invalid_binding')
        if len(self.reply) > 500 or '\n' in self.reply or '\r' in self.reply:
            raise ValueError('invalid_binding')


@contextmanager
def owner(path):
    path.mkdir(parents=True, exist_ok=True)
    f = open(path / 'owner.lock', 'a+b')
    try:
        if os.name == 'nt':
            import msvcrt
            f.seek(0); f.write(b'0'); f.flush(); f.seek(0)
            msvcrt.locking(f.fileno(), msvcrt.LK_NBLCK, 1)
        else:
            import fcntl
            fcntl.flock(f, fcntl.LOCK_EX | fcntl.LOCK_NB)
        yield
    finally:
        f.close()


def write_record(path, record):
    fd, name = tempfile.mkstemp(dir=path.parent, prefix='.trial-', suffix='.tmp')
    try:
        with os.fdopen(fd, 'w', encoding='utf-8') as f:
            json.dump(record, f); f.flush(); os.fsync(f.fileno())
        os.replace(name, path)
    finally:
        if os.path.exists(name):
            os.unlink(name)


def pending(root):
    for path in root.glob('*.json'):
        try:
            record = json.loads(path.read_text(encoding='utf-8'))
            if record['state'] in ('prepared', 'submitted', 'unknown'):
                return True
            if record['state'] not in ('failed_before_submit', 'completed_observed'):
                return True
        except (ValueError, KeyError, OSError, TypeError):
            return True
    return False


def run_trial(binding, factory, root, clock=time.monotonic, sleep=time.sleep, timeout=120, limit=10):
    binding.validate()
    if not 0 < timeout <= 120 or not 0 < limit <= 10:
        raise ValueError('invalid_limits')
    root = Path(root)
    result = {'production_eligible': False, 'new_test_received': False, 'send_invoked': False,
              'framework_reported_success': False, 'operator_observed': False, 'outcome_unknown': False}
    with owner(root):
        path = root / (binding.trial_id + '.json')
        if pending(root) or path.exists():
            result['reason'] = 'pending_or_used'; return result
        record = {'state': 'failed_before_submit', 'ack': 'none', 'send_count': 0}
        def stop(reason):
            write_record(path, record); result['reason'] = reason; return result
        try:
            client = Wxauto4Client(factory)
            def matches():
                return client.current_chat() == (binding.chat_name, binding.chat_type)
            if not matches(): return stop('chat_mismatch')
            baseline = client.snapshot(binding.trial_id)
            if not matches(): return stop('chat_mismatch')
            ids = [m.ui_id for m in baseline]
            if len(set(ids)) != len(ids): return stop('ambiguous_ids')
            seen = set(ids)
            result['baseline_count'] = len(ids)
            start = clock(); candidates = 0
            while clock() - start < timeout:
                sleep(min(2, max(0, timeout - (clock() - start))))
                if clock() - start >= timeout: return stop('timeout')
                if not matches(): return stop('chat_mismatch')
                messages = client.snapshot(binding.trial_id)
                if not matches(): return stop('chat_mismatch')
                if clock() - start >= timeout: return stop('timeout')
                current = [m.ui_id for m in messages]
                if len(set(current)) != len(current) or (seen and not seen.intersection(current)):
                    return stop('ambiguous_ids')
                new = [m for m in messages if m.ui_id not in seen]
                seen.update(current)
                if candidates + sum(m.type == 'text' for m in new) > limit:
                    return stop('candidate_limit')
                eligible = [m for m in new if m.attr == 'friend' and m.type == 'text'
                            and m.sender == binding.tester and m.sender not in binding.blacklist
                            and m.content == binding.challenge]
                if len(eligible) > 1: return stop('ambiguous_messages')
                for message in new:
                    if message.type == 'text':
                        candidates += 1
                        if candidates > limit: return stop('candidate_limit')
                    if (message.attr == 'friend' and message.type == 'text' and
                        message.sender == binding.tester and message.sender not in binding.blacklist and
                        message.content == binding.challenge):
                        result['new_test_received'] = True
                        if not matches(): return stop('chat_mismatch')
                        if clock() - start >= timeout: return stop('timeout')
                        record = {'state': 'prepared', 'ack': 'none', 'send_count': 1}
                        write_record(path, record)
                        record['state'] = 'submitted'; write_record(path, record)
                        result['send_invoked'] = True
                        response = client.send_once(binding.reply)
                        if isinstance(response, dict) and response.get('status') == '成功':
                            record['ack'] = 'local_reported'
                            result['framework_reported_success'] = True
                        record['state'] = 'unknown'; write_record(path, record)
                        result['outcome_unknown'] = True; result['reason'] = 'unknown'; return result
                    if candidates >= limit: return stop('candidate_limit')
            return stop('timeout')
        except BaseException:
            if record['state'] in ('prepared', 'submitted'):
                record['state'] = 'unknown'; result['outcome_unknown'] = True
            write_record(path, record)
            result['reason'] = 'operation_failed'
            return result


def observe(root, trial_id):
    if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', trial_id): raise ValueError('invalid_trial')
    root = Path(root)
    with owner(root):
        path = root / (trial_id + '.json')
        record = json.loads(path.read_text(encoding='utf-8'))
        if record.get('state') not in ('prepared', 'submitted', 'unknown'):
            raise ValueError('not_pending')
        record.update(state='completed_observed', ack='operator_observed')
        write_record(path, record)


def main():
    parser = argparse.ArgumentParser()
    sub = parser.add_subparsers(dest='command', required=True)
    sub.add_parser('inspect'); sub.add_parser('mock')
    run = sub.add_parser('run'); run.add_argument('--mode', required=True, choices=['live']); run.add_argument('--binding', required=True)
    observed = sub.add_parser('observe'); observed.add_argument('--trial-id', required=True)
    args = parser.parse_args()
    try:
        if args.command == 'inspect': result = inspect_dependency()
        elif args.command == 'mock':
            from types import SimpleNamespace
            class MockClient:
                def __init__(self): self.polls = 0
                def ChatInfo(self): return {'chat_name': 'synthetic', 'chat_type': 'group'}
                def GetAllMessage(self):
                    self.polls += 1
                    old = SimpleNamespace(id='old', attr='friend', type='text', sender='test', content='old')
                    new = SimpleNamespace(id='new', attr='friend', type='text', sender='test', content='input')
                    return [old] if self.polls == 1 else [old, new]
                def SendMsg(self, *, msg): return None
            ticks = [0]
            with tempfile.TemporaryDirectory() as directory:
                binding = TrialBinding('mock', 'mock', 'synthetic', 'group', 'test', [], 'input', 'output', True)
                result = run_trial(binding, MockClient, directory, lambda: ticks[0],
                                   lambda seconds: ticks.__setitem__(0, ticks[0] + seconds))
            result['mode'] = 'mock'
        elif args.command == 'observe':
            observe('state/wxauto4-trials', args.trial_id); result = {'operator_observed': True, 'production_eligible': False}
        else:
            data = json.loads(Path(args.binding).read_text(encoding='utf-8'))
            binding = TrialBinding(**data); binding.validate()
            if not inspect_dependency()['dependency_present']:
                result = {'reason': 'dependency_unavailable', 'production_eligible': False}
            else:
                result = run_trial(binding, live_factory, 'state/wxauto4-trials')
    except (Exception, KeyboardInterrupt):
        result = {'reason': 'operation_failed', 'production_eligible': False}
    print(json.dumps(result, ensure_ascii=True))


if __name__ == '__main__': main()
