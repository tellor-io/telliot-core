""" Telliot registry module"""
import dataclasses
import inspect
from typing import Any, Optional, List
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type
from typing import Union
from typing import List
from typing import Tuple
import json

from telliot.model.base import Base

ModelStateType = List[Tuple[str, Dict[str, Any]]]


def find_subclasses(cls: Type[Any]) -> List[Type[Any]]:
    """ Finds subclasses of the given class"""
    classes = []
    for subclass in cls.__subclasses__():
        classes.append(subclass)
        classes.extend(find_subclasses(subclass))
    return classes


class Serializer:
    """Telliot model registry for serialization/deserialization

    Main telliot model registry used for registering
    OracleQuery, DataSource, DataFeed, and ValueType classes.
    """

    #: Type Registry
    _registry: ClassVar[Dict[str, Type[Base]]] = dict()

    @classmethod
    def register(cls, model: Type[Base], name: Optional[str] = None) -> None:
        registered_type = name or model.__name__

        if registered_type in cls._registry:
            raise NameError(
                f"Cannot register class with pytelliot. "
                f"Duplicate name exists: {registered_type}"
            )

        cls._registry[registered_type] = model

    @classmethod
    def get(cls, name: str) -> Optional[Type[Base]]:
        """Get a model from the registry by name"""
        return cls._registry.get(name)

    @classmethod
    def models(cls) -> Dict[str, Type[Base]]:
        """Get a model from the registry by name"""
        return cls._registry


class RegisteredModel(Base):
    """A helper subclass that allows nested serialization

    The serialized format contains the class name, which can be used
    to reconstruct an object of the correct class.

    A registry is maintained to provide import context for
    reconstruction from the class name string.
    """

    def __init_subclass__(cls, type: Optional[str] = None) -> None:
        """Add to registry"""
        Serializer.register(cls, type)

    # @classmethod
    # def __get_validators__(cls) -> Any:
    #     yield cls._convert_to_model

    @classmethod
    def _convert_to_model(cls, data: Union[ModelStateType, Base]) -> Base:
        """Convert input to a class instance

        When input is a JSON string, it should have two attributes:

        - 'type': The class name
        - 'inputs': keyword arguments to pass to the constructor

        """

        if isinstance(data, Base):
            return data

        data_type = data[0]

        if data_type is None:
            raise ValueError("Missing 'type'")

        factory = Serializer.get(data_type)

        if factory is None:
            raise TypeError(f"Unsupported type: {data_type}")

        inputs = data[1]

        if inputs is None:
            raise ValueError("Missing inputs")

        return factory(**inputs)

    @classmethod
    def from_state(cls, obj: ModelStateType) -> Any:
        return cls._convert_to_model(obj)

    def to_state(self) -> ModelStateType:
        """Convert model to a python object representing the to_state of the model

        Override pydantic model to return a dict that includes
        the class name to help deserialization.
        """

        dr = (self.__class__.__name__, super().dict())

        return dr

    def to_json(self, compact=True):
        if compact:
            return json.dumps(self.to_state())
        else:
            return json.dumps(self.to_state(), separators=(',', ':'))

    @classmethod
    def from_json(cls, jstr: str):
        state = json.loads(jstr)
        return cls.from_state(state)


class SimpleSerial:
    def __init_subclass__(cls, type: Optional[str] = None) -> None:
        """Add to registry"""
        Serializer.register(cls, type)

    @classmethod
    def _arg_names(cls) -> List[str]:
        sig = inspect.signature(cls.__init__)
        names = list(sig.parameters.keys())
        names.pop(0)  # Remove 'self' argument

        if not dataclasses.is_dataclass(cls):
            if names == ['args', 'kwargs']:
                raise Exception(f"__init__() method undefined in {cls.__name__}. Define __init__() or use dataclass ")

        return names

    def arg_dict(self):
        d = {}
        for name in self._arg_names():
            val = getattr(self, name)
            d[name] = val
        return d


    @classmethod
    def from_state(cls, obj: ModelStateType) -> Any:
        return cls._convert_to_model(obj)

    def to_state(self) -> ModelStateType:
        """Convert model to a python object representing the to_state of the model

        Override pydantic model to return a dict that includes
        the class name to help deserialization.
        """

        dr = (self.__class__.__name__, self.arg_dict())

        return dr

    def to_json(self, compact=True):
        if compact:
            return json.dumps(self.to_state(), separators=(',', ':'))
        else:
            return json.dumps(self.to_state())

    @classmethod
    def from_json(cls, jstr: str):
        state = json.loads(jstr)
        return cls.from_state(state)

