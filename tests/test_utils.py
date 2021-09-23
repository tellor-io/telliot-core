import os

from dotenv import load_dotenv
import pytest

from telliot.utils.eth_utils import RPCEndpoint

load_dotenv() #we will replace this with loading from config

def test_rpc_endpoint():
    url = os.getenv("NODE_URL")
    endpt = RPCEndpoint(url)
    

def test_bad_rpc_url():
    url = "hi"
    with pytest.raises(Exception) as e_info:
        endpt = RPCEndpoint(url)


def test_load_from_config():
    pass
