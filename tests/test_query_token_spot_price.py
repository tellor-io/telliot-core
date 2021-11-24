""" Unit tests for ERC-20 spot prices

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot_core.queries.token_spot_price import TokenSpotPrice

TRB_address = "0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0"


def test_erc20_spot_price_usd():
    """Validate price query"""

    q = TokenSpotPrice(address=TRB_address, chain_id=1, currency="usd")

    exp = (
        b'{"type":"TokenSpotPrice",'
        b'"address":"0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",'
        b'"chain_id":1,"currency":"usd"}'
    )

    print(q.query_data)
    assert q.query_data == exp

    exp = "c83928d2035b30eb2ed0fa81b1dd45051360813e46f6a91fcdefe11a0653250c"
    assert q.query_id.hex() == exp


def test_erc20_spot_price_eth():
    """Validate price_type setting"""
    q = TokenSpotPrice(address=TRB_address, chain_id=1, currency="native")

    exp = (
        b'{"type":"TokenSpotPrice",'
        b'"address":"0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",'
        b'"chain_id":1,"currency":"native"}'
    )

    print(q.query_data)
    assert q.query_data == exp

    exp = "b77c3f01bfbf486f4bdc5e5aae007ebbdaf47dc7cb0572d6a2cc473ad957f69a"
    assert q.query_id.hex() == exp
