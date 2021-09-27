from os import stat
from typing import Any
from eth_typing import abi
from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel
from web3 import Web3
import web3

@dataclass
class RPCEndpoint:
    """Convenience wrapper for connecting to Ethereum blockchain"""

    node_url:str

    def connect(self):
        self.web3 = Web3(Web3.HTTPProvider(self.node_url))

@dataclass
class Contract:
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    address: str

    #: Abi specifications of contract, likely loaded from JSON
    abi: str

    def connect(self):
        self.Contract = self.node.web3.eth.contract(
            address=self.address,
            abi=self.abi
        )