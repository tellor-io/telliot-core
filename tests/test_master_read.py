import pytest
from brownie import accounts
from brownie import TellorXMasterMock

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorx.master import account_status_map
from telliot_core.tellor.tellorx.master import TellorxMasterContract
from telliot_core.utils.timestamp import TimeStamp


@pytest.fixture
def tellorx_master_mock_contract():
    """Mock the TellorXMaster contract"""
    return accounts[0].deploy(TellorXMasterMock)


@pytest.mark.asyncio
async def test_get_staker_info(rinkeby_test_cfg, tellorx_master_mock_contract):
    """Test the TellorXMaster contract"""

    async with TelliotCore(config=rinkeby_test_cfg) as core:
        account = core.get_account()
        tellorx = TellorxMasterContract(core.endpoint, account)
        tellorx.address = tellorx_master_mock_contract.address
        tellorx.connect()

        result, status = await tellorx.getStakerInfo(tellorx.address)

        assert status.ok
        assert len(result) == 2
        assert result[0] in account_status_map.values()
        assert isinstance(result[1], TimeStamp)
