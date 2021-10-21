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
from telliot.types.float_type import UnsignedFloatType
from telliot.types.value_type import ValueType

price_types = Literal["current", "eod", "24hr_twap", "1hr_twap", "custom", "manual"]


# List of inputs used to customize a CoinPrice object
price_query_params = ["coin", "currency", "price_type"]


class CoinPrice(OracleQuery):
    """Query the price of a cryptocurrency coin.

    Attributes:
        coin: Token symbol
        currency: Price currency symbol (default = USD)
        price_type: Price Type (default = current)

    """

    inputs: ClassVar[List[str]] = price_query_params

    coin: str = ""

    currency: str = "usd"

    price_type: price_types = "current"

    #: Private storage for response_type
    _value_type: ValueType = PrivateAttr()

    def __init__(self, **kwargs: Any):
        # Fixed response type for all queries

        super().__init__(**kwargs)

        self._value_type = UnsignedFloatType(abi_type="ufixed64x6", packed=True)

    @property
    def value_type(self) -> ValueType:
        """Returns the fixed value type for a CoinPrice."""
        return self._value_type

    @validator("coin")
    def asset_must_be_lower_case(cls, v: str) -> str:
        """A validator to force coin to lower case"""
        return v.lower()

    @validator("currency")
    def currency_must_be_lower_case(cls, v: str) -> str:
        """A validator to force the currency lower case"""
        return v.lower()


if __name__ == "__main__":
    """CoinPrice Example."""

    q = CoinPrice(coin="btc")
    print(q.__repr__())

    print(q.tip_data)
    print("0x" + q.tip_id.hex())
