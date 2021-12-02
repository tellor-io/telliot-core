""" Unit tests for Legacy Queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot_core.queries.legacy_query import LegacyRequest


def test_legacy_ample_query():
    """Validate legacy query"""
    q = LegacyRequest(
        legacy_id=10,
    )
    assert q.value_type.abi_type == "ufixed256x18"
    assert q.value_type.packed is False

    exp = b'{"type":"LegacyRequest","legacy_id":10}'

    # print(q.query_data)
    assert q.query_data == exp

    assert (
        q.query_id.hex()
        == "000000000000000000000000000000000000000000000000000000000000000a"
    )

    assert (
        q.value_type.encode(116.7).hex()
        == "0000000000000000000000000000000000000000000000065389afb268160b1a"
    )
