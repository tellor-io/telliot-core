""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.price_query import PriceQuery


def test_constructor():
    """Validate price query"""
    q = PriceQuery(asset="BTC", currency="USD")

    exp = (
        b"qid-101?what is the current value of btc "
        b"in usd?abi_type=ufixed64x6,packed=true"
    )

    assert q.tip_data == exp

    exp = "58a476e45522ad46d48b17bdac8600bb63656435ee938f0d72990cc3007fb7ad"
    assert q.request_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = PriceQuery(asset="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b"qid-101?what is the 24hr_twap value of eth in usd?"
        b"abi_type=ufixed64x6,packed=true"
    )
    assert q.tip_data == exp

    exp = "c89db5d2c69b59e8a4260ad119dc1710683341a69d985437717b6b92aadd203e"
    assert q.request_id.hex() == exp
