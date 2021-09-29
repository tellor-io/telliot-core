"""
Test covering Pytelliot EVM contract connection utils.
"""

import web3

from telliot.utils.contract import Contract
from telliot.utils.rpc_endpoint import RPCEndpoint

with open("abi.json") as f:
    abi = f.read()

network = "mainnet"
provider = "pokt"

def test_read_tellor_playground():
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    assert len(contract.web3_contract.all_functions()) > 0
    assert isinstance(
        contract.web3_contract.all_functions()[0], web3.contract.ContractFunction
    )
def connect_to_contract(address):
    """Helper function for connecting to a contract at an address"""
    url = "https://mainnet.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()

    c = Contract(endpt, address, abi)
    c.connect()
    return c