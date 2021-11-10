"""
A wrapper for accessing all TellorX contracts in one place.
Each TellorX contract is accessible by its name.
"""
from dataclasses import dataclass

from telliot_core.contract.contract import Contract


@dataclass
class TellorContracts:
    """Main point of access for the assortment of TellorX contracts"""

    master: Contract

    oracle: Contract
