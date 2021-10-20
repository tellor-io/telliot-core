""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = (
        b'{"type":"CoinPrice",'
        b'"inputs":'
        b'{"coin":"btc","currency":"usd","price_type":"current"}}?'
        b'{"type":"UnsignedFloatType",'
        b'"inputs":{"abi_type":"ufixed64x6","packed":true}}'
    )

    print(q.tip_data)
    assert q.tip_data == exp

    exp = "1cb51cfbde0f6dddd03172ba0ea9e8d2e77a1beecc7edcb907bbd83311af9b53"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b'{"type":"CoinPrice",'
        b'"inputs":'
        b'{"coin":"eth","currency":"usd","price_type":"24hr_twap"}}?'
        b'{"type":"UnsignedFloatType",'
        b'"inputs":{"abi_type":"ufixed64x6","packed":true}}'
    )

    print(q.tip_data)
    assert q.tip_data == exp

    exp = "c7f37408fb3c59185abb27cb66b6299288927bb9b51f2db4ab1e0c42d71bbaf2"
    assert q.tip_id.hex() == exp
