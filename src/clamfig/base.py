"""
Copyright (c) 2021, PyDefi Developemnt Team
Distributed under the terms of the MIT License.
"""
import logging
import traceback
from base64 import b64decode
from base64 import b64encode
from collections.abc import MutableMapping
from datetime import date
from datetime import datetime
from datetime import time
from decimal import Decimal
from pprint import pformat
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import List
from typing import Optional
from typing import Tuple
from typing import Type
from typing import Union

logger = logging.getLogger("clam_cereal")

stateType = Dict[str, Any]


class Serializable:
    """An mixin that allows an object that can be serialized to json or yaml.

    Currently supported subclass types:
        - dataclass
    """

    #: Registered type name, set during subclass initialization
    type: ClassVar[str]

    # ==========================================================================
    # Serialization API
    # ==========================================================================
    def __init_subclass__(cls, type: Optional[str] = None) -> None:
        """Add to registry"""
        type_name = type or cls.__name__  # f'{cls.__module__}.{cls.__name__}'
        Registry.register(subclass=cls, name=type_name)
        cls.type = type_name

    @classmethod
    def from_state(cls, state: stateType) -> "Serializable":
        """Create an object from the database state"""
        obj = cls.__new__(cls)
        obj.restore_state(state)
        return obj  # type: ignore

    def get_state(self) -> Dict[str, Any]:

        state: Dict[str, Any]
        state = {
            "type": self.type,
        }

        fields = list(f for f in self.__dataclass_fields__.values())  # type: ignore

        for f in fields:
            if f.init:
                state[f.name] = serialize(getattr(self, f.name))

        return state

    def restore_state(self, state: stateType) -> None:
        """Restore an object from the state"""
        name = state.get("type", self.type)
        if name != self.type:
            raise ValueError(f"Trying to use {name} state for {self.type} object")

        members = list(f for f in self.__dataclass_fields__.values())  # type: ignore

        for m in members:
            try:
                v = state[m.name]
                uobj = deserialize(
                    v,
                )
                setattr(self, m.name, uobj)
            except Exception:
                exc = traceback.format_exc()
                logger.error(
                    f"Error loading state:"
                    f"{self.type}.{m.name}:"
                    f"\nValue: {pformat(v)}"
                    f"\nState: {pformat(state)}"
                    f"\n{exc}"
                )


def find_subclasses(cls: type) -> List[type]:
    """Finds subclasses of the given class"""
    classes = []
    for subclass in cls.__subclasses__():
        classes.append(subclass)
        classes.extend(find_subclasses(subclass))
    return classes


#: Mapping of type name to coercer function
coercers = {
    "py_datetime.date": lambda s: date(**s),
    "py_datetime.datetime": lambda s: datetime(**s),
    "py_datetime.time": lambda s: time(**s),
    "py_bytes": lambda s: b64decode(s["bytes"]),
    "py_decimal": lambda s: Decimal(s["value"]),
}

valid_types = Union[
    Serializable, list, dict, tuple, date, datetime, time, bytes, Decimal
]


def serialize(v: valid_types) -> Union[Dict[str, Any], List[Any]]:
    """Recursively convert objects to a flattened dict or list"""
    if isinstance(v, Serializable):
        return v.get_state()

    elif isinstance(v, (list, tuple, set)):
        return [serialize(item) for item in v]

    elif isinstance(v, (dict, MutableMapping)):
        return {k: serialize(item) for k, item in v.items()}

    elif isinstance(v, bytes):
        return {"type": "py_bytes", "bytes": b64encode(v).decode()}

    elif isinstance(v, Decimal):
        return {"type": "py_decimal", "value": str(v)}

    elif isinstance(v, (date, datetime, time)):

        s: Dict[str, Any]

        s = {"type": f"py_{v.__class__.__module__}.{v.__class__.__name__}"}
        if isinstance(v, (date, datetime)):
            s.update({"year": v.year, "month": v.month, "day": v.day})
        if isinstance(v, (time, datetime)):
            s.update(
                {
                    "hour": v.hour,
                    "minute": v.minute,
                    "second": v.second,
                    "microsecond": v.microsecond,
                }
            )
        return s

    return v


def deserialize(
    v: Union[Dict[str, Any], List[Any], Tuple[Any]]
) -> Union[Type[Serializable], Dict[str, Any], List[Any]]:
    """Recursively convert a flattened dict or list to an Object,
    Dict of Objects, or List of Objects"""

    if isinstance(v, dict):

        # Create the object
        name = v.get("type")

        if name is not None:

            if name[:2] == "py":
                coercer = coercers.get(name)
                if coercer:
                    v.pop("type")
                    return coercer(v)  # type: ignore

            else:

                cls = Registry.registry[name]
                return instance(cls, v)

        return {k: deserialize(i) for k, i in v.items()}

    elif isinstance(v, (list, tuple)):
        return [deserialize(item) for item in v]
    return v


def instance(cls: Type[Serializable], state: stateType) -> Type[Serializable]:
    """Create an instance of the class using the given state"""

    obj = cls.__new__(cls)
    obj.restore_state(state)
    return obj  # type: ignore


class Registry:
    """Registry containing known object strings"""

    #: Type registry
    registry: ClassVar[Dict[str, Any]] = dict()

    @classmethod
    def register(cls, subclass: Type[Serializable], name: str) -> None:
        """Register a new type"""
        if name in cls.registry:
            raise NameError(f"Cannot register class. Duplicate name exists: {name}")
        cls.registry[name] = subclass
