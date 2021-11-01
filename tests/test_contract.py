"""
Test covering Pytelliot EVM contract connection utils.
"""
import time

import pytest
import web3
from hexbytes.main import HexBytes
from telliot.contract.gas import fetch_gas_price
from web3 import Web3


def test_connect_to_tellor(cfg, master):
    """Contract object should access Tellor functions"""
    assert len(master.contract.all_functions()) > 0
    assert isinstance(
        master.contract.all_functions()[0], web3.contract.ContractFunction
    )


@pytest.mark.skip(reason="for playground.")
@pytest.mark.asyncio
async def test_call_read_function(cfg, master):
    """Contract object should be able to call arbitrary contract read function"""

    output, status = await master.read(
        func_name="getTimestampCountById", _queryId=Web3.keccak(HexBytes(2))
    )
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
    print("my sender address:", sender)
    print("my sender balance:", balance / 1e18)
    recipient = str(
        Web3.toChecksumAddress("0xf3428C75CAfb3FBA46D3E190B7539Fbbfb96f244")
    )

    balance, status = await master.read("balanceOf", _user=recipient)
    assert status.ok
    print("before:", balance / 1e18)

    receipt, status = await master.write(
        "transfer", _to=recipient, _amount=1, gas_price=gas_price
    )
    print(status.error)
    assert status.ok

    balance, status = await master.read("balanceOf", _user=recipient)
    print("after:", balance / 1e18)


@pytest.mark.asyncio
async def test_submit_value(cfg, master, oracle):
    """E2E test for submitting a value to rinkeby"""

    gas_price = await fetch_gas_price()
    user = master.node.web3.eth.account.from_key(cfg.main.private_key).address
    print(user)

    balance, status = await master.read("balanceOf", _user=user)
    print(balance / 1e18)

    is_staked, status = await master.read("getStakerInfo", _staker=user)
    print(is_staked)

    if is_staked[0] == 0:
        _, status = await master.write(func_name="depositStake", gas_price=gas_price)
        assert status.ok

    time.sleep(20)

    query_data = HexBytes(bytes("how are you", "utf-8"))
    query_id = Web3.keccak(hexstr=query_data.hex()).hex()
    print(query_data)
    print(query_id)

    value_count, status = await oracle.read(
        func_name="getTimestampCountById", _queryId=query_id
    )
    assert status.ok
    assert value_count >= 0
    print(value_count)
    value = HexBytes(bytes("Im doing fine", "utf-8"))

    receipt, status = await oracle.write(
        func_name="submitValue",
        gas_price=gas_price,
        # extra_gas_price=20,
        # retries=1,
        _queryId=query_id,
        _value=value,
        _nonce=0,
        _queryData=query_data,
    )

    print(status.error)
    assert status.ok
