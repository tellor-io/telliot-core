""" Price Query Class

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from typing import Any
from typing import Literal

from pydantic import Field
from pydantic import PrivateAttr
from telliot.queries.dynamic_query import DynamicQuery
from telliot.response_type import ResponseType

price_types = Literal["current", "eod", "24hr_twap", "1hr_twap", "custom", "manual"]

# Standard response type for price query
response_type = ResponseType(abi_type="ufixed64x6", packed=True)


class PriceQuery(DynamicQuery):
    """A dynamic query for the price of an asset in a specified currency."""

    type: str = Field("PriceQuery", constant=True)

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
        response_type = ResponseType(abi_type="ufixed64x6", packed=True)

        super().__init__(**kwargs)

        self._response_type = response_type

    @property
    def response_type(self) -> ResponseType:
        """Abstract method implementation."""
        return self._response_type

    @property
    def question(self) -> str:
        """Abstract method implementation."""

        q = (
            f"what is the {self.price_type} value of "
            f"{self.asset} in {self.currency}"
        )

        if self.check_parameters():
            return q
        else:
            return ""

    def check_parameters(self) -> bool:
        """Abstract method implementation."""

        if not self.price_type:
            return False
        if not self.asset:
            return False
        if not self.currency:
            return False
        return True
