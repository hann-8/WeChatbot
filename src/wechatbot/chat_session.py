"""Supervised single-window chat. All framework calls stay on its creating thread."""
import asyncio
from collections import deque
from dataclasses import dataclass
import hashlib
import json
from pathlib import Path
import re
import uuid

from qqbot_gateway.group_memory import MemoryStore, receipt_plan
from qqbot_gateway.token_budget import dialog_text
from .wxauto4_trial import write_record


@dataclass(frozen=True)
class ChatBinding:
    account_alias: str
    conversation_key: str
    chat_name: str
    allowed_senders: list
    blacklist: list
    chat_type: str = 'group'
    trigger_mode: str = 'text_prefix'
    prefix: str = 'bot '

    @classmethod
    def read(cls, path):
        binding = cls(**json.loads(Path(path).read_text(encoding='utf-8')))
        binding.validate()
        return binding

    def validate(self):
        for alias in (self.account_alias, self.conversation_key):
            if not re.fullmatch(r'[A-Za-z0-9_-]{1,64}', alias):
                raise ValueError('local_alias_required')
        if self.chat_type != 'group' or not isinstance(self.chat_name, str) or not self.chat_name.strip():
            raise ValueError('one_group_required')
        if (not isinstance(self.allowed_senders, list) or not self.allowed_senders or
                any(not isinstance(s, str) or not s.strip() for s in self.allowed_senders)
                or not isinstance(self.blacklist, list) or any(not isinstance(s, str) for s in self.blacklist)):
            raise ValueError('allowed_senders_required')
        if self.trigger_mode not in ('text_prefix', 'all_allowed_text'):
            raise ValueError('trigger_mode')
        if self.trigger_mode == 'text_prefix' and (not isinstance(self.prefix, str) or not self.prefix):
            raise ValueError('text_prefix_required')

    @property
    def namespace(self):
        return hashlib.sha256((self.account_alias + ':' + self.conversation_key).encode()).hexdigest()


