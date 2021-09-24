import os

from dotenv import load_dotenv
import pytest
import requests

from telliot.utils.eth_utils import RPCEndpoint

load_dotenv() #we will replace this with loading from config

def test_rpc_endpoint():
    url = os.getenv("NODE_URL")
    endpt = RPCEndpoint(url)
    endpt.connect()
    assert endpt.web3.eth.blockNumber > 1
    

def test_very_bad_rpc_url():
    url = "this is not a valid rpc url"
    endpt = RPCEndpoint(url)
    endpt.connect()
    #expect bad url error from requests library
    with pytest.raises(requests.exceptions.MissingSchema) as e_info:
        endpt.web3.eth.blockNumber

def test_incomplete_rpc_url():
    url = "https://eth-rinkeby.gateway.pokt.network/v1/lb/"
    endpt = RPCEndpoint(url)
    endpt.connect()
    #expect bad url error from requests library
    with pytest.raises(requests.exceptions.HTTPError) as e_info:
        endpt.web3.eth.blockNumber

def test_contract_connection():
    pass


def test_load_from_config():
    pass
