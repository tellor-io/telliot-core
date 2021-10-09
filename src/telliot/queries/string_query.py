""" :mod:`telliot.queries.string`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import ClassVar
from typing import List

from telliot.queries.query import OracleQuery
from telliot.response_type import ResponseType


class StringQuery(OracleQuery):
    """Static Oracle Query

    A string query supports a question in the form of an arbitrary
    string.
    """

    parameters: ClassVar[List[str]] = ["string"]

    #: Static query string
    string: str

    #: Static response type
    static_response_type: ResponseType

    @property
    def response_type(self) -> ResponseType:
        """Returns the static response type."""
        return self.static_response_type
