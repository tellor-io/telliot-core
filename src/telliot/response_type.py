from typing import Any

import eth_abi.grammar
from eth_abi.abi import decode_single
from eth_abi.abi import encode_single
from eth_abi.packed import encode_single_packed
from pydantic import BaseModel
from pydantic import validator


class ResponseType(BaseModel):
    """Specify format of Query Response"""

    #: Type string per eth-abi grammar
    #: https://eth-abi.readthedocs.io/en/latest/grammar.html
    abi_type: str = "uint256"

    #: True if response should be packed
    packed: bool = False

    @validator("abi_type")
    def require_valid_grammar(cls, v):  # type: ignore
        """Validate and normalize abi type string"""
        t = eth_abi.grammar.parse(v)
        t.validate()
        return eth_abi.grammar.normalize(v)  # type: ignore

    def encode(self, response: Any) -> bytes:
        """Encode a response using abi type string

        Args:
            response: Value to encode

        Returns:
            Encoded value
        """
        if self.packed:
            return encode_single(self.abi_type, response)
        else:
            return encode_single_packed(self.abi_type, response)

    def decode(self, bytes_val: bytes) -> Any:
        """Decode bytes into a response using abi type string

        Args:
            bytes_val: Bytes to decode

        Returns:
            Decoded response
        """
        return decode_single(self.abi_type, bytes_val)
