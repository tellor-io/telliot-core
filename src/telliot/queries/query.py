"""  :mod:`telliot.queries.query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Union

from pydantic import BaseModel
from telliot.response_type import ResponseType
from web3 import Web3


CoerceToTipId = Union[bytearray, bytes, int, str]


def to_tip_id(value: CoerceToTipId) -> bytes:
    """Coerce input type to tip id in Bytes32 format"""
    if isinstance(value, bytearray):
        value = bytes(value)

    if isinstance(value, bytes):
        bytes_value = value

    elif isinstance(value, str):
        value = value.lower()
        if value.startswith("0x"):
            value = value[2:]
        bytes_value = bytes.fromhex(value)

    elif isinstance(value, int):
        bytes_value = value.to_bytes(32, "big", signed=False)

    else:
        raise TypeError("Cannot convert {} to tip id".format(value))

    if len(bytes_value) != 32:
        raise ValueError("Tip ID must have 32 bytes")

    return bytes_value


def dict2argstr(d: Dict[str, Any]) -> str:
    """Convert a dict to a string of kwd=arg pairs"""
    return ",".join("{!s}={!r}".format(key, val) for (key, val) in d.items())


class OracleQuery(BaseModel, ABC):
    """Oracle Query

    An :class:`OracleQuery` specifies how to pose a question to the
    Tellor Oracle and how to format/interpret the response.

    The :class:`OracleQuery` class serves
    as the base class for all Queries, and implements default behaviors.
    Each subclass corresponds to a unique Query Type supported
    by the TellorX network.

    The base class provides:

    - Query :attr:`parameters` attributes that enable customization of
      the query type.

    - Calculation of the contents of the ``data`` field to include with the
      ``TellorX.Oracle.addTip()`` contract call.

    - Calculation of the `id` field field to include with the
      ``TellorX.Oracle.addTip()`` and ``TellorX.Oracle.submitValue()``
      contract calls

    """

    #: A list of parameter names used to customize the query
    parameters: ClassVar[List[str]]

    @property
    @abstractmethod
    def response_type(self) -> ResponseType:
        """Returns the response type the current Query configuration

        The response type defines required data type/structure of the
        ``value`` submitted to the contract through
        ``TellorX.Oracle.submitValue()``
        """
        pass

    @property
    def tip_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.addTip()``
        contract call.

        By convention, the tip data includes the unique ID, a query string
        and the expected response type in the following format:

        <:attr:`uid`> : <:attr:`query`> ? <:attr:`response_type`>
        """

        rtype_str = dict2argstr(self.response_type.dict())

        q = f"{self.query}?{rtype_str}"

        return q.encode("utf-8")

    def get_params(self) -> Dict[str, Any]:
        """Returns a dictionary of all query parameter values"""
        result = {}
        for p in self.parameters:
            result[p] = self.__getattribute__(p)

        return result

    @property
    def tip_id(self) -> bytes:
        """Returns the tip ``id`` for use with the
        ``TellorX.Oracle.addTip()`` and ``TellorX.Oracle.submitValue()``
        contract calls.
        """
        return bytes(Web3.keccak(self.tip_data))

    @property
    def query(self) -> str:
        """Returns the default query

        By default, a query will create a customized query string
        using currently configured values of each parameter.
        """

        params = self.get_params()

        param_str = dict2argstr(params)

        q = f"{self.__class__.__name__}({param_str})"

        return q
