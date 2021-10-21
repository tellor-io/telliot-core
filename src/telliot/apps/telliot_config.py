import enum
from pathlib import Path
from typing import Optional

from telliot.apps.config import ConfigFile
from telliot.apps.config import ConfigOptions
from telliot.model.chain import ChainList
from telliot.model.endpoints import EndpointList
from telliot.model.endpoints import RPCEndpoint
from telliot.utils.base import Base


class LogLevel(str, enum.Enum):
    """Enumeration of supported log levels"""

    DEBUG = "debug"
    INFO = "info"
    WARNING = "warning"
    ERROR = "error"
    CRITICAL = "critical"


class MainConfig(ConfigOptions):
    """Main telliot configuration object"""

    config_version: str = "0.0.1"

    #: Control application logging level
    loglevel: LogLevel = LogLevel.INFO

    #: Select chain id
    chain_id: int = 4

    #: Select network (e.g. mainnet, testnet, rinkeby
    network: str = "rinkeby"

    #: Private key for selected chain_id/network
    private_key: str = ""


class TelliotConfig(Base):
    """Main telliot configuration object

    Load all configuration objects from config files.
    If any config file does not exist, a default will be created.
    """

    main: MainConfig

    endpoints: EndpointList

    chains: ChainList

    def __init__(self, config_dir: Optional[Path] = None) -> None:
        main_file = ConfigFile(
            name="main",
            config_type=MainConfig,
            config_format="yaml",
            config_dir=config_dir,
        )
        ep_file = ConfigFile(
            name="endpoints",
            config_type=EndpointList,
            config_format="yaml",
            config_dir=config_dir,
        )
        chain_file = ConfigFile(
            name="chains",
            config_type=ChainList,
            config_format="json",
            config_dir=config_dir,
        )

        super().__init__(
            main=main_file.get_config(),
            endpoints=ep_file.get_config(),
            chains=chain_file.get_config(),
        )

    def get_endpoint(self) -> Optional[RPCEndpoint]:
        """Search endpoints for current chain_id"""
        return self.endpoints.get_chain_endpoint(self.main.chain_id)
