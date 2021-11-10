""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot_core.queries.coin_price import CoinPrice


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    # exp = b'["CoinPrice",{"coin":"BTC","currency":"USD","price_type":"current"}]'
    exp = b'{"type":"CoinPrice","coin":"BTC","currency":"USD","price_type":"current"}'

    print(q.query_data)
    assert q.query_data == exp

    exp = "c6bc01753088c82583c6e011d736314e4548c05052908cd63b4207b78fbc6f40"
    assert q.query_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = b'{"type":"CoinPrice","coin":"ETH","currency":"USD","price_type":"24hr_twap"}'

    print(q.query_data)
    assert q.query_data == exp

    exp = "055367425f0ea7d0f53cdbe7f782ae348d2c721a26734da5f3c612f090e6262e"
    assert q.query_id.hex() == exp
