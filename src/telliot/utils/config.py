import enum
import pathlib
from typing import Union

import yaml
from pydantic import BaseModel
from yaml import CDumper as Dumper
from yaml import CLoader as Loader


class LogLevel(str, enum.Enum):
    """Enumeration of supported log levels"""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class ConfigOptions(BaseModel):
    """An object used to manage configuration options

    Each attribute represents an option in the config file.
    This object can be subclassed to add parameters.
    """

    loglevel: LogLevel = LogLevel.INFO

    class Config:
        # Export price_type as string
        use_enum_values = True

    @classmethod
    def from_file(cls, filename: Union[str, pathlib.Path]) -> "ConfigOptions":
        """Load Configuration from a .yaml file

        Parameters
        ----------
        filename
        """
        with open(filename, "r") as f:
            state = yaml.load(f, Loader=Loader)

        return cls.parse_obj(state)

    def to_file(self, filename: Union[str, pathlib.Path]) -> None:
        """Save configuration to a file"""
        try:
            with open(filename, "w") as f:
                state = self.dict()
                print(state)
                yaml.dump(state, f, Dumper=Dumper)
                print("Saved configuration to {}".format(filename))

        except FileNotFoundError as e:
            print("Error writing config file {}".format(filename))
            raise e
