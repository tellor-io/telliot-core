import pytest
from brownie import accounts
from brownie import TellorXOracleMock

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorx.oracle import TellorxOracleContract
from telliot_core.utils.timestamp import TimeStamp


@pytest.fixture
def tellorx_oracle_mock_contract():
    """Reusable fixture for TellorXOracleMock contract"""
    return accounts[0].deploy(TellorXOracleMock)


@pytest.mark.asyncio
async def test_getReportTimestampByIndex(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorxOracleContract getReportTimestampByIndex method"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        index = 2
        timestamp, status = await oracle.getReportTimestampByIndex(queryId, index)
        assert status.ok
        assert isinstance(timestamp, int)
        print(timestamp)
        assert timestamp == 1234


@pytest.mark.asyncio
async def test_getReportingLock(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorxOracleContract.getReportingLock() method"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        result, status = await oracle.getReportingLock()
        assert status.ok
        assert result == 12
        print(result)


@pytest.mark.asyncio
async def test_gettimebasedreward(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorxOracleContract.getTimeBasedReward() method"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        result, status = await oracle.getTimeBasedReward()
        assert status.ok
        assert result == 1


@pytest.mark.asyncio
async def test_getCurrentReward(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorX oracle contract"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        (tips, reward), status = await oracle.getCurrentReward(queryId)

        assert status.ok
        assert tips == 1
        assert reward == 2


@pytest.mark.asyncio
async def test_getTimestampCountById(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorX oracle contract"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000001"
        result, status = await oracle.getTimestampCountById(queryId)

        assert status.ok
        assert result == 30


@pytest.mark.asyncio
async def test_getTimeOfLastNewValue(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorX oracle contract"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        result, status = await oracle.getTimeOfLastNewValue()

        assert status.ok
        assert isinstance(result, TimeStamp)
        assert result.ts == 123456789


@pytest.mark.asyncio
async def test_getTipsById(rinkeby_test_cfg, tellorx_oracle_mock_contract):
    """Test the TellorX oracle contract"""
    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        oracle = TellorxOracleContract(core.endpoint, account)
        oracle.address = tellorx_oracle_mock_contract.address  # Override with locally-deployed mock contract address
        oracle.connect()

        queryId = "0x0000000000000000000000000000000000000000000000000000000000000002"
        result, status = await oracle.getTipsById(queryId)

        assert status.ok
        assert result == 3
