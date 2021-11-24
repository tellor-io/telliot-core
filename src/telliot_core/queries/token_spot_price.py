""" ERC-20 Spot Price Queries

"""
from dataclasses import dataclass
from typing import Literal

from telliot_core.queries.query import OracleQuery
from telliot_core.types.float_type import UnsignedFloatType
from telliot_core.types.value_type import ValueType


@dataclass
class TokenSpotPrice(OracleQuery):
    """Query the price of an ERC-20 token in US Dollars

    Attributes:
        address: Token contract address
        chain_id: Token chain ID
        currency: Selected currency
            'native': returns the price in the native currency of the chain
              (e.g. ETH for chain_id = 1)
            'usd': returns the price in USD

    """

    address: str

    chain_id: int

    currency: Literal["native", "usd"]

    @property
    def value_type(self) -> ValueType:
        """Returns the response value type for a TokenSpotPrice query."""
        return UnsignedFloatType(abi_type="ufixed256x18", packed=True)


if __name__ == "__main__":
    """ERC20SpotPriceUSD Example."""

    TRB_address = "0x88df592f8eb5d7bd38bfef7deb0fbc02cf3778a0"

    q = TokenSpotPrice(address=TRB_address, chain_id=1, currency="usd")

    print(q.descriptor)
    print(f"queryData: 0x{q.query_data.hex()}")
    print(f"queryID: 0x{q.query_id.hex()}")

    value = 99.99
    print(f"submitValue (float): {value}")

    encoded_bytes = q.value_type.encode(value)
    print(f"submitValue (bytes): 0x{encoded_bytes.hex()}")

    decoded_value = q.value_type.decode(encoded_bytes)
    print(f"Decoded value (float): {decoded_value}")
