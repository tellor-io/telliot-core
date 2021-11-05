from dataclasses import dataclass

from telliot.contract.contract import Contract

@dataclass
class ContractsDict:

    master: Contract

    oracle: Contract
