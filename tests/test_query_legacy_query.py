""" Unit tests for Legacy Queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.legacy_query import LegacyQuery


def test_legacy_query():
    """Validate legacy query"""
    q = LegacyQuery(
        uid="qid-100",
        name="name",
        legacy_tip_id=100,
    )
    assert q.response_type.abi_type == "ufixed256x6"
    assert q.response_type.packed is False

    assert q.tip_data == b"LegacyQuery(legacy_tip_id=100)?abi_type='ufixed256x6',packed=False"

    assert (
        q.tip_id.hex()
        == "0000000000000000000000000000000000000000000000000000000000000064"
    )


