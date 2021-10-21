"""
Test covering Pytelliot EVM contract connection utils.
"""
from os import name
import os
from pathlib import Path
import pytest
import web3
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.abi import tellor_playground_abi
from telliot.utils.contract import Contract


network = "rinkeby"
provider = "infura"

func_name = "getNewValueCountbyRequestId"
requestId = "0x0000000000000000000000000000000000000000000000000000000000000002"

@pytest.fixture
def app():
    class NewAppConfig(AppConfig):
        private_key: str = ""
        contract_address: str = (
            "0x4699845F22CA2705449CFD532060e04abE3F1F31"  # tellorX playground
        )
        chain_id: int = 4  # rinkeby

    class TestApp(Application):
        def __init__(self, **data):
            super().__init__(name="reporter", config_class=NewAppConfig, **data)

    test_app = TestApp()

    if not test_app.config.private_key:
        test_app.config.private_key = os.environ["PRIVATE_KEY"]

    if "e.g." in test_app.telliot_config.default_endpoint.provider:
        test_app.telliot_config.default_endpoint.provider = "pokt"

    if "e.g." in test_app.telliot_config.default_endpoint.url:
        test_app.telliot_config.default_endpoint.url = os.environ["NODE_URL"]

    if "e.g." in test_app.telliot_config.default_endpoint.network:
        test_app.telliot_config.default_endpoint.network = "rinkeby"

    return test_app

def test_connect_to_tellor_playground(app):
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract(app, "0x4699845F22CA2705449CFD532060e04abE3F1F31")
    assert len(contract.contract.all_functions()) > 0
    assert isinstance(
        contract.contract.all_functions()[0], web3.contract.ContractFunction
    )


def test_call_read_function(app):
    """Contract object should be able to call arbitrary contract read function"""

    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    output = contract.read(func_name=func_name, _requestId=requestId)
    assert output.result > 0
    assert output.ok


def connect_to_contract(app, address):
    """Helper function for connecting to a contract at an address"""
    endpt = app.telliot_config.default_endpoint
    endpt.connect()

    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    c.connect()
    return c


def test_attempt_read_not_connected(app):
    """Read method should connect to contract if not connected"""
    address = app.config.contract_address
    endpt = app.telliot_config.default_endpoint
    endpt.connect()

    c = Contract(node=endpt, address=address, abi=tellor_playground_abi)
    assert c.contract is None
    # read will succeed even if contract is initially diconnected
    assert c.read(func_name=func_name, _requestId=requestId).result > 0
    assert c.read(func_name=func_name, _requestId=requestId).ok
