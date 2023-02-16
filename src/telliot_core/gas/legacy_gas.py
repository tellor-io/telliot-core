import json
import logging
import math
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Literal
from typing import Optional
from typing import Tuple
from typing import Union

import requests

logger = logging.getLogger(__name__)
ethgastypes = Literal["fast", "fastest", "safeLow", "average", "standard"]


@dataclass
class GasStation:
    api: str
    default_speed: Union[Tuple[str, int, str], ethgastypes]


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
GNOSIS_GAS_PRICE_API = "https://blockscout.com/xdai/mainnet/api/v1/gas-price-oracle"
OPTIMISM_GAS_PRICE_API = "https://api.owlracle.info/v3/opt/gas"
ARBITRUM_GAS_PRICE_API = "https://api.owlracle.info/v3/arb/gas"

gas_station = {
    1: GasStation(api=ETH_GAS_PRICE_API, default_speed="fast"),
    5: GasStation(api=ETH_GAS_PRICE_API, default_speed="fast"),
    10: GasStation(api=OPTIMISM_GAS_PRICE_API, default_speed=("speeds", 2, "gasPrice")),
    42161: GasStation(api=ARBITRUM_GAS_PRICE_API, default_speed=("speeds", 2, "gasPrice")),
    137: GasStation(api=MATIC_GAS_PRICE_API, default_speed="safeLow"),
    80001: GasStation(api=MATIC_GAS_PRICE_API, default_speed="safeLow"),
    10200: GasStation(api=CHIADO_GAS_PRICE_API, default_speed="average"),
    100: GasStation(api=GNOSIS_GAS_PRICE_API, default_speed="average"),
}


async def legacy_gas_station(
    chain_id: int, speed: Optional[Union[Tuple[str, int, str], ethgastypes]] = None, retries: int = 2
) -> Optional[int]:
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

    if isinstance(speed, tuple):
        try:
            gas_price = prices[speed[0]][speed[1]][speed[2]]
            # optimisim gas price is returning 0.01 gwei so we need to round up
            gas_price = int(gas_price) if gas_price > 1 else math.ceil(gas_price)
            if gas_price is None:
                logger.error("Unable to fetch gas price from gasstation")
                return None
        except (KeyError, IndexError):
            logger.error(f"Invalid gas price speed for gasstation: {speed}")
            return None
    else:
        if speed not in prices:
            logger.error(f"Invalid gas price speed for gasstation: {speed}")
            return None
        if prices[speed] is None:
            logger.error("Unable to fetch gas price from gasstation")
            return None
        gas_price = int(prices[speed])

    return gas_price if chain_id not in (1, 5) else int(gas_price / 10)  # json output is gwei*10 for eth


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    for i in (1, 5, 10, 42161, 137, 80001, 10200, 100):
        price = loop.run_until_complete(legacy_gas_station(i))
        assert isinstance(price, int)
        print(i, price)
