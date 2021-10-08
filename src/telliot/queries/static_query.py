""" :mod:`telliot.queries.static_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from pydantic import Field
from telliot.queries.query import OracleQuery
from telliot.response_type import ResponseType
from web3 import Web3


class StaticQuery(OracleQuery):
    """Static Oracle Query

    A static query uses a fixed value for addTip ``data``.
    The addTip ``id`` is also fixed according the keccak algorithm.
    """

    type: str = Field("StaticQuery", constant=True)

    #: Static query string
    static_query: str

    #: Static response type
    static_response_type: ResponseType

    @property
    def response_type(self) -> ResponseType:
        """Returns the static response type."""
        return self.static_response_type

    @property
    def request_id(self) -> bytes:
        """Compute and return the request ID."""
        return bytes(Web3.keccak(self.tip_data))

    @property
    def query(self) -> str:
        """Returns the static query"""
        return self.static_query
