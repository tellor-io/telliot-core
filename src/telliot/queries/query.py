""" Base Query Classes

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

from pydantic import BaseModel
from pydantic import Field
from telliot.response_type import ResponseType


CoerceToRequestId = Union[bytearray, bytes, int, str]


def to_request_id(value: CoerceToRequestId) -> bytes:
    """Coerce input type to request_id in Bytes32 format

    Args:
        value:  CoerceToRequestId

    Returns:
        bytes: Request ID
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
        raise TypeError("Cannot convert {} to request_id".format(value))

    if len(bytes_value) != 32:
        raise ValueError("Request ID must have 32 bytes")

    return bytes_value


class SerializableSubclassModel(BaseModel):
    """Pydantic subclass that allows nested serialization of subclasses

    The following machinery is used to force Pydantic to properly
    serialize and deserialize OracleQuery subclasses by including
    type info in the JSON stream, per the following:

    - https://github.com/samuelcolvin/pydantic/issues/2177
    - https://github.com/samuelcolvin/pydantic/discussions/3091

    This pydantic Config is required to prevent the following error:
    ``cls._subtypes_[type or cls.__name__.lower()] = cls``
    ``TypeError: 'member_descriptor' object does not support item assignment``
    """

    # class Config:
    #    underscore_attrs_are_private = False

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
    """Abstract Base class for all tellorX queries"""

    #: Type field is required to support registry export/import through json
    #: Must be overridden in all OracleQuery subclasses
    type: str = Field("OracleQuery", constant=True)

    #: Unique query ID (Tellor Assigned)
    uid: str

    #: Descriptive name
    name: str

    @property
    @abstractmethod
    def response_type(self) -> ResponseType:
        """Return the response type the current Query configuration

        The response type defines required data type of
        `value` in the corresponding `TellorX.submitValue` function call
        """
        pass

    @property
    def tip_data(self) -> bytes:
        """Return the tip data for the current Query configuration

        Returns:
            `data` field for use in `TellorX.addTip()` function
        """

        rtype = (
            f"abi_type={self.response_type.abi_type},packed={self.response_type.packed}"
        )

        q = f"{self.uid}?{self.question}?{rtype}"

        return q.lower().encode("utf-8")

    @property
    @abstractmethod
    def request_id(self) -> bytes:
        """Return the request ID for the current Query configuration

        Returns:
            bytes: 32-byte Request ID
        """
        pass

    @property
    @abstractmethod
    def question(self) -> str:
        """Return question for the current Query configuration

        Questions should not have question marks.

        Parameterized queries must return a unique question for each
        possible combinations of parameters.
        """
        pass
