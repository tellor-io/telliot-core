from typing import Any
from eth_typing import abi
from pydantic.dataclasses import dataclass
from pydantic.main import BaseModel
from web3 import Web3
import web3

@dataclass
class RPCEndpoint(BaseModel):
    """Convenience wrapper for connecting to Ethereum blockchain"""

    #: RPC url
    rpc_endpoint: str

    #: Tellor Contract
    tellor_contract: web3.eth.Eth.contract

    def __init__(self, rpc_endpoint:str) -> None:
        Web3(Web3.HTTPProvider(rpc_endpoint))

    def connect_to_contract(address:str) -> web3.eth.Eth.contract:
        """Connect to Tellor contract at a given address"""

        with open("abi.json") as f:
            abi = f.read()

        return Web3.eth.contract(address=address, abi=abi)
