"""
Test covering Pytelliot EVM contract connection utils.
"""
import os

import pytest
import web3
from telliot.apps.telliot_config import TelliotConfig
from telliot.contract.contract import Contract
from telliot.contract.gas import estimate_gas
from telliot.utils.abi import tellor_playground_abi

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


@pytest.fixture
def c(cfg):
    """Helper function for connecting to a contract at an address"""
    endpoint = cfg.get_endpoint()
    endpoint.connect()
    c = Contract(
        address="0xb539Cf1054ba02933f6d345937A612332C842827",
        abi=tellor_playground_abi,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    c.connect()
    return c


def test_connect_to_tellor_playground(cfg, c):
    """Contract object should access Tellor Playground functions"""
    assert len(c.contract.all_functions()) > 0
    assert isinstance(c.contract.all_functions()[0], web3.contract.ContractFunction)


def test_call_read_function(cfg, c):
    """Contract object should be able to call arbitrary contract read function"""

    output, status = c.read(func_name=func_name, _requestId=requestId)
    assert status.ok
    assert output >= 0

def test_faucet(cfg, c):
    """Contract call to mint to an account with the contract faucet"""
    #estimate gas
    gas_price = estimate_gas()
    #set up user
    user = cfg.get_endpoint().web3.eth.account.from_key(cfg.main.private_key).address
    print(user)
    #read balance
    balance1, status = c.read(func_name="balanceOf", _account=user)
    assert status.ok
    assert balance1 >= 0
    print(balance1)
    #mint tokens to user
    receipt, status = c.write(func_name="faucet", gas_price=gas_price, _user=user)
    assert status.ok
    #read balance again
    balance2, status = c.read(func_name="balanceOf", _account=user)
    assert balance2 - balance1 == 1E21
    assert status.ok
    


@pytest.mark.skip(reason="We should ensure contract is connected when instantiated.")
def test_attempt_read_not_connected(cfg):
    """Read method should connect to contract if not connected"""
    address = "0xb539Cf1054ba02933f6d345937A612332C842827"
    endpoint = cfg.get_endpoint()
    endpoint.connect()

    c = Contract(
        address=address,
        abi=tellor_playground_abi,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    assert c.contract is None
    # read will succeed even if contract is initially diconnected
    status, output = c.read(func_name=func_name, _requestId=requestId)
    assert status.ok
    assert output >= 0
