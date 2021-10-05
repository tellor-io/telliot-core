import pathlib
from pathlib import Path
from typing import Any
from typing import Optional
from typing import Union

import yaml
from telliot.utils.base import Base
from yaml import CDumper as Dumper
from yaml import CLoader as Loader


class ConfigOptions(Base):
    """An object used to manage configuration options

    Each attribute represents a configuration option.

    if `config_file` is provided, load and store methods will be available.
    This object can be subclassed to add parameters.

    """

    #: Configuration version used to manage config file versions
    config_version: str = "0.0.1"

    #: Private storage for Config File Path
    _config_file: Optional[Path]

    @property
    def config_file(self) -> Optional[Path]:
        return self._config_file

    def __init__(
        self, config_file: Optional[Union[str, Path]] = None, **data: Any
    ) -> None:
        """Construct a new ConfigOptions object

        Args:
            **data: Configuration options (Keyword/Argument pairs)
            config_file: Optional file
        """

        super().__init__(**data)

        if config_file:
            self._config_file = Path(config_file).resolve().absolute()
        else:
            self._config_file = None

    @classmethod
    def from_file(cls, filename: Union[str, pathlib.Path]) -> Any:
        """Load Configuration from a .yaml file

        Parameters
        ----------
        filename
        """
        filepath = Path(filename).resolve().absolute()

        with open(filepath, "r") as f:
            state = yaml.load(f, Loader=Loader)

        obj = cls.parse_obj(state)
        obj._config_file = filepath

        return obj

    def save(self) -> None:
        """Save configuration to file"""
        if not self.config_file:
            raise AttributeError("Cannot save configuration.  config_file not defined")

        try:

            # Make sure folder exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            with open(self.config_file, "w") as f:
                state = self.dict()
                print(state)
                yaml.dump(state, f, Dumper=Dumper)
                print(
                    "Saved {} to {}".format(self.__class__.__name__, self.config_file)
                )

        except FileNotFoundError as e:
            print(
                "Error saving {} to {}".format(
                    self.__class__.__name__, self.config_file
                )
            )
            raise e
