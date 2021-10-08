""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.price_query import PriceQuery


def test_constructor():
    """Validate price query"""
    q = PriceQuery(asset="BTC", currency="USD")

    exp = (
        b"PriceQuery(asset='btc',currency='usd',price_type='current')?"
        b"abi_type='ufixed64x6',packed=True")

    assert q.tip_data == exp

    exp = "067301891b463794433b722e176d8dac5e3e5e8152342ca85212dd562ac8128c"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = PriceQuery(asset="ETH", currency="USD", price_type="24hr_twap")

    exp =(b"PriceQuery(asset='eth',currency='usd',price_type='24hr_twap')?"
          b"abi_type='ufixed64x6',packed=True")

    assert q.tip_data == exp
    print(q.tip_data)

    exp = "3b78e54622a770904d047cbb72a7fff611a3561eebc86a4922c3e4a6d1d237cb"
    assert q.tip_id.hex() == exp
