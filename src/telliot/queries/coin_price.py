""" :mod:`telliot.queries.price_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from typing import Any
from typing import ClassVar
from typing import List
from typing import Literal

from pydantic import PrivateAttr
from pydantic import validator
from telliot.queries.query import OracleQuery
from telliot.queries.value_type import ValueType

price_types = Literal["current", "eod", "24hr_twap", "1hr_twap", "custom", "manual"]

# Standard response type for price query
response_type = ValueType(abi_type="ufixed64x6", packed=True)

# List of inputs used to customize a CoinPrice object
price_query_params = ["coin", "currency", "price_type"]


class CoinPrice(OracleQuery):
    """Query the price of a cryptocurrency coin."""

    inputs: ClassVar[List[str]] = price_query_params

    #: Asset symbol
    coin: str = ""

    #: Price currency symbol
    currency: str = ""

    #: Price Type
    price_type: price_types = "current"

    #: Private storage for response_type
    _response_type: ValueType = PrivateAttr()

    def __init__(self, **kwargs: Any):
        # Fixed response type for all queries
        fixed_rtype = ValueType(abi_type="ufixed64x6", packed=True)

        super().__init__(**kwargs)

        self._response_type = fixed_rtype

    @property
    def value_type(self) -> ValueType:
        """Abstract method implementation."""
        return self._response_type

    @validator("coin")
    def asset_must_be_lower_case(cls, v: str) -> str:
        """Ensure coin/currency are lower case"""
        return v.lower()

    @validator("currency")
    def currency_must_be_lower_case(cls, v: str) -> str:
        """Ensure coin/currency are lower case"""
        return v.lower()
