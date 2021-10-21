"""
Test covering Pytelliot EVM contract connection utils.
"""
import os

import pytest
import web3
from telliot.apps.telliot_config import TelliotConfig
from telliot.utils.abi import tellor_playground_abi
from telliot.utils.contract import Contract

func_name = "getNewValueCountbyRequestId"
requestId = "0x0000000000000000000000000000000000000000000000000000000000000002"


@pytest.fixture
def cfg():
    """Get rinkeby endpoint from config

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for rinkeby testnet
    cfg.main.chain_id = 4

    rinkeby_endpoint = cfg.get_endpoint()
    assert rinkeby_endpoint.network == "rinkeby"

    # Optionally override private key and URL with ENV vars for testing
    if os.getenv("PRIVATE_KEY", None):
        cfg.main.private_key = os.environ["PRIVATE_KEY"]

    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]

    return cfg


def test_connect_to_tellor_playground(cfg):
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract(cfg, "0xb539Cf1054ba02933f6d345937A612332C842827")
    assert len(contract.contract.all_functions()) > 0
    assert isinstance(
        contract.contract.all_functions()[0], web3.contract.ContractFunction
    )


def test_call_read_function(cfg):
    """Contract object should be able to call arbitrary contract read function"""

    contract = connect_to_contract(cfg, "0xb539Cf1054ba02933f6d345937A612332C842827")
    status, output = contract.read(func_name=func_name, _requestId=requestId)
    assert status.ok
    assert output >= 0


def connect_to_contract(cfg, address):
    """Helper function for connecting to a contract at an address"""
    endpt = cfg.get_endpoint()
    endpt.connect()

    c = Contract(address=address, abi=tellor_playground_abi, config=cfg)
    c.connect()
    return c


def test_attempt_read_not_connected(cfg):
    """Read method should connect to contract if not connected"""
    address = "0xb539Cf1054ba02933f6d345937A612332C842827"
    endpt = cfg.get_endpoint()
    endpt.connect()

    c = Contract(address=address, abi=tellor_playground_abi, config=cfg)
    assert c.contract is None
    # read will succeed even if contract is initially diconnected
    status, output = c.read(func_name=func_name, _requestId=requestId)
    assert status.ok
    assert output >= 0
