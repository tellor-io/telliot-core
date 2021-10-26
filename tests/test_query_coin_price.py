""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = b'["CoinPrice",{"coin":"BTC","currency":"USD","price_type":"current"}]'

    print(q.query_data)
    assert q.query_data == exp

    exp = "c09f8e5a2f8b0eb295d9f2fff14f3330f9b89259da98ce25b31c8231e2a7f323"
    assert q.query_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = b'["CoinPrice",{"coin":"ETH","currency":"USD","price_type":"24hr_twap"}]'

    print(q.query_data)
    assert q.query_data == exp

    exp = "ce19ecb1561a93f444c9453aa6a8bbab7ebf8a74bfdbcb727340437f475fa621"
    assert q.query_id.hex() == exp
