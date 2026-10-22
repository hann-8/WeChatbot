"""Capabilities belong to a bound adapter, never to inbound caller claims."""
from dataclasses import dataclass
import hashlib
import json


@dataclass(frozen=True)
class Capabilities:
    account: str
    epoch: str
    transport: str = 'mock'
    client_version: str = 'synthetic-v1'
    adapter_code: str = 'wx01-mock-v1'
    stable_identity: bool = True
    real_mentions: bool = True
    stable_messages: bool = True
    correlated_ack: bool = True

    @property
    def digest(self):
        return hashlib.sha256(json.dumps(self.__dict__, sort_keys=True).encode()).hexdigest()

    @property
    def production_eligible(self):
        # No observed real capability exists in WX-01. A caller cannot set passed.
        return False

    def status(self):
        return dict(transport=self.transport, evidence='offline_synthetic',
                    identity='offline_passed', mentions='offline_passed',
                    delivery='offline_passed', production_eligible=False)
