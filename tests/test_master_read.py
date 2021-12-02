import pytest

from telliot_core.apps.master_read import getStakerInfo


@pytest.mark.asyncio
async def test_get_staker_info(rinkeby_core):
    result, status = await getStakerInfo()
    assert status.ok
    assert len(result) == 2
    assert isinstance(result[0], int)
    assert isinstance(result[1], int)
