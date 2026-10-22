"""One global generation slot, bounded waiting queue and frozen task targets."""
import asyncio
from collections import deque
import uuid
from qqbot_gateway.errors import GatewayError
from .delivery import deliver
from .gate import Gate


class Router:
    def __init__(self, config, adapter, store, model):
        self.config, self.adapter, self.store, self.model = config, adapter, store, model
        self.gate = Gate(config, adapter, store)
        self.lock = asyncio.Lock()
        self.waiting = 0
        self.windows = {}
        self.last_trace = None

    async def handle(self, event):
        ticket, reason = self.gate.admit(event)
        if ticket is None:
            return reason
        limit = self.config.data['models']['llm']['queue_limit']
        if self.lock.locked() and self.waiting >= limit:
            return 'queue_full'
        self.waiting += 1
        queued = True
        trace = None
        try:
            async with self.lock:
                self.waiting -= 1
                queued = False
                if not self.gate.current(ticket):
                    return 'cancelled_target'
                if self.store.blocked(event.target) or self.model.status()['blocked']:
                    return 'target_or_model_blocked'
                # Only admitted, current and unfrozen events can reach a RAM window.
                if event.history_key not in self.windows and len(self.windows) >= 256:
                    return 'window_capacity'
                window = self.windows.setdefault(event.history_key, deque(maxlen=32))
                window.append(event.text)
                trace = self.last_trace = uuid.uuid4().hex[:10]
                self.store.prepare(trace, event.target)
                try:
                    reply = await self.model.generate(event, self.store.history(event), trace)
                except GatewayError as error:
                    state = 'failed' if error.code == 'INPUT_TOO_LONG' else 'unknown'
                    self.store.transition(trace, state, 'model')
                    return 'model_' + state
                if not self.gate.current(ticket):
                    self.store.transition(trace, 'failed', 'delivery')
                    return 'cancelled_target'
                return await deliver(self.store, self.adapter, self.gate, ticket, trace, reply)
        except BaseException as error:
            # If cancellation occurred while waiting, there was no model request.
            if trace is None:
                # A waiter has not decremented the counter yet if lock is held.
                if queued:
                    self.waiting -= 1
            else:
                row = self.store.record(trace)
                if row and row['state'] in ('prepared', 'submitted'):
                    self.store.transition(trace, 'unknown', row['phase'])
            if isinstance(error, asyncio.CancelledError) or not isinstance(error, Exception):
                raise
            return 'model_unknown'

    def status(self):
        return dict(phase='offline_only', transport='mock', real_channel=False,
                    real_sends=False, real_model=False, queued=self.waiting,
                    busy=self.lock.locked(), counts=self.store.counts(),
                    model_cleanup=self.model.status(), capabilities=self.adapter.capabilities.status())
