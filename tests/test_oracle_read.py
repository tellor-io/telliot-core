import pytest

from telliot_core.apps.oracle_read import getBlockNumberByTimestamp
from telliot_core.apps.oracle_read import getCurrentReward
from telliot_core.apps.oracle_read import getReportingLock
from telliot_core.apps.oracle_read import getReportTimestampByIndex
from telliot_core.apps.oracle_read import getTimeBasedReward
from telliot_core.apps.oracle_read import getTimeOfLastNewValue
from telliot_core.apps.oracle_read import getTimestampCountById
from telliot_core.apps.oracle_read import getTipsById


@pytest.mark.asyncio
async def test_getReportTimestampByIndex(rinkeby_core):
    queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
    index = 2
    timestamp, status = await getReportTimestampByIndex(queryId, index)
    assert status.ok
    assert isinstance(timestamp, int)
    print(timestamp)
    assert timestamp > 0


@pytest.mark.asyncio
async def test_getReportingLock(rinkeby_core):
    result, status = await getReportingLock()
    assert status.ok
    print(result)


@pytest.mark.asyncio
async def test_gettimebasedreward(rinkeby_core):
    result, status = await getTimeBasedReward()
    assert status.ok
    print(result)


@pytest.mark.asyncio
async def test_getCurrentReward(rinkeby_core):
    queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
    (tips, reward), status = await getCurrentReward(queryId)
    assert status.ok
    print(tips)
    print(reward)


@pytest.mark.asyncio
async def test_getBlockNumberByTimestamp(rinkeby_core):
    queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
    timestamp = 1638377944
    result, status = await getBlockNumberByTimestamp(queryId, timestamp)
    assert status.ok
    print(result)


@pytest.mark.asyncio
async def test_getTimestampCountById(rinkeby_core):
    queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
    result, status = await getTimestampCountById(queryId)
    print(result)
    assert status.ok
    assert result > 30


@pytest.mark.asyncio
async def test_getTimeOfLastNewValue(rinkeby_core):
    result, status = await getTimeOfLastNewValue()
    assert status.ok
    print(result)


@pytest.mark.asyncio
async def test_getTipsById(rinkeby_core):
    queryId = "0x0000000000000000000000000000000000000000000000000000000000000002"
    result, status = await getTipsById(queryId)
    print(result)
    assert status.ok
