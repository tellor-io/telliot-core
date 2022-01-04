import asyncio
from telliot_core.apps.core import TelliotCore
from telliot_core.reporters.reporter_utils import tellorx_suggested_report
import pytest


@pytest.mark.asyncio
async def test_suggested_report(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        q = await tellorx_suggested_report(core.tellorx.oracle)
        print(q)
