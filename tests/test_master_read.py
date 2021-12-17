import pytest

from telliot_core.apps.master_read import getStakerInfo
from telliot_core.apps.master_read import staker_status_map


@pytest.mark.asyncio
async def test_get_staker_info(rinkeby_core):
    result, status = await getStakerInfo()
    assert status.ok
    assert len(result) == 2
    assert result[0] in staker_status_map.values()
    assert isinstance(result[1], int)
