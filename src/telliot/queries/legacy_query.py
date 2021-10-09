""" :mod:`telliot.queries.legacy_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import ClassVar
from typing import List

from pydantic import validator
from telliot.queries.query import OracleQuery
from telliot.response_type import ResponseType


class LegacyQuery(OracleQuery):
    """Legacy Query

    Legacy queries are queries that existed prior to TellorX
    A legacy query uses static tip data and a static request ID.
    The request ID is always an integer less than 100.
    """

    parameters: ClassVar[List[str]] = ["legacy_tip_id"]

    #: The request ID of all legacy queries is a static integer 1 < N <=100
    legacy_tip_id: int

    @property
    def response_type(self) -> ResponseType:
        """ All legacy queries

        """
        return ResponseType(abi_type="ufixed256x6", packed=False)

    @property
    def tip_id(self) -> bytes:
        """Override tip ``id`` with the legacy value."""
        return self.legacy_tip_id.to_bytes(32, "big", signed=False)

    @validator("legacy_tip_id")
    def must_be_less_than_100(cls, v):  # type: ignore
        """Ensure legacy request ID is valid"""
        if v is not None:
            if v > 100:
                raise ValueError("Legacy request ID must be less than 100")
        return v
