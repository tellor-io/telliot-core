import eth_abi.grammar
from eth_abi import decode_single, encode_single
from eth_abi.packed import encode_single_packed
from pydantic import BaseModel, validator


class ResponseType(BaseModel):
    """ Specify format of Query Response

    """

    #: Type string per eth-abi grammar
    #: https://eth-abi.readthedocs.io/en/latest/grammar.html
    abi_type: str

    #: True if response should be packed
    packed: bool = False

    @validator("abi_type")
    def require_valid_grammar(cls, v):
        t = eth_abi.grammar.parse(v)
        t.validate()
        return eth_abi.grammar.normalize(v)

    def encode(self, value):
        if self.packed:
            return encode_single(self.abi_type, value)
        else:
            return encode_single_packed(self.abi_type, value)

    def decode(self, value):
        return decode_single(self.abi_type, value)