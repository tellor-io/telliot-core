""" Unit tests for Legacy Queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot_core.queries.legacy_query import LegacyRequest


def test_legacy_query():
    """Validate legacy query"""
    q = LegacyRequest(
        legacy_id=100,
    )
    assert q.value_type.abi_type == "ufixed256x6"
    assert q.value_type.packed is False

    exp = b'{"type":"LegacyRequest","legacy_id":100}'

    # print(q.query_data)
    assert q.query_data == exp

    assert (
        q.query_id.hex()
        == "0000000000000000000000000000000000000000000000000000000000000064"
    )
