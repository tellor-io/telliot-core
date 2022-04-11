# import secrets
import pytest
from brownie import accounts
from brownie import chain
from brownie import StakingToken
from brownie import TellorFlex

# from chained_accounts import ChainedAccount
# from chained_accounts import find_accounts
# from web3 import Web3

# from telliot_core.apps.telliot_config import TelliotConfig

# from eth_utils import to_checksum_address


# if not test_acct.is_unlocked:
#             test_acct.unlock("")


def test_connect_local_web3(local_cfg):
    # w3 = Web3(Web3.WebsocketProvider('wss://127.0.0.1:8545'))
    #
    # w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545"))
    endpoint = local_cfg.get_endpoint()
    assert endpoint is not None
    chain.mine(10)
    assert endpoint.url == "http://127.0.0.1:8545"
    endpoint.connect()
    block = endpoint._web3.eth.get_block("latest")
    # block = endpoint.web3.eth.get_block('latest')
    # block = w3.eth.get_block("latest")

    # assert w3.isConnected()
    assert block.number == 10
    pass


@pytest.fixture
def trb():  # Tellor Tributes (TRB)
    return accounts[0].deploy(StakingToken)


@pytest.fixture
def tellor_flex(trb):
    return accounts[0].deploy(TellorFlex, trb.address)


def test_mint_test_token(trb):
    trb.mint(accounts[0], 1000, {"from": accounts[0]})

    assert trb.balanceOf(accounts[0]) == 1000


# def test_approve(trb):
#     trb.approve(accounts[1], 100, {'from': accounts[0]})
#     assert trb.allowance(accounts[0], accounts[1]) == 100
