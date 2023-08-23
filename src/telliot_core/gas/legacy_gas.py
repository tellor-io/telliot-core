import json
import logging
import math
from dataclasses import dataclass
from json.decoder import JSONDecodeError
from typing import Literal
from typing import Optional
from typing import Union

import requests

logger = logging.getLogger(__name__)
ethgastypes = Literal["fast", "fastest", "safeLow", "average", "standard"]


@dataclass
class GasStation:
    api: str
    parse_rsp: list[Union[str, int, ethgastypes]]


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
    1: GasStation(api=ETH_GAS_PRICE_API, parse_rsp=["fast"]),
    5: GasStation(api=ETH_GAS_PRICE_API, parse_rsp=["fast"]),
    11155111: GasStation(api=ETH_GAS_PRICE_API, parse_rsp=["fast"]),
    10: GasStation(api=OPTIMISM_GAS_PRICE_API, parse_rsp=["speeds", 2, "gasPrice"]),
    420: GasStation(api=OPTIMISM_GAS_PRICE_API, parse_rsp=["speeds", 2, "gasPrice"]),
    42161: GasStation(api=ARBITRUM_GAS_PRICE_API, parse_rsp=["speeds", 2, "gasPrice"]),
    421613: GasStation(api=ARBITRUM_GAS_PRICE_API, parse_rsp=["speeds", 2, "gasPrice"]),
    137: GasStation(api=MATIC_GAS_PRICE_API, parse_rsp=["safeLow"]),
    80001: GasStation(api=MATIC_GAS_PRICE_API, parse_rsp=["safeLow"]),
    10200: GasStation(api=CHIADO_GAS_PRICE_API, parse_rsp=["average"]),
    100: GasStation(api=GNOSIS_GAS_PRICE_API, parse_rsp=["average"]),
}


async def legacy_gas_station(
    chain_id: int, speed_parse_lis: Optional[list[Union[str, int, ethgastypes]]] = None, retries: int = 2
) -> Optional[int]:
    """Fetch gas price from gas station Api in gwei"""
    prices = {}
    if chain_id not in gas_station:
        logger.error(f"Please add gas station API for chain id: {chain_id}")
        return None

    for _ in range(retries):
        try:
            rsp = requests.get(gas_station[chain_id].api)
            prices = json.loads(rsp.content)
        except JSONDecodeError:
            logger.error("Error decoding JSON from gasstation API")
            continue
        except requests.exceptions.SSLError:
            logger.error("SSLError: Unable to fetch gas price")
            return None
        except Exception as e:
            logger.error(f"Error fetching gas price: {e}")
            return None

    if speed_parse_lis is None:
        speed_parse_lis = gas_station[chain_id].parse_rsp

    for i in speed_parse_lis:
        try:
            prices = prices[i]
        except (KeyError, IndexError):
            logger.error(f"Unable to parse gas price from gasstation: {speed_parse_lis}")
            return None

    if isinstance(prices, int):
        gas_price = prices
    elif isinstance(prices, float):
        gas_price = int(prices) if prices > 1 else math.ceil(prices)
    else:
        logger.error(f"Invalid reponse from gas station API: {prices}")
        return None

    return gas_price if chain_id not in (1, 5) else int(gas_price / 10)  # json output is gwei*10 for eth


if __name__ == "__main__":
    import asyncio

    loop = asyncio.get_event_loop()
    for chain_id in gas_station:
        price = loop.run_until_complete(legacy_gas_station(chain_id))
        assert isinstance(price, int)
        assert price > 0
        print(chain_id, price)
