"""
Utils for connecting to an EVM contract
"""
import web3
from pydantic.dataclasses import dataclass
from telliot.utils.rpc_endpoint import RPCEndpoint


@dataclass
class Contract:
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    address: str

    #: Abi specifications of contract, likely loaded from JSON
    abi: str

    def connect(self) -> web3.contract.Contract:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            raise TypeError("node is not connected")
        else:
            self.web3_contract = self.node.web3.eth.contract(
                address=self.address, abi=self.abi
            )
            return self.web3_contract
