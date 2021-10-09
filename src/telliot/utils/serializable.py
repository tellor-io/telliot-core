from typing import Any, ClassVar, Dict, Optional, Type

from pydantic import BaseModel


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
