"""
Utils for connecting to an EVM contract
"""
from typing import Any
from typing import Dict
from typing import List
from typing import Optional

import web3
from pydantic import BaseModel
from telliot.utils.rpc_endpoint import RPCEndpoint


class Contract(BaseModel):
    """Convenience wrapper for connecting to an Ethereum contract"""

    #: RPCNode connection to Ethereum network
    node: RPCEndpoint

    #: Contract address
    address: str

    #: ABI specifications of contract
    abi: List[Dict[str, Any]]

    #: Contract address
    web3_contract: Optional[web3.contract.Contract]

    class Config:
        arbitrary_types_allowed = True

    def connect(self) -> None:
        """Connect to EVM contract through an RPC Endpoint"""
        if self.node.web3 is None:
            raise TypeError("node is not connected")
        else:
            self.web3_contract = self.node.web3.eth.contract(
                address=self.address, abi=self.abi
            )
