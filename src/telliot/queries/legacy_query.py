""" :mod:`telliot.queries.legacy_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from pydantic import validator
from telliot.queries.query import OracleQuery
from telliot.queries.value_type import ValueType

LegacyValueType = ValueType(abi_type="ufixed256x6", packed=False)


class LegacyQuery(OracleQuery):
    """Legacy Query

    Legacy queries are queries that existed prior to TellorX
    A legacy query uses arbitrary tip ``data`` and a static tip ``id``.
    The tip ``id`` is always an integer less than 100.

    The LegacyQuery class is deprecated and should not be used by
    new projects.  Instead, use the
    :class:`~telliot.queries.coin_price.CoinPrice` query or create
    a new query.

    Refer to tellor documentation for a description of each ``id``

    - https://docs.tellor.io/tellor/integration/data-ids


    """

    #: The request ID of all legacy queries is a static integer 1 < N <=100
    legacy_tip_id: int

    @property
    def value_type(self) -> ValueType:
        """Returns the Legacy Value Type for all legacy queries"""
        return LegacyValueType

    @property
    def tip_id(self) -> bytes:
        """Override tip ``id`` with the legacy value."""
        return self.legacy_tip_id.to_bytes(32, "big", signed=False)

    @validator("legacy_tip_id")
    def must_be_less_than_100(cls, v):  # type: ignore
        """Validator to ensure that legacy request ID is less than
        or equal to 100.
        """
        if v is not None:
            if v > 100:
                raise ValueError("Legacy request ID must be less than 100")
        return v
