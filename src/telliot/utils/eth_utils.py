from typing import Any
from eth_typing import abi
from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel
from web3 import Web3

@dataclass
class RPCEndpoint(Web3):
    """Convenience wrapper for connecting to Ethereum blockchain"""

    #: RPC url
    rpc_endpoint: str

    #: Tellor Contract
    tellor_contract: Web3.eth.contract

    def __init__(self, rpc_endpoint:str) -> None:
        super().__init__(super().HTTPProvider(rpc_endpoint))

    def connect_to_contract(address:str) -> Web3.eth.contract:
        """Connect to Tellor contract at a given address"""

        with open("abi.json") as f:
            abi = f.read()

        return super().eth.contract(address=address, abi=abi)
