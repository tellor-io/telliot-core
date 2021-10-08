""" Unit tests for Legacy Queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.legacy_query import LegacyPriceQuery
from telliot.queries.legacy_query import LegacyQuery


def test_legacy_query():
    """Validate legacy query"""
    q = LegacyQuery(
        uid="qid-100",
        name="name",
        legacy_tip_id=100,
        legacy_query=b"legacy question",
    )
    assert q.response_type.abi_type == "ufixed256x6"
    assert q.response_type.packed is False
    assert (
        q.tip_id.hex()
        == "0000000000000000000000000000000000000000000000000000000000000064"
    )
    assert q.tip_data == b"qid-100?legacy question?abi_type=ufixed256x6,packed=false"


def test_legacy_price_query():
    """Test legacy price query"""
    q = LegacyPriceQuery(
        name="BTC/USD Current Price",
        uid="qid-99",
        legacy_tip_id=99,
        asset="btc",
        currency="usd",
        price_type="current",
    )

    exp = (
        b"qid-99?what is the current value of btc in usd "
        b"(warning:deprecated)?abi_type=ufixed256x6,packed=false"
    )
    assert q.tip_data == exp

    exp = "0000000000000000000000000000000000000000000000000000000000000063"
    assert q.tip_id.hex() == exp
