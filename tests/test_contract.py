"""
Test covering Pytelliot EVM contract connection utils.
"""
import web3
from telliot.utils.abi import tellor_playground_abi
from telliot.utils.contract import Contract
from telliot.utils.rpc_endpoint import RPCEndpoint
from tests.test_rpc_endpoint import connect_to_rpc


network = "mainnet"
provider = "pokt"


def test_read_tellor_playground():
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    assert len(contract.all_functions()) > 0
    assert isinstance(
        contract.all_functions()[0], web3.contract.ContractFunction
    )


def connect_to_contract(address):
    """Helper function for connecting to a contract at an address"""
    url = "https://mainnet.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt, _ = connect_to_rpc(url)
    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    return c.contract
