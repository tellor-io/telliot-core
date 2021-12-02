from typing import Optional

from telliot_core.apps.core import TelliotCore  # type: ignore
from telliot_core.apps.oracle_read import ReadRespType


async def getStakerInfo(address: Optional[str] = None) -> ReadRespType:
    core = TelliotCore.get()

    if address is None:
        staker = core.get_default_staker()
        address = staker.address

    result, status = await core.tellorx.master.read("getStakerInfo", _staker=address)

    return result, status


async def disputesById(value: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.master.read("disputesById", value)

    return result, status
