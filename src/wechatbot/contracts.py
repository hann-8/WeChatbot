"""Closed, bounded wire format. Display text never supplies an identity."""
from dataclasses import dataclass, fields
import json
import math
import unicodedata


def opaque(value):
    if (not isinstance(value, str) or not 1 <= len(value) <= 256 or
            value in ('.', '..') or any(c in value for c in '/\\:') or
            any(unicodedata.category(c).startswith('C') for c in value)):
        raise ValueError('invalid_identifier')
    return value


def pairs(items):
    result = {}
    for key, value in items:
        if key in result:
            raise ValueError('duplicate_key')
        result[key] = value
    return result


@dataclass(frozen=True)
class NormalizedEvent:
    version: int
    platform: str
    transport: str
    account_id: str
    conversation_kind: str
    conversation_id: str
    sender_id: str
    source_message_id: str
    id_scope: str
    received_seq: int
    received_monotonic: float
    adapter_epoch: str
    sender_is_self: bool
    text: str
    capabilities_digest: str
    mention_self: bool | None = None
    first_image_handle: str | None = None
    display_name: str | None = None

    def __post_init__(self):
        if (type(self.version) is not int or self.version != 1 or self.platform != 'wechat' or
                self.transport not in ('mock', 'pyweixin') or
                self.conversation_kind not in ('group', 'direct') or
                self.id_scope not in ('server_stable', 'process_local')):
            raise ValueError('invalid_event')
        for key in ('account_id', 'conversation_id', 'sender_id', 'source_message_id',
                    'adapter_epoch', 'capabilities_digest'):
            opaque(getattr(self, key))
        if (type(self.received_seq) is not int or self.received_seq < 1 or
                type(self.received_monotonic) not in (int, float) or
                not math.isfinite(self.received_monotonic) or self.received_monotonic < 0 or
                type(self.sender_is_self) is not bool or
                self.mention_self is not None and type(self.mention_self) is not bool):
            raise ValueError('invalid_event')
        if (not isinstance(self.text, str) or len(self.text) > 4000 or
                any(unicodedata.category(c).startswith('C') and c not in '\n\t' for c in self.text)):
            raise ValueError('invalid_text')
        if self.first_image_handle is not None:
            opaque(self.first_image_handle)
        if self.display_name is not None and (not isinstance(self.display_name, str) or
                len(self.display_name) > 256 or
                any(unicodedata.category(c).startswith('C') for c in self.display_name)):
            raise ValueError('invalid_display')

    @property
    def target(self):
        return (self.account_id, self.conversation_kind, self.conversation_id)

    @property
    def history_key(self):
        return self.target + (self.sender_id,)


def decode_batch(raw: bytes):
    if not isinstance(raw, bytes) or len(raw) > 65536:
        raise ValueError('batch_size')
    data = json.loads(raw.decode('utf-8'), object_pairs_hook=pairs,
                      parse_constant=lambda _: (_ for _ in ()).throw(ValueError('non_finite')))
    if not isinstance(data, list) or not 1 <= len(data) <= 32:
        raise ValueError('batch_count')
    allowed = {f.name for f in fields(NormalizedEvent)}
    result = []
    for row in data:
        if not isinstance(row, dict) or set(row) - allowed:
            raise ValueError('event_fields')
        try:
            result.append(NormalizedEvent(**row))
        except TypeError:
            raise ValueError('event_fields') from None
    return tuple(result)
