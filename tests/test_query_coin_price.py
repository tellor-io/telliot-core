""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = (
        b"CoinPrice(coin='btc',currency='usd',price_type='current')?"
        b"abi_type='ufixed64x6',packed=True"
    )

    assert q.tip_data == exp

    exp = "fb4247810138c3cc5c53f70e0aa53eb1854bb12cbf828a1e3298b4a24f237780"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b"CoinPrice(coin='eth',currency='usd',price_type='24hr_twap')?"
        b"abi_type='ufixed64x6',packed=True"
    )

    assert q.tip_data == exp
    print(q.tip_data)

    exp = "cbcc7a822c0c5225aac4cdb9f3c368f4aa15da8b11c3f5829476453381fd3475"
    assert q.tip_id.hex() == exp
