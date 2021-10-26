""" :mod:`telliot.queries.string_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from telliot.queries.query import OracleQuery
from telliot.types.value_type import ValueType
from dataclasses import dataclass


@dataclass
class StringQuery(OracleQuery):
    """Static Oracle Query

    A text query supports a question in the form of an arbitrary
    text.
    """

    #: Static query text
    text: str

    @property
    def value_type(self) -> ValueType:
        """Returns a default text response type."""
        return ValueType(abi_type="string", packed=False)
