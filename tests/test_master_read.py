import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.tellor.tellorx.master import staker_status_map
from telliot_core.utils.timestamp import TimeStamp


@pytest.mark.asyncio
async def test_get_staker_info(rinkeby_cfg):

    async with TelliotCore(config=rinkeby_cfg) as core:
        tellorx = core.get_tellorx_contracts()

        account = core.get_account()
        address = account.address

        result, status = await tellorx.master.getStakerInfo(address)
        assert status.ok
        assert len(result) == 2
        assert result[0] in staker_status_map.values()
        assert isinstance(result[1], TimeStamp)
