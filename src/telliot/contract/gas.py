'''Utils for gas calculations'''

import json
from typing import Optional, Tuple

import requests
from telliot.utils.response import ResponseStatus


def fetch_gas_price() -> Tuple[ResponseStatus, Optional[int]]:
    '''Fetch network gas price from RPC endpoint or an API'''

    try:
        status = ResponseStatus()
        # get gas price
        rsp = requests.get("https://ethgasstation.info/json/ethgasAPI.json")
        prices = json.loads(rsp.content)
        return status, int(prices["fast"])
    except requests.exceptions.RequestException as e:
        status.ok = False
        status.error = "request for gas price failed"
        status.e = e
        return status, None
        



