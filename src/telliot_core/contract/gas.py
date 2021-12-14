import json
from typing import Literal, Tuple

import requests

ethgastypes = Literal["SafeGasPrice", "ProposeGasPrice", "FastGasPrice"]


async def fetch_gas_price() -> int:
    """Estimate current ETH gas price

    Current implementation fetches from ethgasstation

    Returns:
        eth gas price in gwei
    """
    return await etherscan_gas_api("fast")


async def etherscan_gas_api(style: ethgastypes = "FastGasPrice") -> Tuple[int]:
    """Fetch gas price from ethgasstation in gwei"""
    rsp = requests.get("https://api.etherscan.io/api?module=gastracker&action=gasoracle")
    json_ = json.loads(rsp.content)

    base_fee = int(json_["result"]["suggestBaseFee"])
    priority_fee = int(json_["result"][style])

    return base_fee, priority_fee
