from telliot.types.value_type import ValueType
from decimal import Decimal
from typing import Any
from pydantic import validator


class UnsignedFloatType(ValueType):
    """Unsigned Float Type

    This class specifies the a floating point value
    using an ABI data type.  It also provides encoding/decoding
    to/from floating point values.

    """

    # Default ABI Encoding for Unsigned Float value
    abi_type: str = "ufixed256x6"

    def __init__(self, **data: Any) -> None:

        super().__init__(**data)

    @validator("abi_type")
    def require_ufixed_abi_type(cls, v: str) -> str:
        """Validator to require a ufixed abi type

        """
        if v[:6] != 'ufixed':
            raise ValueError("Abi Type must be ufixedMxN")

        return v.lower()

    @property
    def decimals(self) -> int:
        """Get precision from abi type"""
        mxn = self.abi_type[6:]
        m, n = mxn.split('x')
        return int(n)

    @property
    def nbits(self) -> int:
        """Get number of bits from abi type"""
        mxn = self.abi_type[6:]
        m, n = mxn.split('x')
        return int(m)

    def encode(self, value: float) -> bytes:
        """An encoder for float values

        This encoder converts a float value to the CoinPrice ABI
        data type.
        """

        decimal_value = Decimal(value).quantize(Decimal(10) ** -self.decimals)

        return super().encode(decimal_value)

    def decode(self, bytes_val: bytes) -> Any:
        """A decoder for float values

        This decoder converts from the CoinPrice ABI data type to
        a floating point value.
        """
        nbytes = self.nbits / 8

        if self.packed:
            if len(bytes_val) != nbytes:
                raise ValueError(f"Value must be {nbytes} bytes")

        intval = int.from_bytes(bytes_val, "big", signed=False)

        return intval / 10.0 ** self.decimals
