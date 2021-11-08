"""
A wrapper for accessing all TellorX contracts in one place.
Each TellorX contract is accessible by its name.
"""
from dataclasses import dataclass

from telliot.contract.contract import Contract


@dataclass
class ContractsDict:
    """Main point of access for the assortment of TellorX contracts"""

    master: Contract

    oracle: Contract
