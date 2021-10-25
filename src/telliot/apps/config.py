"""telliot.apps.config module"""
import logging
from pathlib import Path
from typing import Literal
from typing import Optional
from typing import Type
from typing import Union

import yaml
from telliot.model.base import Base
from telliot.utils.home import telliot_homedir
from yaml import CDumper as Dumper
from yaml import CLoader as Loader


logger = logging.getLogger(__name__)

config_formats = Literal["yaml", "json"]


class ConfigOptions(Base):
    """An object used to manage configuration options

    Each attribute represents a configuration option.
    Subclasses should add configuration attributes as required.
    """
    pass

class ConfigFile:
    """ConfigFile"""

    @property
    def config_file(self) -> Path:
        return self.config_dir / f"{self.name}.{self.config_format}"

    def __init__(
        self,
        name: str,
        config_type: Type[ConfigOptions],
        config_dir: Optional[Union[str, Path]] = None,
        config_format: config_formats = "yaml",
    ) -> None:
        """Construct a new ConfigFile object

        Args:
            name:
                Config filename

            config_dir:
                Config file folder  If None, home directory is automatically computed.

            config_format:
                Format of config file ('yaml' or 'json')

        """

        #: Configuration Name
        self.name = name

        #: Config Type
        self.config_type = config_type

        #: Configuration Folder
        self.config_dir = telliot_homedir(config_dir)

        #: File Format
        self.config_format = config_format

        # Try to load configuration from file
        if self.config_file.exists():

            # Try to load file
            _ = self.get_config()

        else:
            # Create a default configuration and save it
            print(f"Creating default {self.name} config file")
            options = self.config_type()
            self.save_config(options)
            print(f"Saved config file: {self.config_file}")

    def get_config(self) -> ConfigOptions:
        """Load Configuration from a .yaml file"""

        if self.config_format == "yaml":

            with open(self.config_file, "r") as f:

                state = yaml.load(f, Loader=Loader)

                # Try to parse file
                config = self.config_type.parse_obj(state)

        elif self.config_format == "json":

            config = self.config_type.parse_file(self.config_file)

        else:
            raise AttributeError(f"Invalid config file type: {self.config_format}")

        return config

    def save_config(self, config: ConfigOptions) -> None:

        """Save configuration to file"""

        try:

            # Make sure folder exists
            self.config_file.parent.mkdir(parents=True, exist_ok=True)

            # Back up existing file
            if self.config_file.exists():
                self.config_file.rename(self.config_file.with_suffix(".bak"))

            if self.config_format == "yaml":
                with open(self.config_file, "w") as f:
                    state = config.dict()
                    print(state)
                    yaml.dump(state, f, Dumper=Dumper, sort_keys=False)

            elif self.config_format == "json":

                with open(self.config_file, "w") as f:
                    jstr = config.json(indent=2)
                    f.write(jstr)

            print("Saved {} to {}".format(self.name, self.config_file))

        except FileNotFoundError as e:
            print(
                "Error saving {} to {}".format(
                    self.__class__.__name__, self.config_file
                )
            )
            raise e
