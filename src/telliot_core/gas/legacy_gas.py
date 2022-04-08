import json
import logging
from json.decoder import JSONDecodeError
from time import sleep
from typing import Literal
from typing import Optional

import requests

logger = logging.getLogger(__name__)
ethgastypes = Literal["fast", "fastest", "safeLow", "average"]


async def fetch_gas_price() -> Optional[int]:
    """Estimate current ETH gas price

    Current implementation fetches from ethgasstation

    Returns:
        eth gas price in gwei
    """
    return await ethgasstation("fast")


async def ethgasstation(style: ethgastypes = "fast") -> Optional[int]:
    """Fetch gas price from ethgasstation in gwei"""
    i = 0
    while i < 2:
        try:
            rsp = requests.get("https://ethgastation.info/json/ethgasAPI.json")
            prices = json.loads(rsp.content)
            gas_price = int(prices[style])
            return int(gas_price / 10)  # json output is gwei*10
        except JSONDecodeError:
            logger.info("ethgasstation api retrying ...")
            i += 1
            sleep(1)
            continue
    return None
