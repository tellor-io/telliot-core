""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = (
        b'{"type": "CoinPrice", '
        b'"inputs": '
        b'{"coin": "btc", "currency": "usd", "price_type": "current"}}?'
        b'{"type": "UnsignedFloatType", '
        b'"inputs": {"abi_type": "ufixed64x6", "packed": true}}'
    )

    print(q.tip_data)
    assert q.tip_data == exp

    exp = "0202f9d405bcee6f34f49deab26d448734fe0a4e6a1f61444851e1ee3f43ed3c"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b'{"type": "CoinPrice", '
        b'"inputs": '
        b'{"coin": "eth", "currency": "usd", "price_type": "24hr_twap"}}?'
        b'{"type": "UnsignedFloatType", '
        b'"inputs": {"abi_type": "ufixed64x6", "packed": true}}'
    )

    print(q.tip_data)
    assert q.tip_data == exp

    exp = "e38918373558af60b44db8b9bc69cec05c7a4fd185806d71ead6188300372158"
    assert q.tip_id.hex() == exp
