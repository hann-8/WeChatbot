"""Exactly one submit per attempt; ambiguous outcomes freeze the target."""
import asyncio
from .transports.mock import SendResult


async def deliver(store, adapter, gate, ticket, trace, text):
    if not gate.current(ticket):
        store.transition(trace, 'failed', 'delivery')
        return 'cancelled_target'
    store.transition(trace, 'submitted', 'delivery')
    try:
        result = await adapter.send_text(ticket.event.target, text, trace, lambda: gate.current(ticket))
        if (not isinstance(result, SendResult) or result.trace != trace or not gate.current(ticket)):
            store.transition(trace, 'unknown', 'delivery')
            return 'unknown'
        if (result.state == 'accepted' and result.ack_level in ('api_accepted', 'ui_observed') and
                adapter.capabilities.correlated_ack):
            store.accept(trace, ticket.event, text, result.ack_level)
            return 'accepted'
        if result.state == 'failed' and result.ack_level == 'none':
            store.transition(trace, 'failed', 'delivery')
            return 'failed'
        store.transition(trace, 'unknown', 'delivery')
        return 'unknown'
    except BaseException as error:
        # Cancellation during submit cannot prove the side effect did not happen.
        row = store.record(trace)
        if row['state'] == 'submitted':
            store.transition(trace, 'unknown', 'delivery')
        if isinstance(error, asyncio.CancelledError):
            raise
        if not isinstance(error, Exception):
            raise
        return 'unknown'
