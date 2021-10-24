""" Telliot registry module"""
from typing import Any
from typing import ClassVar
from typing import Dict
from typing import Optional
from typing import Type
from typing import Union

from telliot.model.base import Base


class ModelRegistry:
    """Telliot model registry

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


class RegisteredModel(Base):
    """A helper subclass that allows nested serialization

    The serialized format contains the class name, which can be used
    to reconstruct an object of the correct class.

    A registry is maintained to provide import context for
    reconstruction from the class name string.
    """

    def __init_subclass__(cls, type: Optional[str] = None) -> None:
        """Add to registry"""
        ModelRegistry.register(cls, type)

    @classmethod
    def __get_validators__(cls) -> Any:
        yield cls._convert_to_model

    @classmethod
    def _convert_to_model(cls, data: Union[Dict[str, Any], Base]) -> Base:
        """Convert input to a class instance

        When input is a JSON string, it should have two attributes:

        - 'type': The class name
        - 'inputs': keyword arguments to pass to the constructor

        """

        if isinstance(data, Base):
            return data

        data_type = data.get("type")

        if data_type is None:
            raise ValueError("Missing 'type'")

        factory = ModelRegistry.get(data_type)

        if factory is None:
            raise TypeError(f"Unsupported type: {data_type}")

        inputs = data.get("inputs")

        if inputs is None:
            raise ValueError("Missing inputs")

        return factory(**inputs)

    @classmethod
    def parse_obj(cls, obj: Dict[str, Any]) -> Any:
        return cls._convert_to_model(obj)

    def dict(self, **d_args: Any) -> Dict[str, Any]:
        """Convert model to dict

        Override pydantic model to return a dict that includes
        the class name to help deserialization.
        """

        dr = {"type": self.__class__.__name__, "inputs": super().dict(**d_args)}

        return dr
