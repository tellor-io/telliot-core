import os
from dataclasses import dataclass
from dataclasses import field
from pathlib import Path
from typing import Literal
from typing import Optional
from typing import Union

from chained_accounts import ChainedAccount
from chained_accounts import find_accounts

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.model.api_keys import ApiKeyList
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
    chain_id: int = 5


@dataclass
class TelliotConfig(Base):
    """Main telliot_core configuration object

    Load all configuration objects from config files.
    If any config file does not exist, a default will be created.
    """

    config_dir: Optional[Union[str, Path]] = None

    main: MainConfig = field(default_factory=MainConfig)

    endpoints: EndpointList = field(default_factory=EndpointList)

    api_keys: ApiKeyList = field(default_factory=ApiKeyList)

    chains: ChainList = field(default_factory=ChainList)

    # Private storage for config files
    _main_config_file: Optional[ConfigFile] = None
    _ep_config_file: Optional[ConfigFile] = None
    _api_keys_config_file: Optional[ConfigFile] = None
    _chain_config_file: Optional[ConfigFile] = None

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
        self._api_keys_config_file = ConfigFile(
            name="api_keys",
            config_type=ApiKeyList,
            config_format="yaml",
            config_dir=self.config_dir,
        )
        self._chain_config_file = ConfigFile(
            name="chains",
            config_type=ChainList,
            config_format="json",
            config_dir=self.config_dir,
        )

        self.main = self._main_config_file.get_config()
        self.endpoints = self._ep_config_file.get_config()
        self.api_keys = self._api_keys_config_file.get_config()
        self.chains = self._chain_config_file.get_config()

    def get_endpoint(self) -> RPCEndpoint:
        """Search endpoints for current chain_id"""
        eps = self.endpoints.find(chain_id=self.main.chain_id)
        if len(eps) > 0:
            return eps[0]
        else:
            raise ValueError(f"Endpoint not found for chain_id={self.main.chain_id}")


def override_test_config(cfg: TelliotConfig, write: bool = False) -> TelliotConfig:
    """Override config with test configuration

    Returns a rinkeby test configuration, using github secrets if they are defined

    FOR DEVELOPMENT USE ONLY
    Overrides the current configuration with rinkeby test config.
    Also handles overrides for github secret keys.
    """

    # Override configuration for rinkeby testnet
    override_main = False
    if cfg.main.chain_id != 11155111:
        cfg.main.chain_id = 11155111
        override_main = True

    sepolia_endpoint = cfg.get_endpoint()
    assert sepolia_endpoint is not None

    override_endpoint = False
    if os.getenv("NODE_URL", None):
        sepolia_endpoint.url = os.environ["NODE_URL"]
        override_endpoint = True

    sepolia_accounts = find_accounts(chain_id=11155111)
    if not sepolia_accounts:

        # Add private key if detected on git
        if os.getenv("PRIVATE_KEY", None):
            # Create an account for use on git
            ChainedAccount.add("git-sepolia-key", chains=[11155111], key=os.environ["PRIVATE_KEY"], password="")

    if write:
        if override_endpoint:
            assert cfg._ep_config_file is not None
            cfg._ep_config_file.save_config(cfg.endpoints)
        if override_main:
            assert cfg._main_config_file is not None
            cfg._main_config_file.save_config(cfg.main)

    return cfg
