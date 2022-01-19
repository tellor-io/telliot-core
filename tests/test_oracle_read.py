import pytest

from telliot_core.apps.core import TelliotCore


@pytest.mark.asyncio
async def test_getReportTimestampByIndex(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        index = 2
        timestamp, status = await tellorx.oracle.getReportTimestampByIndex(queryId, index)
        assert status.ok
        assert isinstance(timestamp, int)
        print(timestamp)
        assert timestamp > 0


@pytest.mark.asyncio
async def test_getReportingLock(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        result, status = await tellorx.oracle.getReportingLock()
        assert status.ok
        print(result)


@pytest.mark.asyncio
async def test_gettimebasedreward(rinkeby_cfg):

    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        result, status = await tellorx.oracle.getTimeBasedReward()
        assert status.ok
        print(result)


@pytest.mark.asyncio
async def test_getCurrentReward(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        (tips, reward), status = await tellorx.oracle.getCurrentReward(queryId)
        assert status.ok
        print(tips)
        print(reward)


@pytest.mark.asyncio
async def test_getBlockNumberByTimestamp(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        timestamp = 1638377944
        result, status = await tellorx.oracle.getBlockNumberByTimestamp(queryId, timestamp)
        assert status.ok
        print(result)


@pytest.mark.asyncio
async def test_getTimestampCountById(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        result, status = await tellorx.oracle.getTimestampCountById(queryId)
        print(result)
        assert status.ok
        assert result > 30


@pytest.mark.asyncio
async def test_getTimeOfLastNewValue(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()
        result, status = await tellorx.oracle.getTimeOfLastNewValue()
        assert status.ok
        print(result)


@pytest.mark.asyncio
async def test_getTipsById(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000002"
        result, status = await tellorx.oracle.getTipsById(queryId)
        print(result)
        assert status.ok
