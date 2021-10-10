""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = (
        b"CoinPrice(coin='btc', currency='usd', price_type='current')?"
        b"ValueType(abi_type='ufixed64x6', packed=True)"
    )

    assert q.tip_data == exp

    exp = "df872ce15bdfe08ca4f3862bc7a3381deb1a1c33f0fa6fff9c5c4f902f4d2062"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b"CoinPrice(coin='eth', currency='usd', price_type='24hr_twap')?"
        b"ValueType(abi_type='ufixed64x6', packed=True)"
    )

    assert q.tip_data == exp

    exp = "2ca3ad01b0746a57aa4005af40e0c70e26841b2d0c6da9291ee365c5f157e81c"
    assert q.tip_id.hex() == exp
