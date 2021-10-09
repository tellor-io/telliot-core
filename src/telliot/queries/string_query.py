""" :mod:`telliot.queries.string`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import ClassVar
from typing import List

from telliot.queries.query import OracleQuery
from telliot.queries.value_type import ValueType


class StringQuery(OracleQuery):
    """Static Oracle Query

    A string query supports a question in the form of an arbitrary
    string.
    """

    inputs: ClassVar[List[str]] = ["string"]

    #: Static query string
    string: str

    #: Static response type
    static_response_type: ValueType

    @property
    def value_type(self) -> ValueType:
        """Returns the static response type."""
        return self.static_response_type
