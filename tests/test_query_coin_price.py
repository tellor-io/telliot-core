""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.coin_price import CoinPrice
from telliot.queries.coin_price import CoinPriceValue


def test_constructor():
    """Validate price query"""
    q = CoinPrice(coin="BTC", currency="USD")

    exp = (
        b"CoinPrice(coin='btc', currency='usd', price_type='current')?"
        b"CoinPriceValue(abi_type='ufixed64x6', packed=True)"
    )

    assert q.tip_data == exp

    exp = "5f01defef41c0e66adefd7637657c13c7a8f415233d817a51a83e6bc517b33ef"
    assert q.tip_id.hex() == exp


def test_price_type():
    """Validate price_type setting"""
    q = CoinPrice(coin="ETH", currency="USD", price_type="24hr_twap")

    exp = (
        b"CoinPrice(coin='eth', currency='usd', price_type='24hr_twap')?"
        b"CoinPriceValue(abi_type='ufixed64x6', packed=True)"
    )

    assert q.tip_data == exp

    exp = "f24a500b7e59df12c2dd9c158b55f28c6fb417f3eb5ad935648509803f5fac84"
    assert q.tip_id.hex() == exp


def test_value_type():
    """Test CoinPrice Value Type coding/decoding"""

    decimals = 6

    value = 99.9

    r1 = CoinPriceValue()
    bytes_val = r1.encode(value)
    assert bytes_val.hex() == "0000000005f45a60"

    int_val = int.from_bytes(bytes_val, "big", signed=False)
    assert int_val == value * 10 ** decimals

    decoded = r1.decode(bytes_val)
    print(decoded)
    assert decoded == value
