"""Bounded, metadata-only probe, separate from router/history/model paths."""
import math
import time
import hashlib
import json
from pathlib import Path
from dataclasses import dataclass

from .transports.pyweixin_adapter import (
    UPSTREAM_COMMIT, MockPrimitives, Snapshot, VisibleItem, WindowBinding,
    image_capability, keypress_result,
)


def capability_report():
    return {
        'upstream_commit': UPSTREAM_COMMIT, 'distribution': 'pywechat127',
        'declared_version': '1.9.8', 'evidence': 'source_review_only',
        'real_observed': False, 'production_eligible': False,
        'identity': 'identity_unverified', 'mentions': 'mention_unverified',
        'delivery': 'delivery_unverified', 'real_entry_enabled': False,
        'stable_account_id': 'unverified', 'stable_conversation_id': 'unverified',
        'stable_sender_id': 'unverified', 'stable_message_id': 'unverified',
        'display_names': 'source_supported_not_identity',
        'ui_runtime_id': 'source_supported_process_local_not_message_id',
        'trusted_real_mention': 'unverified', 'sender_is_self': 'unverified',
        'images': image_capability(), 'send_result': keypress_result(),
        'live_entry_blocker': 'hard_deadline_and_single_window_binding_unobserved',
    }


def inspect_candidate(root=None):
    """Hash inert local evidence; not an upstream import or runtime observation."""
    root = Path(root) if root is not None else Path(__file__).resolve().parents[2]
    base = root / 'vendor/pyweixin'
    result = capability_report()
    try:
        hashes = json.loads((base / 'evidence-hashes.json').read_text('utf-8'))
        for name, expected in hashes.items():
            target = base / name
            if (not target.resolve().is_relative_to(base.resolve()) or
                    target.is_symlink() or any(p.is_symlink() for p in target.parents)):
                raise ValueError('evidence_path')
            if hashlib.sha256(target.read_bytes()).hexdigest() != expected:
                raise ValueError('evidence_hash')
        lock = json.loads((base / 'source-lock.json').read_text('utf-8'))
        if (lock['commit'] != UPSTREAM_COMMIT or lock['declared_version'] != '1.9.8' or
                lock['distribution'] != 'pywechat127' or lock['upstream_installed'] is not False):
            raise ValueError('source_pin')
        result['local_evidence'] = 'hash_verified_not_runtime_observed'
    except (ValueError, OSError, KeyError, TypeError):
        result['local_evidence'] = 'unavailable_or_invalid'
    return result


@dataclass(frozen=True)
class ObservationLimits:
    seconds: float = 120
    samples: int = 10

    def __post_init__(self):
        if (type(self.seconds) not in (int, float) or not math.isfinite(self.seconds) or
                not 0 < self.seconds <= 120 or type(self.samples) is not int or
                not 1 <= self.samples <= 10):
            raise ValueError('observation_limits')


class ProbeSession:
    """Explicitly synthetic offline sessions only; no raw text or pixel API.

    Baseline properties are runtime IDs/class names, never historical text.
    Runtime recycling is inherently ambiguous: reject removal/reconstruction,
    never manufacture stable IDs from names/text, never claim no missed messages.
    """
    def __init__(self, primitives, binding, *, limits=None, clock=time.monotonic):
        if type(primitives) is not MockPrimitives:
            raise ValueError('real_observation_closed')
        if not isinstance(binding, WindowBinding):
            raise ValueError('invalid_window_binding')
        self.primitives, self.binding = primitives, binding
        self.limits, self.clock = limits or ObservationLimits(), clock
        self.deadline = clock() + self.limits.seconds
        self.seen = None
        self.count = 0
        self.closed = False

    def _stop(self, reason):
        self.closed = True
        return {'state': reason, 'new_runtime_samples': 0, 'production_eligible': False}

    def poll(self):
        if self.closed:
            return self._stop('closed')
        if self.clock() >= self.deadline:
            return self._stop('deadline')
        try:
            snap = self.primitives.snapshot()
        except Exception:
            return self._stop('ui_unavailable')
        if self.clock() >= self.deadline:
            return self._stop('deadline')
        if not isinstance(snap, Snapshot) or snap.binding != self.binding:
            return self._stop('window_changed')
        if (snap.overflow or type(snap.items) is not tuple or len(snap.items) > 32 or
                any(type(x) is not VisibleItem for x in snap.items)):
            return self._stop('invalid_or_overflow')
        current = {x.runtime_id for x in snap.items}
        if len(current) != len(snap.items):
            return self._stop('ambiguous_runtime_ids')
        if self.seen is None:
            self.seen = current
            return {'state': 'baseline_discarded', 'new_runtime_samples': 0,
                    'production_eligible': False}
        if not self.seen.issubset(current):
            return self._stop('virtual_list_or_reconstruction_unverified')
        new = current - self.seen
        if len(new) > self.limits.samples - self.count:
            return self._stop('sample_budget_exceeded')
        self.seen = current
        self.count += len(new)
        if self.count == self.limits.samples:
            self.closed = True
        return {'state': 'offline_synthetic', 'new_runtime_samples': len(new),
                'identity': 'identity_unverified', 'mentions': 'mention_unverified',
                'delivery': 'delivery_unverified', 'production_eligible': False}


def mock_probe():
    binding = WindowBinding('synthetic-account', 1, 1.0, 1, (1,), (2,), 'synthetic-epoch')
    primitive = MockPrimitives([
        Snapshot(binding, (VisibleItem((10,)),)),
        Snapshot(binding, (VisibleItem((10,)), VisibleItem((11,)))),
    ])
    session = ProbeSession(primitive, binding)
    return {'evidence': 'offline_synthetic', 'steps': [session.poll(), session.poll()],
            'capabilities': capability_report()}
