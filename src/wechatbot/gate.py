"""Authorization precedes dedup, RAM window, image materials, model and history."""
from dataclasses import dataclass
from qqbot_gateway.group_silence import silence_request
from .contracts import NormalizedEvent


@dataclass(frozen=True)
class Ticket:
    event: NormalizedEvent
    digest: str
    generation: int


class Gate:
    def __init__(self, config, adapter, store):
        self.config, self.adapter, self.store = config, adapter, store
        self.sequence = 0
        self.monotonic = 0
        self.epoch = adapter.capabilities.epoch
        self.muted = set()
        self.generations = {}

    def base_reason(self, event):
        d, cap = self.config.data, self.adapter.capabilities
        if not isinstance(event, NormalizedEvent):
            return 'invalid_event'
        if (event.transport != d['bot']['transport'] or event.transport != cap.transport or
                event.account_id != cap.account or event.capabilities_digest != cap.digest):
            return 'transport_or_account'
        if not cap.stable_identity:
            return 'identity_unverified'
        if event.sender_id in d['bot']['blocked_users']:
            return 'blocked_sender'
        if event.conversation_kind == 'group':
            if event.conversation_id not in d['bot']['allowed_groups']:
                return 'unauthorized_group'
        else:
            direct = d['chat']['direct']
            if (not direct['enabled'] or event.sender_id not in direct['allowed_users'] or
                    event.conversation_id not in direct['allowed_conversations']):
                return 'direct_disabled_or_unbound'
        if event.sender_is_self or event.sender_id == cap.account:
            return 'self_loop'
        if event.adapter_epoch != cap.epoch:
            return 'stale_epoch'
        if not event.text.strip():
            return 'no_text_material'
        if event.id_scope != 'server_stable' and cap.transport != 'mock':
            return 'message_id_unverified'
        if not cap.stable_messages and cap.transport != 'mock':
            return 'message_id_unverified'
        if cap.transport != 'mock' or not self.adapter.offline:
            return 'real_channel_closed'
        return None

    def admit(self, event):
        reason = self.base_reason(event)
        if reason:
            return None, reason
        cap = self.adapter.capabilities
        if self.epoch != cap.epoch:
            self.epoch = cap.epoch
            self.sequence, self.monotonic = 0, 0
        if event.received_seq <= self.sequence or event.received_monotonic < self.monotonic:
            return None, 'stale_sequence'
        self.sequence, self.monotonic = event.received_seq, event.received_monotonic
        if not self.store.claim(event):
            return None, 'duplicate'
        if event.conversation_kind == 'group':
            stop = self.config.data['chat']['silence']['enabled'] and silence_request(event.text, (), event.mention_self is True)
            target = event.target
            if stop:
                self.muted.add(target)
                self.generations[target] = self.generations.get(target, 0) + 1
                return None, 'silenced'
            if event.mention_self is not True or not cap.real_mentions:
                return None, 'mention_unverified_or_absent'
            if target in self.muted:
                self.muted.remove(target)
                self.generations[target] = self.generations.get(target, 0) + 1
        if self.store.uncertain(event.target):
            return None, 'target_blocked'
        return Ticket(event, cap.digest, self.generations.get(event.target, 0)), 'admitted'

    def current(self, ticket):
        e = ticket.event
        return (self.base_reason(e) is None and ticket.digest == self.adapter.capabilities.digest and
                ticket.generation == self.generations.get(e.target, 0) and e.target not in self.muted and
                self.adapter.current_target == e.target)
