'''Configuration class for AMPL plugin.'''
from dataclasses import dataclass, field

from telliot.apps.config import ConfigFile, ConfigOptions
from telliot.model.base import Base
from typing import Optional, Union
from pathlib import Path


@dataclass
class AMPLConfigOptions(ConfigOptions):
    '''Configurations needed for AMPL apis.'''
    # Acces key for AnyBlock api
    anyblock_api_key: str = ""

    # Access key for BraveNewCoin / Rapid api
    rapid_api_key: str = ""


@dataclass
class AMPLConfig(Base):
    """Main AMPL plugin configuration object"""

    config_dir: Optional[Union[str, Path]] = None

    main: AMPLConfigOptions = field(default_factory=AMPLConfigOptions)

    def __post_init__(self) -> None:
        main_file = ConfigFile(
            name="ampl",
            config_type=AMPLConfigOptions,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        self.main = main_file.get_config()  # type: ignore
