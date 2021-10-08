""" :mod:`telliot.queries.legacy_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import Any
from typing import Literal

from pydantic import Field
from pydantic import validator
from telliot.queries.price_query import price_types
from telliot.queries.query import OracleQuery
from telliot.response_type import ResponseType

# The default response type applicable to most legacy queries
default_legacy_response_type = ResponseType(abi_type="ufixed256x6", packed=False)


class LegacyQuery(OracleQuery):
    """Legacy Query

    Legacy queries are queries that existed prior to TellorX
    A legacy query uses static tip data and a static request ID.
    The request ID is always an integer less than 100.
    """

    type: str = Field("LegacyQuery", constant=True)

    #: The request ID of all legacy queries is a static integer 1 < N <=100
    legacy_request_id: int

    #: The question used by a legacy query (and submitted with tip data).
    #: Per the contract, this could be anything
    legacy_question: str

    #: The response type of the query, default for most legacy queries
    value_type: ResponseType = Field(default=default_legacy_response_type)

    @property
    def response_type(self) -> ResponseType:
        """Abstract method implementation."""
        return self.value_type

    @property
    def request_id(self) -> bytes:
        """Abstract method implementation."""
        return self.legacy_request_id.to_bytes(32, "big", signed=False)

    @property
    def question(self) -> str:
        """Abstract method implementation."""
        return self.legacy_question

    @validator("legacy_request_id")
    def must_be_less_than_100(cls, v):  # type: ignore
        """Ensure legacy request ID is valid"""
        if v is not None:
            if v > 100:
                raise ValueError("Legacy request ID must be less than 100")
        return v


class LegacyPriceQuery(LegacyQuery):
    type: Literal["LegacyPriceQuery"] = "LegacyPriceQuery"

    #: Asset symbol
    asset: str

    #: Price currency symbol
    currency: str

    #: Price Type
    price_type: price_types = "current"

    def __init__(self, **data: Any) -> None:

        # Handle deserialization when legacy_question is defined
        if "legacy_question" in data:
            legacy_question = data.pop("legacy_question")
        else:
            legacy_question = ""

        super().__init__(legacy_question=legacy_question, **data)

        question = (
            f"what is the {self.price_type} value of {self.asset}"
            f" in {self.currency} (warning:deprecated)"
        )

        if self.legacy_question:
            if self.legacy_question != question:
                raise ValueError("Unexpected question")
        else:
            self.legacy_question = question
