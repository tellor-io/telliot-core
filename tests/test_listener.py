import asyncio
import logging

import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.contract.listener import block_logger


async def block_printer(msg) -> None:
    """Print block info"""
    sub_id = msg["params"]["subscription"]
    block = msg["params"]["result"]
    print(f"handled block subscription: {sub_id}")
    print(block)


@pytest.mark.asyncio
async def test_subscribe_new_blocks(caplog, amoy_test_cfg):
    """Test the block listener"""
    caplog.set_level(logging.INFO)
    async with TelliotCore(config=amoy_test_cfg) as core:
        # Subscribe to blocks
        await core.listener.subscribe_new_blocks(handler=block_logger)
        await asyncio.sleep(1)  # Note delay needed

    print(caplog.text)
