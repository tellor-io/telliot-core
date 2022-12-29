import json
import logging
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Literal
from typing import Optional

import requests

logger = logging.getLogger(__name__)
ethgastypes = Literal["fast", "fastest", "safeLow", "average", "standard"]


@dataclass
class GasStation:
    api: str
    default_speed: ethgastypes


async def fetch_gas_price() -> Optional[int]:
    """Estimate current ETH gas price

    Current implementation fetches from ethgasstation

    Returns:
        eth gas price in gwei
    """
    return await ethgasstation("fast")


async def ethgasstation(style: ethgastypes = "fast", retries: int = 2) -> Optional[int]:
    """Fetch gas price from ethgasstation in gwei"""
    for _ in range(retries):
        try:
            rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
            prices = json.loads(rsp.content)
            gas_price = int(prices[style])
            return int(gas_price / 10)  # json output is gwei*10
        except JSONDecodeError:
            logger.error("Error decoding JSON from ethgasstation API")
            continue
        except requests.exceptions.SSLError:
            logger.error("SSLError -- Unable to fetch gas price")
            return None
        except Exception as e:
            logger.error(f"Error fetching gas price: {e}")
    return None


ETH_GAS_PRICE_API = "https://ethgasstation.info/json/ethgasAPI.json"
MATIC_GAS_PRICE_API = "https://gasstation-mainnet.matic.network"
CHIADO_GAS_PRICE_API = "https://blockscout.com/xdai/mainnet/api/v1/gas-price-oracle"
gas_station = {
    1: GasStation(api=ETH_GAS_PRICE_API, default_speed="fast"),
    5: GasStation(api=ETH_GAS_PRICE_API, default_speed="fast"),
    137: GasStation(api=MATIC_GAS_PRICE_API, default_speed="safeLow"),
    80001: GasStation(api=MATIC_GAS_PRICE_API, default_speed="safeLow"),
    10200: GasStation(api=CHIADO_GAS_PRICE_API, default_speed="average"),
}


async def legacy_gas_station(chain_id: int, speed: Optional[ethgastypes] = None, retries: int = 2) -> Optional[int]:
    """Fetch gas price from gas station Api in gwei"""

    if speed is None:
        try:
            speed = gas_station[chain_id].default_speed
        except KeyError:
            logger.error(f"Please add gas station api for chain id: {chain_id}")
            return None

    for _ in range(retries):
        try:
            rsp = requests.get(gas_station[chain_id].api)
            prices = json.loads(rsp.content)
        except JSONDecodeError:
            logger.error("Error decoding JSON from gasstation API")
            continue
        except requests.exceptions.SSLError:
            logger.error("SSLError -- Unable to fetch gas price")
            return None
        except Exception as e:
            logger.error(f"Error fetching gas price: {e}")
            return None

    if speed not in prices:
        logger.error(f"Invalid gas price speed for gasstation: {speed}")
        return None

    if prices[speed] is None:
        logger.error("Unable to fetch gas price from gasstation")
        return None

    gas_price = int(prices[speed])
    return gas_price if chain_id not in (1, 5) else int(gas_price / 10)  # json output is gwei*10 for eth
