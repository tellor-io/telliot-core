from dataclasses import dataclass

from telliot.contract.contract import Contract

@dataclass
class TellorX:

    master: Contract

    oracle: Contract
