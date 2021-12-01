from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Literal
from typing import Optional
from typing import Union

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.apps.staker import StakerList
from telliot_core.model.base import Base
from telliot_core.model.chain import ChainList
from telliot_core.model.endpoints import EndpointList
from telliot_core.model.endpoints import RPCEndpoint


@dataclass
class MainConfig(ConfigOptions):
    """Main telliot_core configuration object"""

    #: Control application logging level
    loglevel: Literal["DEBUG", "INFO", "WARNING", "ERROR", "CRITICAL"] = "INFO"

    #: Select chain id
    chain_id: int = 4

    #: Select network (e.g. mainnet, testnet, rinkeby
    network: str = "rinkeby"

    #: Private key for selected chain_id/network
    private_key: str = ""


@dataclass
class TelliotConfig(Base):
    """Main telliot_core configuration object

    Load all configuration objects from config files.
    If any config file does not exist, a default will be created.
    """

    config_dir: Optional[Union[str, Path]] = None

    main: MainConfig = field(default_factory=MainConfig)

    endpoints: EndpointList = field(default_factory=EndpointList)

    chains: ChainList = field(default_factory=ChainList)

    stakers: StakerList = field(default_factory=StakerList)

    def __post_init__(self) -> None:
        main_file = ConfigFile(
            name="main",
            config_type=MainConfig,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        ep_file = ConfigFile(
            name="endpoints",
            config_type=EndpointList,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        chain_file = ConfigFile(
            name="chains",
            config_type=ChainList,
            config_format="json",
            config_dir=self.config_dir,
        )
        staker_file = ConfigFile(
            name="stakers",
            config_type=StakerList,
            config_format="yaml",
            config_dir=self.config_dir,
        )

        self.main = main_file.get_config()
        self.endpoints = ep_file.get_config()
        self.chains = chain_file.get_config()
        self.stakers = staker_file.get_config()

    def get_endpoint(self) -> Optional[RPCEndpoint]:
        """Search endpoints for current chain_id"""
        return self.endpoints.get_chain_endpoint(self.main.chain_id)
