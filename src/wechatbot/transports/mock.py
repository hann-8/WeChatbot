from dataclasses import dataclass
from ..capabilities import Capabilities


@dataclass(frozen=True)
class SendResult:
    state: str
    ack_level: str = 'none'
    trace: str | None = None


class MockAdapter:
    offline = True

    def __init__(self, account='synthetic-account', epoch='synthetic-epoch'):
        self.capabilities = Capabilities(account, epoch)
        self.current_target = None
        self.calls = []
        self.next_state = 'accepted'

    async def send_text(self, target, text, trace, check):
        # Last check immediately before the mock submission. No awaits in between.
        if not check() or target != self.current_target:
            return SendResult('failed', trace=trace)
        self.calls.append((target, text, trace))
        if self.next_state == 'accepted':
            return SendResult('accepted', 'api_accepted', trace)
        return SendResult(self.next_state, 'none', trace)
