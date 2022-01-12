import pytest

from telliot_core.apps.core import TelliotCore
from telliot_core.contract.listener import event_logger, block_logger
import asyncio
import logging


async def block_printer(msg) -> None:
    sub_id = msg["params"]["subscription"]
    block = msg["params"]["result"]
    print(f"handled block subscription: {sub_id}")
    print(block)


@pytest.mark.asyncio
async def test_subscribe_new_blocks(caplog):
    caplog.set_level(logging.INFO)
    async with TelliotCore() as core:
        # Subscribe to blocks
        await core.listener.subscribe_new_blocks(handler=block_logger)
        await asyncio.sleep(1)  # Note delay needed

    print(caplog.text)
