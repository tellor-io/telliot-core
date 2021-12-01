from typing import Any
from typing import Optional
from typing import Tuple

from telliot_core.apps.core import TelliotCore  # type: ignore
from telliot_core.utils.response import ResponseStatus


async def getTimeBasedReward() -> Tuple[Any, ResponseStatus]:
    core = TelliotCore.get()
    result, status = await core.tellorx.oracle.read("getTimeBasedReward")
    if status.ok:
        trb_reward = result / 1.0e18
    else:
        trb_reward = result
    return trb_reward, status


async def getStakerInfo(address: Optional[str] = None) -> Tuple[Any, ResponseStatus]:
    core = TelliotCore.get()

    if address is None:
        staker = core.get_default_staker()
        address = staker.address

    result, status = await core.tellorx.master.read("getStakerInfo", _staker=address)

    return result, status
