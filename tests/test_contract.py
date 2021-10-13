"""
Test covering Pytelliot EVM contract connection utils.
"""
import web3
from telliot.utils.abi import tellor_playground_abi
from telliot.utils.contract import Contract
from telliot.utils.rpc_endpoint import RPCEndpoint


network = "rinkeby"
provider = "infura"

func_name = "getNewValueCountbyRequestId"
requestId = "0x0000000000000000000000000000000000000000000000000000000000000002"


def test_connect_to_tellor_playground():
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    assert len(contract.contract.all_functions()) > 0
    assert isinstance(
        contract.contract.all_functions()[0], web3.contract.ContractFunction
    )


def test_call_read_function():
    """Contract object should be able to call arbitrary contract read function"""

    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    data, success = contract.read(func_name=func_name, _requestId=requestId)
    assert data[0] > 0
    assert success


def connect_to_contract(address):
    """Helper function for connecting to a contract at an address"""
    url = "https://rinkeby.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()

    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    c.connect()
    return c


def test_attempt_read_not_connected():
    """Read method should connect to contract if not connected"""
    address = "0x4699845F22CA2705449CFD532060e04abE3F1F31"
    url = "https://rinkeby.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()

    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    assert c.contract is None
    # read will succeed even if contract is initially diconnected
    assert c.read(func_name=func_name, _requestId=requestId)[0][0] > 0
    assert c.read(func_name=func_name, _requestId=requestId)[1]
