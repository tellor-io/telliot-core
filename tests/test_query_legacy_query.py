""" Unit tests for Legacy Queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.legacy_query import LegacyQuery


def test_legacy_query():
    """Validate legacy query"""
    q = LegacyQuery(
        legacy_tip_id=100,
    )
    assert q.value_type.abi_type == "ufixed256x6"
    assert q.value_type.packed is False

    exp = (
        b"LegacyQuery(legacy_tip_id=100)?"
        b"LegacyValueType(abi_type='ufixed256x6', packed=False)"
    )

    assert q.tip_data == exp

    assert (
        q.tip_id.hex()
        == "0000000000000000000000000000000000000000000000000000000000000064"
    )
