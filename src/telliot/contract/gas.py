import json
from typing import Literal

import requests

ethgastypes = Literal["fast", "fastest", "safeLow", "average"]


async def fetch_gas_price() -> int:
    """Estimate current ETH gas price

    Current implementation fetches from ethgasstation

    Returns:
        eth gas price in gwei
    """
    return await ethgasstation("fast")


async def ethgasstation(style: ethgastypes = "fast") -> int:
    """Fetch gas price from ethgasstation in gwei"""
    rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    prices = json.loads(rsp.content)
    gas_price = int(prices[style])

    return int(gas_price / 10)  # json output is gwei*10
