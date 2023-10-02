"""
Tests covering Pytelliot rpc connection  utils.
"""
import pytest
from brownie import chain
from requests.exceptions import ConnectionError
from requests.exceptions import HTTPError

from telliot_core.model.endpoints import EndpointList
from telliot_core.model.endpoints import RPCEndpoint

network = "mainnet"
provider = "pokt"


def test_rpc_endpoint():
    """RPCEndpoint connects to the blockchain"""
    url = "http://127.0.0.1:8545"  # local Ganache node
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()
    chain.mine(10)
    assert endpt.web3.eth.block_number > 1

    print(endpt.get_state())


def test_very_bad_rpc_url():
    """an invalid url will raise an exception in RPCEndpoint"""
    url = "this is not a valid rpc url"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    with pytest.raises(ValueError):
        _ = endpt.connect()


def test_incomplete_rpc_url():
    """an incomplete url will raise an exception in RPCEndpoint"""
    url = "https://eth-rpc.gateway.pokt.networ/"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    try:
        _ = endpt.connect()
    except HTTPError:
        pass  # expected
    except ConnectionError:
        pass  # expected
    except ValueError as e:
        assert "Invalid request path" in str(e)
    else:
        pytest.fail("Expected ValueError or HTTPError.")


def test_endpoint_list():
    sl = EndpointList()
    # print(json.dumps(sl.get_state(), indent=2))
    ep11155111 = sl.find(chain_id=11155111)[0]
    assert ep11155111.network == "sepolia"
