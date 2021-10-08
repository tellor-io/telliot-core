"""  :mod:`telliot.queries.query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from abc import ABC
from abc import abstractmethod
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type
from typing import Union
from typing import List
from web3 import Web3

from pydantic import BaseModel
from pydantic import Field
from telliot.response_type import ResponseType


CoerceToTipId = Union[bytearray, bytes, int, str]


def to_tip_id(value: CoerceToTipId) -> bytes:
    """Coerce input type to tip id in Bytes32 format

    """
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


def dict2argstr(d: dict) -> str:
    """ Convert a dict to a string of kwd=arg pairs

    """
    return ','.join("{!s}={!r}".format(key, val) for (key, val) in d.items())

class SerializableSubclassModel(BaseModel):
    """A helper subclass that allows nested serialization of subclasses

    """

    #: Container to register subclasses for pydantic export hack (see below)
    _subtypes_: ClassVar[Dict[str, Type[BaseModel]]] = dict()

    # used to register automatically all the submodels in `_subtypes_`.
    def __init_subclass__(cls, type: Optional[str] = None) -> None:
        cls._subtypes_[type or cls.__name__] = cls

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls._convert_to_real_type_

    @classmethod
    def _convert_to_real_type_(cls, data: Any) -> BaseModel:

        if isinstance(data, BaseModel):
            return data

        data_type = data.get("type")

        if data_type is None:
            raise ValueError("Missing 'type'")

        sub = cls._subtypes_.get(data_type)

        if sub is None:
            raise TypeError(f"Unsupported sub-type: {data_type}")

        return sub(**data)

    @classmethod
    def parse_obj(cls, obj: Dict[str, Any]) -> Any:
        return cls._convert_to_real_type_(obj)


class OracleQuery(SerializableSubclassModel, ABC):
    """Abstract Base class for all TellorX queries

    An OracleQuery specifies how to pose a question to the
    Tellor Oracle and how to format/interpret the response.

    The base class provides:

    - An identifier (:attr:`uid`) that uniquely identifies the query
      it within the TellorX network.
    - Calculation of the contents of the ``data`` field to include with the
      ``TellorX.Oracle.addTip()`` contract call.
    - Calculation of the `id` field field to include with the
      ``TellorX.Oracle.addTip()`` and ``TellorX.Oracle.submitValue()``
      contract calls
    - serialization/deserialization using the :meth:`OracleQuery.json` method.
    """

    type: str = Field("OracleQuery", constant=True)
    """ Type String

    Required to support registry serialization/deserialization
    Must be overridden with the Class Name in all subclasses
    """

    #: Unique query ID (Tellor Assigned).
    uid: str

    #: A descriptive name for the query.
    name: str

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

        # rtype = (
        #     f"abi_type={self.response_type.abi_type},packed={self.response_type.packed}"
        # )

        q = f"{self.query}?{rtype_str}"

        return q.encode("utf-8")

    def get_params(self) -> Dict[str, Any]:
        """ Returns a dictionary of all query parameter values

        """
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
