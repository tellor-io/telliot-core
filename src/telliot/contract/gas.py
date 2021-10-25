# import asyncio
import json
from typing import Literal

import requests

ethgastypes = Literal["fast", "fastest", "safeLow", "average"]


# async def estimate_gas() -> int:
#     """Estimate current ETH gas price

#     Work In Progress - Just do something quick
#     """
#     return asyncio.run(ethgasstation("fast"))


# async def ethgasstation(style: ethgastypes = "fast") -> int:
#     """Fetch gas price from ethgasstation"""
#     rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
#     prices = json.loads(rsp.content)
#     gas_price = int(prices[style])

#     return gas_price

def estimate_gas(style: ethgastypes = "fast") -> int:
    """Fetch gas price from ethgasstation"""
    rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
    prices = json.loads(rsp.content)
    gas_price = int(prices[style])

    return gas_price