from typing import Any
from typing import Optional
from typing import Tuple

from telliot_core.apps.core import TelliotCore  # type: ignore
from telliot_core.utils.response import ResponseStatus

ReadRespType = Tuple[Any, ResponseStatus]


# ----------------------------------------------------------------------------------------------
# Oracle getters
# ----------------------------------------------------------------------------------------------


async def getBlockNumberByTimestamp(queryId: str, timestamp: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getBlockNumberByTimestamp", _queryId=queryId, _timestamp=timestamp
    )

    return result, status


async def getCurrentReward(queryId: str) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getCurrentReward", _queryId=queryId
    )

    if status.ok:
        (tips, reward) = result
        return (tips / 1.0e18, reward / 1.0e18), status
    else:
        return (0, 0), status


async def getCurrentValue(queryId: str) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read("getCurrentValue", _queryId=queryId)

    return result, status


async def getReportingLock() -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read("getReportingLock")

    return result, status


async def getReporterByTimestamp(queryId: str, timestamp: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getReporterByTimestamp", _queryId=queryId, _timestamp=timestamp
    )

    return result, status


async def getReporterLastTimestamp(reporter: Optional[str] = None) -> ReadRespType:
    core = TelliotCore.get()

    if reporter is None:
        staker = core.get_default_staker()
        reporter = staker.address

    result, status = await core.tellorx.oracle.read(
        "getReporterLastTimestamp", _reporter=reporter
    )

    return result, status


async def getReportsSubmittedByAddress(reporter: Optional[str] = None) -> ReadRespType:
    core = TelliotCore.get()

    if reporter is None:
        staker = core.get_default_staker()
        reporter = staker.address

    result, status = await core.tellorx.oracle.read(
        "getReportsSubmittedByAddress", _reporter=reporter
    )

    return result, status


async def getReportTimestampByIndex(queryId: str, index: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getReportTimestampByIndex", _queryId=queryId, _index=index
    )

    return result, status


async def getTimeBasedReward() -> ReadRespType:
    core = TelliotCore.get()
    result, status = await core.tellorx.oracle.read("getTimeBasedReward")
    if status.ok:
        trb_reward = result / 1.0e18
    else:
        trb_reward = result
    return trb_reward, status


async def getTimestampCountById(queryId: str) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getTimestampCountById", _queryId=queryId
    )

    return result, status


async def getTimeOfLastNewValue() -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read("getTimeOfLastNewValue")

    return result, status


async def getTimestampIndexByTimestamp(queryId: str, timestamp: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getTimestampIndexByTimestamp", _queryId=queryId, _timestamp=timestamp
    )

    return result, status


async def getTipsById(queryId: str) -> ReadRespType:
    core = TelliotCore.get()

    tips, status = await core.tellorx.oracle.read("getTipsById", _queryId=queryId)

    return tips / 1.0e18, status


async def getTipsByUser(user: Optional[str] = None) -> ReadRespType:
    core = TelliotCore.get()

    if user is None:
        staker = core.get_default_staker()
        user = staker.address

    result, status = await core.tellorx.oracle.read("getTipsByUser", _user=user)

    return result, status


async def getValueByTimestamp(queryId: str, timestamp: int) -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read(
        "getValueByTimestamp", _queryId=queryId, _timestamp=timestamp
    )

    return result, status


async def verify() -> ReadRespType:
    core = TelliotCore.get()

    result, status = await core.tellorx.oracle.read("verify")

    return result, status
