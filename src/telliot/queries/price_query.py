""" :mod:`telliot.queries.price_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import Any
from typing import ClassVar
from typing import List
from typing import Literal

from pydantic import Field
from pydantic import PrivateAttr
from pydantic import validator
from telliot.queries.query import OracleQuery
from telliot.response_type import ResponseType

price_types = Literal["current", "eod", "24hr_twap", "1hr_twap", "custom", "manual"]

# Standard response type for price query
response_type = ResponseType(abi_type="ufixed64x6", packed=True)

# List of parameters used to customize a PriceQuery object
price_query_params = ["asset", "currency", "price_type"]


class PriceQuery(OracleQuery):
    """A dynamic query for the price of an asset in a specified currency."""

    parameters: ClassVar[List[str]] = price_query_params

    name: str = Field("Price Query", constant=True)

    uid: str = Field("qid-101", constant=True)

    #: Asset symbol
    asset: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Type
    price_type: price_types = "current"

    #: Private storage for response_type
    _response_type: ResponseType = PrivateAttr()

    def __init__(self, **kwargs: Any):
        # Fixed response type for all queries
        fixed_rtype = ResponseType(abi_type="ufixed64x6", packed=True)

        super().__init__(**kwargs)

        self._response_type = fixed_rtype

    @property
    def response_type(self) -> ResponseType:
        """Abstract method implementation."""
        return self._response_type

    @validator("asset")
    def asset_must_be_lower_case(cls, v: str) -> str:
        """Ensure asset/currency are lower case"""
        return v.lower()

    @validator("currency")
    def currency_must_be_lower_case(cls, v: str) -> str:
        """Ensure asset/currency are lower case"""
        return v.lower()
