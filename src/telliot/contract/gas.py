import asyncio
import json
from typing import Literal, Optional, Tuple

import requests

from telliot.utils.response import ResponseStatus

ethgastypes = Literal["fast", "fastest", "safeLow", "average"]


async def estimate_gas() -> Tuple[Optional[int], ResponseStatus]:
    """Estimate current ETH gas price

    Work In Progress - Just do something quick
    """
    return asyncio.run(ethgasstation("fast"))


async def ethgasstation(style: ethgastypes = "fast") -> Tuple[Optional[int], ResponseStatus]:
    """Fetch gas price from ethgasstation"""
    try:
        status = ResponseStatus()
        rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
        prices = json.loads(rsp.content)
        gas_price = int(prices[style])

        return gas_price, status

    #catching requests failures
    except requests.exceptions.RequestException as e:
        msg = "request for gas price failed"
        return None, status
    