import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.tellorx.master import staker_status_map
from telliot_core.utils.timestamp import TimeStamp


@pytest.mark.asyncio
async def test_get_staker_info(rinkeby_cfg):

    async with TelliotCore(config=rinkeby_cfg) as core:

        staker = core.get_default_staker()
        address = staker.address

        result, status = await core.tellorx.master.getStakerInfo(address)
        assert status.ok
        assert len(result) == 2
        assert result[0] in staker_status_map.values()
        assert isinstance(result[1], TimeStamp)
