"""
Tests covering Pytelliot rpc connection  utils.
"""
import pytest
import requests

from telliot_core.model.endpoints import EndpointList
from telliot_core.model.endpoints import RPCEndpoint

network = "mainnet"
provider = "pokt"


def test_rpc_endpoint():
    """RPCEndpoint connects to the blockchain"""
    url = "https://mainnet.infura.io/v3/1a09c4705f114af2997548dd901d655b"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    endpt.connect()
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
    url = "https://eth-rinkeby.gateway.pokt.network/v1/lb/"
    endpt = RPCEndpoint(network=network, provider=provider, url=url)
    # expect bad url error from requests library
    with pytest.raises(requests.exceptions.HTTPError):
        _ = endpt.connect()


def test_endpoint_list():
    sl = EndpointList()
    # print(json.dumps(sl.get_state(), indent=2))
    ep4 = sl.get_chain_endpoint(4)
    assert ep4.network == "rinkeby"
