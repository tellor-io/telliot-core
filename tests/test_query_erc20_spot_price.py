""" Unit tests for ERC-20 spot prices

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot_core.queries.erc20spot import ERC20SpotPrice

TRB_address = "0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0"


def test_erc20_spot_price_usd():
    """Validate price query"""

    q = ERC20SpotPrice(address=TRB_address, chain_id=1, currency="usd")

    exp = (
        b'{"type":"ERC20SpotPrice",'
        b'"address":"0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",'
        b'"chain_id":1,"currency":"usd"}'
    )

    print(q.query_data)
    assert q.query_data == exp

    exp = "2c8932428647ecc49f97a319c2ebfc2f6e667cf8ee0e96d9eb1ebf1dbb777492"
    assert q.query_id.hex() == exp


def test_erc20_spot_price_eth():
    """Validate price_type setting"""
    q = ERC20SpotPrice(address=TRB_address, chain_id=1, currency="native")

    exp = (
        b'{"type":"ERC20SpotPrice",'
        b'"address":"0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0",'
        b'"chain_id":1,"currency":"native"}'
    )

    print(q.query_data)
    assert q.query_data == exp

    exp = "a5e36e716292c57ff85d462666fa9064f2dd7f0f169cfb771d4b2c23c26ab944"
    assert q.query_id.hex() == exp
