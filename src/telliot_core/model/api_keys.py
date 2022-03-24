"""
Config file for user API keys for data sources.
"""
import logging
from dataclasses import dataclass
from dataclasses import field
from typing import List
from typing import Optional

from telliot_core.apps.config import ConfigFile
from telliot_core.apps.config import ConfigOptions
from telliot_core.model.base import Base

logger = logging.getLogger(__name__)


@dataclass
class ApiKey(Base):
    """API Key used for a data source."""

    #: API key name
    name: str = ""

    #: API key (secret)
    key: str = ""

    #: Associated URL
    url: str = ""


default_api_keys = [
    ApiKey(name="anyblock", key="", url="https://api.anyblock.tools/"),
    ApiKey(
        name="bravenewcoin",
        key="",
        url="https://bravenewcoin.p.rapidapi.com/",
    ),
    ApiKey(name="nomics", key="", url="https://api.nomics.com/"),
    ApiKey(name="coinmarketcap", key="", url="https://pro-api.coinmarketcap.com/"),
]


@dataclass
class ApiKeyList(ConfigOptions):
    api_keys: List[ApiKey] = field(default_factory=lambda: default_api_keys)

    def find(
        self,
        name: Optional[str] = None,
        url: Optional[str] = None,
    ) -> list[ApiKey]:

        result = []
        for api_key in self.api_keys:

            if name is not None:
                if name != api_key.name:
                    continue
            if url is not None:
                if url != api_key.url:
                    continue

            result.append(api_key)

        return result


if __name__ == "__main__":
    cf = ConfigFile(name="api_keys", config_type=ApiKeyList, config_format="yaml")

    config_endpoints = cf.get_config()

    print(config_endpoints)
