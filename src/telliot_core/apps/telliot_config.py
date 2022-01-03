import os
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

    # Private storage for config files
    _main_config_file: Optional[ConfigFile] = None
    _ep_config_file: Optional[ConfigFile] = None
    _chain_config_file: Optional[ConfigFile] = None
    _staker_config_file: Optional[ConfigFile] = None

    def __post_init__(self) -> None:
        self._main_config_file = ConfigFile(
            name="main",
            config_type=MainConfig,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        self._ep_config_file = ConfigFile(
            name="endpoints",
            config_type=EndpointList,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        self._chain_config_file = ConfigFile(
            name="chains",
            config_type=ChainList,
            config_format="json",
            config_dir=self.config_dir,
        )
        self._staker_config_file = ConfigFile(
            name="stakers",
            config_type=StakerList,
            config_format="yaml",
            config_dir=self.config_dir,
        )

        self.main = self._main_config_file.get_config()
        self.endpoints = self._ep_config_file.get_config()
        self.chains = self._chain_config_file.get_config()
        self.stakers = self._staker_config_file.get_config()

    def get_endpoint(self) -> Optional[RPCEndpoint]:
        """Search endpoints for current chain_id"""
        return self.endpoints.get_chain_endpoint(self.main.chain_id)


def override_test_config(cfg: TelliotConfig, write: bool = False) -> TelliotConfig:
    """Override config with test configuration

    Returns a rinkeby test configuration, using github secrets if they are defined

    FOR DEVELOPMENT USE ONLY
    Overrides the current configuration with rinkeby test config.
    Also handles overrides for github secret keys.
    """

    # Override configuration for rinkeby testnet
    override_main = False
    if cfg.main.chain_id != 4:
        cfg.main.chain_id = 4
        override_main = True

    rinkeby_endpoint = cfg.get_endpoint()
    assert rinkeby_endpoint is not None

    override_endpoint = False
    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]
        override_endpoint = True

    # Replace staker private key
    override_staker = False
    if os.getenv("PRIVATE_KEY", None):
        override_staker = True
        private_key = os.environ["PRIVATE_KEY"]
        rinkeby_stakers = cfg.stakers.find(chain_id=4)
        if len(rinkeby_stakers) == 0:
            raise Exception("No staker/private key defined for rinkeby")
        rinkeby_staker = rinkeby_stakers[0]
        rinkeby_staker.private_key = private_key
        rinkeby_staker.address = "0x8D8D2006A485FA4a75dFD8Da8f63dA31401B8fA2"

    if write:
        if override_staker:
            assert cfg._staker_config_file is not None
            cfg._staker_config_file.save_config(cfg.stakers)
        if override_endpoint:
            assert cfg._ep_config_file is not None
            cfg._ep_config_file.save_config(cfg.endpoints)
        if override_main:
            assert cfg._main_config_file is not None
            cfg._main_config_file.save_config(cfg.main)

    return cfg
