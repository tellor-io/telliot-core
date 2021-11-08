'''Submits three month rolling average of the USPCE to TellorX on Rinkeby.'''
import web3
from hexbytes.main import HexBytes
from telliot.contract.gas import fetch_gas_price
from telliot.queries.legacy_query import LegacyRequest
from web3 import Web3
import os

import pytest
from telliot.apps.telliot_config import TelliotConfig
from telliot.contract.contract import Contract
from telliot.utils.abi import rinkeby_tellor_master
from telliot.utils.abi import rinkeby_tellor_oracle
from dotenv import load_dotenv
import asyncio

load_dotenv()

def get_cfg():
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
        # cfg.main.private_key = os.environ["PRIVATE_KEY"]
        cfg.main.private_key = os.getenv("PRIVATE_KEY")


    if os.getenv("NODE_URL", None):
        # rinkeby_endpoint.url = os.environ["NODE_URL"]
        rinkeby_endpoint.url = os.getenv("NODE_URL")

    return cfg


def get_master(cfg):
    """Helper function for connecting to a contract at an address"""
    endpoint = cfg.get_endpoint()
    endpoint.connect()
    master = Contract(
        address="0x657b95c228A5de81cdc3F85be7954072c08A6042",
        abi=rinkeby_tellor_master,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    master.connect()
    return master


def get_oracle(cfg):
    """Helper function for connecting to a contract at an address"""
    endpoint = cfg.get_endpoint()
    endpoint.connect()
    oracle = Contract(
        address="0x07b521108788C6fD79F471D603A2594576D47477",
        abi=rinkeby_tellor_oracle,
        node=endpoint,
        private_key=cfg.main.private_key,
    )
    oracle.connect()
    return oracle


def parse_user_val():
    print('Enter USPCE value (example: 13659.3:')

    uspce = None

    while uspce is None:
        inpt = input()

        try:
            inpt = int(float(inpt) * 1000000)
        except ValueError:
            print('Invalid input. Enter int or float.')
            continue

        _ = input(f'Submitting value: {inpt}\nPress [ENTER] to confirm.')

        uspce = inpt

    # print success/fail & rinkebyscan link
    # print(f'Success. See here: {uspce}')
    return uspce


async def submit():
    cfg = get_cfg()
    master = get_master(cfg)
    oracle = get_oracle(cfg)

    gas_price =  await fetch_gas_price()  # TODO clarify gas price units
    user = master.node.web3.eth.account.from_key(cfg.main.private_key).address
    print(user)

    balance, status = await master.read("balanceOf", _user=user)
    print(balance / 1e18)

    is_staked, status = await master.read("getStakerInfo", _staker=user)
    print(is_staked)

    if is_staked[0] == 0:
        _, status = await master.write_with_retry(
            func_name="depositStake", gas_price=gas_price, extra_gas_price=20, retries=2
        )
        assert status.ok

    q = LegacyRequest(legacy_id=41)
    usr_input = parse_user_val()
    value = q.value_type.encode(usr_input)

    query_data = q.query_data
    query_id = q.query_id

    value_count, status = await oracle.read(
        func_name="getTimestampCountById", _queryId=query_id
    )
    assert status.ok
    assert value_count >= 0
    print(value_count)

    _, status = await oracle.write_with_retry(
        func_name="submitValue",
        gas_price=gas_price,
        extra_gas_price=40,
        retries=5,
        _queryId=query_id,
        _value=value,
        _nonce=value_count,
        _queryData=query_data,
    )

    print(status.error)
    assert status.ok


if __name__ == "__main__":
    asyncio.run(submit())