class ChatSession:
    def __init__(self, config, binding, client, model, *, notify=print):
        binding.validate()
        self.config, self.binding, self.client, self.model = config, binding, client, model
        self.notify = notify
        self.root = config.root / 'state/wxauto4-chat' / binding.namespace
        self.root.mkdir(parents=True, exist_ok=True)
        self.history = []
        self.queue = deque()
        self.task = None
        self.active = None
        self.version = 0
        self.paused, self.stopped = False, False
        self.reason = 'ready'
        self.epoch = uuid.uuid4().hex
        self.seen = set()
        self.window_ids = set()
        self.memory_notice = False
        self.last_memory = None
        self.memory = MemoryStore(config.root, binding.account_alias, [binding.conversation_key],
                                  binding.blacklist, cfg=config.data['features']['memory'])
        self.unresolved = {}
        for path in self.root.glob('*.json'):
            record = json.loads(path.read_text(encoding='utf-8'))
            if record['state'] in ('prepared', 'submitted', 'unknown'):
                self.unresolved[path.stem] = record
        if self.unresolved:
            self.paused, self.reason = True, 'unknown'

    def matches(self):
        return self.client.current_chat() == (self.binding.chat_name, self.binding.chat_type)

    def invalidate(self, reason):
        self.version += 1
        self.paused, self.reason = True, reason
        self.queue.clear()

    def baseline(self):
        if not self.matches():
            self.invalidate('chat_mismatch'); return False
        rows = self.client.snapshot(self.epoch)
        if not self.matches():
            self.invalidate('chat_mismatch'); return False
        ids = [m.ui_id for m in rows]
        if len(ids) != len(set(ids)):
            self.invalidate('ambiguous_ui_ids'); return False
        self.seen = set(ids)
        self.window_ids = set(ids)
        self.notify('baseline_ready')
        return True

    def poll(self):
        if self.paused or self.stopped:
            return
        if not self.matches():
            self.invalidate('chat_mismatch'); return
        rows = self.client.snapshot(self.epoch)
        if not self.matches():
            self.invalidate('chat_mismatch'); return
        ids = [m.ui_id for m in rows]
        current = set(ids)
        if len(ids) != len(current) or (self.window_ids and not self.window_ids.intersection(current)):
            self.invalidate('window_changed'); return
        new = [m for m in rows if m.ui_id not in self.seen]
        self.seen.update(current)
        self.window_ids = current
        for message in new:
            b = self.binding
            # Blacklist before allowlist and model dispatch; self/system/media ignored.
            if (message.sender in b.blacklist or message.sender not in b.allowed_senders
                    or message.attr != 'friend' or message.type != 'text'):
                continue
            question = message.content
            if b.trigger_mode == 'text_prefix':
                if not question.startswith(b.prefix):
                    continue
                question = question[len(b.prefix):]
            if not question.strip():
                continue
            if len(self.queue) >= self.config.data['models']['llm']['queue_limit']:
                self.notify('queue_full_new_message_skipped'); continue
            self.queue.append((message.sender, question))

    def valid(self, version):
        if self.paused or self.stopped or version != self.version:
            return False
        if not self.matches():
            self.invalidate('chat_mismatch'); return False
        return True

    async def advance(self):
        if self.task is not None and self.task.done():
            task, self.task = self.task, None
            sender, question, request, version, source, context, ref = self.active
            self.active = None
            record = None
            try:
                answer = task.result()
                if not self.valid(version):
                    return
                requested = answer.aux.get('receipt') is True
                self.last_memory = self.memory.stage(context, answer.aux, source)
                if requested and context is None:
                    self.last_memory = dict(result='failed', reason='snapshot_unavailable')
                if self.last_memory['result'] in ('failed', 'rejected'):
                    if not self.memory_notice:
                        self.notify('memory_unavailable_basic_text_continues')
                        self.memory_notice = True
                    if self.last_memory['reason'] in ('storage', 'capacity', 'snapshot_unavailable'):
                        self.memory.disabled.add(self.binding.conversation_key)
                plan = receipt_plan(answer.plan, self.last_memory, requested, self.model.output)
                text = plan.canonical_text
                if not self.valid(version):
                    return
                path = self.root / (request + '.json')
                record = dict(state='prepared', ack='none', send_count=0,
                              memory_result=self.last_memory['result'])
                write_record(path, record)
                if not self.valid(version):
                    record['state'] = 'failed_before_submit'; write_record(path, record); return
                # Persist intent before the one framework call. An interrupted intent is unresolved.
                record.update(state='submitted', send_count=1)
                write_record(path, record)
                try:
                    response = self.client.send_once(text)
                    success = isinstance(response, dict) and response.get('status') == '成功'
                except Exception:
                    success = False
                if success:
                    record.update(state='local_reported', ack='local_reported')
                    # Tool text and memory snapshots are not carried as user assertions.
                    history_reply = '本轮已联网回答；网页材料不作为群友事实。' if answer.used_web else text
                    self.history.extend([dict(role='user', content=dialog_text([dict(sender_ref=ref, text=question)])),
                                         dict(role='assistant', content=history_reply)])
                    self.history = self.history[-2*self.config.data['chat']['history_turns']:]
                else:
                    record['state'] = 'unknown'
                    self.unresolved[request] = record
                    self.invalidate('unknown')
                write_record(path, record)
                self.notify(record['state'])
            except Exception as error:
                # No second model task, no automatic send retry, no raw exception/message log.
                if record is not None and record.get('send_count'):
                    self.unresolved[request] = record | dict(state='unknown')
                    self.invalidate('unknown')
                code = getattr(error, 'code', 'MODEL_FORMAT_OR_STORAGE')
                self.notify('turn_failed_no_retry:' + (code if re.fullmatch('[A-Z_]+', str(code)) else 'UNKNOWN'))
            finally:
                self.memory.close(context)
        if self.task is None and self.queue and not self.paused and not self.stopped:
            sender, question = self.queue.popleft()
            version = self.version
            if not self.valid(version):
                return
            request = uuid.uuid4().hex
            source = {}
            # Pure MemoryStore accepts opaque strings. No QQ event/number is manufactured.
            ref = 'p_' + hashlib.sha256(sender.encode()).hexdigest()[:16]
            context = self.memory.prepare(self.binding.conversation_key, hashlib.sha256(request.encode()).hexdigest(),
                                          source, {ref: sender}, [])
            if self.memory.cfg['enabled'] and context is None and not self.memory_notice:
                self.notify('memory_unavailable_basic_text_continues'); self.memory_notice = True
                self.memory.disabled.add(self.binding.conversation_key)
            self.active = (sender, question, request, version, source, context, ref)
            self.task = asyncio.create_task(self.model.generate(question, ref, source, list(self.history), request))

    def command(self, line):
        parts = line.strip().split()
        if not parts:
            return self.status()
        command = parts[0]
        if command == 'pause':
            self.invalidate('operator_pause')
        elif command == 'reset':
            self.version += 1; self.history.clear(); self.queue.clear()
            # New baseline prevents queued old messages resurfacing; long-term memory stays.
            self.baseline()
        elif command == 'resume':
            if self.unresolved:
                return dict(reason='resolve_unknown_first', pending=list(self.unresolved))
            if self.reason == 'binding_changed':
                return dict(reason='restart_with_binding')
            self.version += 1; self.queue.clear(); self.epoch = uuid.uuid4().hex
            if self.baseline():
                self.paused, self.reason = False, 'ready'
        elif command == 'stop':
            self.invalidate('operator_stop'); self.stopped = True
        elif command in ('confirm-sent', 'mark-not-sent'):
            key = parts[1] if len(parts) > 1 else next(iter(self.unresolved), None)
            if key not in self.unresolved:
                return dict(reason='no_such_pending')
            record = self.unresolved[key]
            record['state'] = 'operator_confirmed_sent' if command == 'confirm-sent' else 'operator_not_sent'
            record['ack'] = 'operator_observed'
            write_record(self.root / (key + '.json'), record)
            del self.unresolved[key]
        elif command == 'memory-status':
            try:
                info = self.memory.manage(self.binding.conversation_key, 'inspect')
                return {k: info[k] for k in ('records','chars','bytes','revision','limits')} | dict(last_save=self.last_memory)
            except (ValueError, OSError):
                return dict(memory='unavailable', last_save=self.last_memory)
        elif command != 'status':
            return dict(reason='unknown_local_command')
        return self.status()

    def status(self):
        return dict(paused=self.paused, stopped=self.stopped, reason=self.reason,
                    queued=len(self.queue), running=self.task is not None,
                    history_turns=len(self.history)//2, pending=list(self.unresolved))

    async def close(self):
        self.command('stop')
        if self.task:
            self.task.cancel()
            await asyncio.gather(self.task, return_exceptions=True)
            self.memory.close(self.active[5])
        await self.model.close()
