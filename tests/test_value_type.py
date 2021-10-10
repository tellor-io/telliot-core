""" Unit tests for response type

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from decimal import Decimal

import pytest
from eth_abi.exceptions import InsufficientDataBytes
from telliot.queries.value_type import ValueType


def test_fixed_response_type():
    """Demonstrate encoding a fixed value with precision=9"""
    value = Decimal("1.0")
    r1 = ValueType(abi_type="ufixed256x9", packed=False)
    bytes_val = r1.encode(value)
    assert (
        bytes_val.hex()
        == "000000000000000000000000000000000000000000000000000000003b9aca00"
    )
    int_val = int.from_bytes(bytes_val, "big", signed=False)
    assert int_val == 10 ** 9


def test_dynamic_response_type_unpacked():
    """Demonstrate a complex response to a query"""
    r1 = ValueType(abi_type="(int8,bytes,ufixed32x9,bool[])[2]", packed=False)

    value = ((1, b"abc", 1, (True, True)), (1, b"def", 1, (True, True)))

    bytes_val = r1.encode(value)
    print(bytes_val.hex())

    decoded = r1.decode(bytes_val)

    assert decoded == value


def test_packed_response_type_FAILS():
    """Demonstrate encoding a fixed value with precision=9

    This test demonstrates that a custom decoder is required for
    packed values
    """
    value = Decimal("1.0")
    r1 = ValueType(abi_type="ufixed64x9", packed=True)
    bytes_val = r1.encode(value)
    assert bytes_val.hex() == "000000003b9aca00"
    int_val = int.from_bytes(bytes_val, "big", signed=False)
    assert int_val == 10 ** 9

    with pytest.raises(InsufficientDataBytes):
        decoded = r1.decode(bytes_val)
        print(decoded)
