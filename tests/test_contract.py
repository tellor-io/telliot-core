"""
Test covering Pytelliot EVM contract connection utils.
"""
from hexbytes.main import HexBytes

import os
import pytest
import time
import web3
from web3 import Web3
from telliot.apps.telliot_config import TelliotConfig
from telliot.contract.contract import Contract
from telliot.contract.gas import fetch_gas_price
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.abi import rinkeby_tellor_master, rinkeby_tellor_oracle


@pytest.fixture
def cfg():
    """Get rinkeby endpoint from config

    If environment variables are defined, they will override the values in config files
    """
    cfg = TelliotConfig()

    # Override configuration for rinkeby testnet
    cfg.main.chain_id = 4

    rinkeby_endpoint = cfg.get_endpoint()
    # assert rinkeby_endpoint.network == "rinkeby"

    # Optionally override private key and URL with ENV vars for testing
    if os.getenv("PRIVATE_KEY", None):
        cfg.main.private_key = os.environ["PRIVATE_KEY"]

    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]

    return cfg


@pytest.fixture
def master(cfg):
    """Helper function for connecting to a contract at an address"""
    endpoint = cfg.get_endpoint()
    # endpoint = RPCEndpoint(chain_id = 31337, network="localhost", provider="local", url=os.environ["NODE_URL"])
    endpoint.connect()
    master = Contract(
        address="0x202bEFC6E551C0E28Bc461363C1aa9fF6D3B1813",
        abi=rinkeby_tellor_master,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    master.connect()
    return master

@pytest.fixture
def oracle(cfg):
    """Helper function for connecting to a contract at an address"""
    endpoint = cfg.get_endpoint()
    # endpoint = RPCEndpoint(chain_id = 31337, network="localhost", provider="local", url=os.environ["NODE_URL"])
    endpoint.connect()
    oracle = Contract(
        address="0xa717F9684c77194d99a7f088833dee6FbD2a75dD",
        abi=rinkeby_tellor_oracle,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    oracle.connect()
    return oracle


def test_connect_to_tellor(cfg, master):
    """Contract object should access Tellor functions"""
    assert len(master.contract.all_functions()) > 0
    assert isinstance(master.contract.all_functions()[0], web3.contract.ContractFunction)

@pytest.mark.skip(reason="for playground.")
@pytest.mark.asyncio
async def test_call_read_function(cfg, master):
    """Contract object should be able to call arbitrary contract read function"""

    output, status = await master.read(func_name="getTimestampCountById", _queryId=Web3.keccak(HexBytes(2)))
    assert status.ok
    assert output >= 0

@pytest.mark.skip(reason="krasi oracle contract does not have balanceOf")
@pytest.mark.asyncio
async def test_faucet(cfg, c):
    """Contract call to mint to an account with the contract faucet"""
    # estimate gas
    gas_price = await fetch_gas_price()
    # set up user
    user = c.node.web3.eth.account.from_key(cfg.main.private_key).address
    # read balance
    balance1, status = await c.read(func_name="balanceOf", _account=user)
    assert status.ok
    assert balance1 >= 0
    print(balance1)
    # mint tokens to user
    receipt, status = await c.write_with_retry(
        func_name="faucet",
        gas_price=gas_price,
        extra_gas_price=20,
        retries=1,
        _user=user,
    )
    assert status.ok
    # read balance again
    balance2, status = await c.read(func_name="balanceOf", _account=user)
    assert status.ok
    print(balance2)
    assert balance2 - balance1 == 1e21

@pytest.mark.asyncio
async def test_trb_transfer(cfg, master):
    """Test TRB transfer through TellorMaster contract (and its proxies)"""

    gas_price = await fetch_gas_price()
    sender = master.node.web3.eth.account.from_key(cfg.main.private_key).address
    balance, status = await master.read("balanceOf", _user=sender)
    print("my sender address:" ,sender)
    print("my sender balance:", balance / 1E18)
    recipient = str(Web3.toChecksumAddress("0xf3428C75CAfb3FBA46D3E190B7539Fbbfb96f244"))


    balance, status = await master.read("balanceOf", _user=recipient)
    assert status.ok
    print("before:", balance / 1E18)

    receipt, status = await master.write("transfer", _to=recipient, _amount=1, gas_price=gas_price)
    print(status.error)
    assert status.ok

    balance, status = await master.read("balanceOf", _user=recipient)
    print("after:", balance / 1E18)



@pytest.mark.asyncio
async def test_submit_value(cfg, master, oracle):

    gas_price = await fetch_gas_price()
    user = master.node.web3.eth.account.from_key(cfg.main.private_key).address
    print(user)

    balance, status = await master.read("balanceOf", _user=user)
    print(balance / 1E18)

    is_staked, status = await master.read("getStakerInfo", _staker=user)
    print(is_staked)

    if is_staked[0] == 0:
        _, status = await master.write(func_name="depositStake", gas_price=gas_price)
        assert status.ok

    time.sleep(20)

    query_data = HexBytes(bytes("how are you", 'utf-8'))
    query_id = Web3.keccak(hexstr=query_data.hex()).hex()
    print(query_data)
    print(query_id)

    value_count, status = await oracle.read(func_name="getTimestampCountById", _queryId=query_id)
    assert status.ok
    assert value_count >= 0
    print(value_count)
    value = HexBytes(bytes("Im doing fine", 'utf-8'))


    receipt, status = await oracle.write(
        func_name="submitValue",
        gas_price=gas_price,
        # extra_gas_price=20,
        # retries=1,
        _queryId=query_id,
        _value=value,
        _nonce=0,
        _queryData=query_data
    )

    print(status.error)
    assert status.ok

@pytest.mark.skip(reason="We should ensure contract is connected when instantiated.")
async def test_attempt_read_not_connected(cfg):
    """Read method should connect to contract if not connected"""
    address = "0x99548B9bda35AFad192c8209dB567a38b94b0940"
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
    status, output = await c.read(func_name=func_name, _requestId=requestId)
    assert status.ok
    assert output >= 0
