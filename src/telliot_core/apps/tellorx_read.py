from telliot_core.apps.core import TelliotCore  # type: ignore
from telliot_core.utils.response import ResponseStatus
import asyncio
from typing import Optional, Tuple, Any


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


if __name__ == '__main__':
    app = TelliotCore()
    app.connect()
    r, s = asyncio.run(getStakerInfo('0xF754856Ed7751976447b3fA64eadeac4C7344CcD'))
    print(s)
    print(r)
