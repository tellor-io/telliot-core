"""
Test covering Pytelliot EVM contract connection utils.
"""
import pytest
import web3

from telliot_core.apps.core import TelliotCore


@pytest.mark.asyncio
async def test_connect_to_tellor(rinkeby_cfg):
    """Contract object should access Tellor functions"""
    async with TelliotCore(config=rinkeby_cfg) as core:
        assert len(core.tellorx.master.contract.all_functions()) > 0
        assert isinstance(
            core.tellorx.master.contract.all_functions()[0],
            web3.contract.ContractFunction,
        )


@pytest.mark.asyncio
async def test_call_read_function(rinkeby_cfg):
    """Contract object should be able to call arbitrary contract read function"""

    async with TelliotCore(config=rinkeby_cfg) as core:
        (reward, tips), status = await core.tellorx.oracle.read(
            func_name="getCurrentReward",
            _queryId="0x0000000000000000000000000000000000000000000000000000000000000001",
        )
        assert status.ok
        assert reward >= 0
