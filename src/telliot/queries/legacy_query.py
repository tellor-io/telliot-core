""" :mod:`telliot.queries.legacy_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from pydantic import validator
from telliot.queries.query import OracleQuery
from telliot.types.float_type import UnsignedFloatType
from telliot.types.value_type import ValueType
from dataclasses import dataclass


@dataclass
class LegacyRequest(OracleQuery):
    """Legacy Price/Value request

    Legacy request are queries that existed prior to TellorX
    A legacy query uses arbitrary query ``data`` and a static query ``id``.
    The query ``id`` is always set to the legacy request ID, which is
    an integer less than 100.

    The LegacyQuery class is deprecated and should not be used by
    new projects.  Instead, use the
    [`CoinPrice`][telliot.queries.coin_price.CoinPrice]
    query or create a new query.

    Refer to [tellor documentation](https://docs.tellor.io/tellor/integration/data-ids)
    for a description of each ``id``

    """

    legacy_id: int
    """The request ID of all legacy queries is a static integer 1 < N <=100"""

    @property
    def value_type(self) -> ValueType:
        """Returns the Legacy Value Type for all legacy queries"""
        return UnsignedFloatType(abi_type="ufixed256x6", packed=False)

    @property
    def query_id(self) -> bytes:
        """Override query ``id`` with the legacy request ID."""
        return self.legacy_id.to_bytes(32, "big", signed=False)

    @validator("legacy_request_id")
    def must_be_less_than_100(cls, v):  # type: ignore
        """Validator to ensure that legacy request ID is less than
        or equal to 100.
        """
        if v is not None:
            if v > 100:
                raise ValueError("Legacy request ID must be less than 100")
        return v
