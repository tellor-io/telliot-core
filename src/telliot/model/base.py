"""
Child class of pydantic.main.BaseModel with some configurations
"""
from pydantic.main import BaseModel


class Base(BaseModel):
    """Project-wide configuration of pydantic.main.BaseModel"""

    class Config:
        arbitrary_types_allowed = True
        extras = False
        use_enum_values = True
        underscore_attrs_are_private = True
