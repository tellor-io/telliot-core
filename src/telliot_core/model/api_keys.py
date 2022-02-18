"""
Config file for user API keys for data sources.
"""
import logging
from dataclasses import dataclass
from dataclasses import field
from typing import List

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.model.base import Base

logger = logging.getLogger(__name__)


@dataclass
class ApiKey(Base):
    """JSON RPC Endpoint for EVM compatible network"""

    #: API key name
    name: str = ""

    #: API key (secret)
    key: str = ""


default_api_keys = [
    ApiKey(
        name="anyblock",
        key="",
    ),
    ApiKey(
        name="bravenewcoin",
        key="",
    ),
    ApiKey(
        name="nomics",
        key="",
    )
]


@dataclass
class ApiKeyList(ConfigOptions):
    endpoints: List[ApiKey] = field(default_factory=lambda: default_api_keys)

    def find() -> None:
        # TODO
        pass


if __name__ == "__main__":
    cf = ConfigFile(name="api_keys", config_type=ApiKeyList, config_format="yaml")

    config_endpoints = cf.get_config()

    print(config_endpoints)
