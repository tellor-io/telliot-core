""" Unit tests for static queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.query import ValueType
from telliot.queries.string_query import StringQuery


def test_static_query():

    """Test static query"""
    q = StringQuery(
        uid="qid-999",
        name="Fundamental Question",
        string="What is the meaning of life",
        static_response_type=ValueType(abi_type="string"),
    )

    assert q.tip_data == (
        b"StringQuery(string='What is the meaning of life')?"
        b"abi_type='string',packed=False"
    )

    response = q.value_type.encode(
        "Please refer to: https://en.wikipedia.org/wiki/Meaning_of_life"
    )
    assert isinstance(response, bytes)
