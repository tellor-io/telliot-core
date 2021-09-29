"""
Tests covering Pytelliot ethereum connection utils.
"""
import os

import pytest
import requests
import web3
from dotenv import load_dotenv
from telliot.utils.rpc_endpoint import Contract
from telliot.utils.rpc_endpoint import RPCEndpoint

load_dotenv()  # we will replace this with loading from config

with open("abi.json") as f:
    abi = f.read()

network = "mainnet"
provider = "pokt"


def test_rpc_endpoint():
    """RPCEndpoint connects to the blockchain"""
    url = "https://mainnet.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()
    assert endpt.web3.eth.block_number > 1


def test_very_bad_rpc_url():
    """an invalid url will raise an exception in RPCEndpoint"""
    url = "this is not a valid rpc url"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()
    # expect bad url error from requests library
    with pytest.raises(requests.exceptions.MissingSchema) as e_info:
        endpt.web3.eth.blockNumber


def test_incomplete_rpc_url():
    """an incomplete url will raise an exception in RPCEndpoint"""
    url = "https://eth-rinkeby.gateway.pokt.network/v1/lb/"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()
    # expect bad url error from requests library
    with pytest.raises(requests.exceptions.HTTPError) as e_info:
        endpt.web3.eth.blockNumber


def test_read_tellor_playground():
    """Contract object should access Tellor Playground functions"""
    contract = connect_to_contract("0x4699845F22CA2705449CFD532060e04abE3F1F31")
    assert len(contract.Contract.all_functions()) > 0
    assert isinstance(
        contract.Contract.all_functions()[0], web3.contract.ContractFunction
    )


def test_load_from_config():
    """RPCEndpoint should read from config.yml"""
    pass


def connect_to_contract(address):
    """Helper function for connecting to a contract at an address"""
    url = "https://mainnet.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()

    c = Contract(endpt, address, abi)
    c.connect()
    return c
