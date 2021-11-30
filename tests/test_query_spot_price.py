""" Unit tests for modern price queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
import pytest

from telliot_core.queries.price.spot_price import SpotPrice


def test_constructor():
    """Validate spot price query"""
    q = SpotPrice(asset="btc", currency="USD")

    exp = b'{"type":"SpotPrice","asset":"btc","currency":"usd"}'

    print(q.query_data)
    assert q.query_data == exp

    exp = "d66b36afdec822c56014e56f468dee7c7b082ed873aba0f7663ec7c6f25d2c0a"
    assert q.query_id.hex() == exp


def test_invalid_currency():
    with pytest.raises(ValueError):
        _ = SpotPrice(asset="btc", currency="xxx")


def test_invalid_pair():

    with pytest.raises(ValueError):
        _ = SpotPrice(asset="xxx", currency="usd")
