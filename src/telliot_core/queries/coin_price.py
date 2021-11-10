""" :mod:`telliot_core.queries.price_query`

"""
from dataclasses import dataclass
from typing import Literal

from telliot_core.queries.query import OracleQuery
from telliot_core.types.float_type import UnsignedFloatType
from telliot_core.types.value_type import ValueType

price_types = Literal["current", "eod", "24hr_twap", "1hr_twap"]

# List of inputs used to customize a CoinPrice object
price_query_params = ["coin", "currency", "price_type"]


@dataclass
class CoinPrice(OracleQuery):
    """Query the price of a cryptocurrency coin. **PROTOTYPE: DO NOT USE**

    Attributes:
        coin: Token symbol
        currency: Price currency symbol (default = USD)
        price_type: Price Type (default = current)

    """

    coin: str = ""

    currency: str = "usd"

    price_type: price_types = "current"

    @property
    def value_type(self) -> ValueType:
        """Returns the fixed value type for a CoinPrice."""
        return UnsignedFloatType(abi_type="ufixed64x6", packed=True)


if __name__ == "__main__":
    """CoinPrice Example."""

    q = CoinPrice(coin="btc")
    print(q.__repr__())

    print(q.query_data)
    print("0x" + q.query_id.hex())
