"""Read-only UI primitives. No pyweixin import, focus, text, pixels or send calls.

The Windows implementation is deliberately NOT reachable from the CLI. Its narrow
properties may be exercised only by a later explicitly authorized observation.
No data from this probe is a NormalizedEvent or a trusted identity.
"""
from dataclasses import dataclass, field
from typing import Protocol

from ..capabilities import Capabilities
from .mock import SendResult

UPSTREAM_COMMIT = '8589baa049bb91d3a500602c167f07b2f8397a13'


def _runtime_id(value):
    if (not isinstance(value, tuple) or not 1 <= len(value) <= 16 or
            any(type(x) is not int or x < 0 for x in value)):
        raise ValueError('invalid_runtime_id')


@dataclass(frozen=True)
class WindowBinding:
    # Operator reference is a declaration, NOT an observed stable account ID.
    account_reference: str = field(repr=False)
    pid: int
    process_started: float
    hwnd: int
    root_runtime_id: tuple[int, ...]
    list_runtime_id: tuple[int, ...]
    epoch: str

    def __post_init__(self):
        from ..contracts import opaque
        import math
        opaque(self.account_reference)
        opaque(self.epoch)
        if (type(self.pid) is not int or self.pid < 1 or
                type(self.hwnd) is not int or self.hwnd < 1 or
                type(self.process_started) not in (int, float) or
                not math.isfinite(self.process_started) or self.process_started <= 0):
            raise ValueError('invalid_window_binding')
        _runtime_id(self.root_runtime_id)
        _runtime_id(self.list_runtime_id)


@dataclass(frozen=True)
class VisibleItem:
    runtime_id: tuple[int, ...]
    class_name: str = 'mmui::ChatBubbleItemView'

    def __post_init__(self):
        _runtime_id(self.runtime_id)
        if type(self.class_name) is not str or len(self.class_name) > 128:
            raise ValueError('invalid_class')


@dataclass(frozen=True)
class Snapshot:
    binding: WindowBinding
    items: tuple[VisibleItem, ...]
    overflow: bool = False


class ReadOnlyPrimitives(Protocol):
    def snapshot(self) -> Snapshot: ...


class MockPrimitives:
    """Only caller-supplied synthetic snapshots; no real window discovery."""
    def __init__(self, snapshots):
        self.snapshots = iter(snapshots)
        self.calls = 0

    def snapshot(self):
        self.calls += 1
        return next(self.snapshots)


class BoundWindowPrimitives:
    """Minimal wrapper operations, exercised with synthetic UI objects only.

    Providers are explicit injection seams, not discovery mechanisms. No live
    provider is wired. A future Windows provider must prove a hard call timeout
    and account/window binding before open_real_observation can be implemented.
    """
    def __init__(self, root, binding, *, process_identity, foreground, list_title='消息'):
        if not isinstance(binding, WindowBinding) or list_title not in ('消息', 'Messages', '訊息'):
            raise ValueError('invalid_window_binding')
        self.binding = binding
        self.root = root
        self.process_identity = process_identity
        self.foreground = foreground
        self.list_title = list_title

    def _check(self):
        b = self.binding
        root = self.root.wrapper_object()
        if (root.process_id() != b.pid or root.handle != b.hwnd or
                self.process_identity(b.pid) != b.process_started or
                tuple(root.element_info.runtime_id) != b.root_runtime_id or
                self.foreground() != b.hwnd):
            raise ValueError('window_changed')
        # Locate only the message-list control inside the bound window. Never
        # enumerate top-level windows, sessions, contacts, or history tabs.
        chat = self.root.child_window(title=self.list_title, control_type='List').wrapper_object()
        if tuple(chat.element_info.runtime_id) != b.list_runtime_id:
            raise ValueError('window_changed')
        return chat

    def snapshot(self):
        chat = self._check()
        children = chat.children(control_type='CheckBox')
        if len(children) > 32:
            return Snapshot(self.binding, (), overflow=True)
        items = tuple(VisibleItem(tuple(c.element_info.runtime_id), c.class_name()) for c in children)
        self._check()  # Switching during the read discards the entire result.
        return Snapshot(self.binding, items)


def open_real_observation(*, mode='inspect', authorized=False, binding=None,
                          synthetic_samples=False, seconds=120, samples=10):
    # Configuration or CLI flags never constitute this session's human consent.
    if mode != 'observe' or authorized is not True or synthetic_samples is not True:
        raise ValueError('observation_not_authorized')
    from ..pyweixin_probe import ObservationLimits
    ObservationLimits(seconds, samples)
    if not isinstance(binding, WindowBinding):
        raise ValueError('invalid_window_binding')
    # Deliberately no imports, discovery or construction of a real UI provider.
    raise ValueError('real_observation_closed')


class CandidateCapabilities(Capabilities):
    def status(self):
        from ..pyweixin_probe import capability_report
        return capability_report()


class PyweixinAdapter:
    """Quarantined candidate; never promotes probe data to the business gate."""
    offline = False

    def __init__(self):
        self.capabilities = CandidateCapabilities(
            'unverified-account', 'unverified-epoch', transport='pyweixin',
            client_version='unobserved', adapter_code='wx02-probe-v1',
            stable_identity=False, real_mentions=False, stable_messages=False,
            correlated_ack=False)
        self.current_target = None

    async def send_text(self, target, text, trace, check):
        # Never call check, focus, set_text, a clipboard, or a keyboard primitive.
        return SendResult('failed', 'none', trace)

    def receive(self):
        raise ValueError('identity_unverified')


def keypress_result():
    """A successful key call supplies no associated transport acceptance."""
    return {'state': 'unknown', 'ack_level': 'none', 'reason': 'delivery_unverified'}


def image_capability():
    # Refer-bubble class / an image count cannot bind current-message pixels.
    return {'image_event': 'unverified', 'pixels': 'unsupported',
            'pixel_source': 'none', 'binding': 'unverified', 'material_handle': None}
