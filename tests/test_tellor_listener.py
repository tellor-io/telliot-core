import asyncio
import logging

import pytest

from telliot_core.contract.tellor_listener import tellor_listener_client

logger = logging.getLogger(__name__)

logging.basicConfig(level=logging.INFO)


@pytest.mark.skip("Doesn't work in pytest")
def test_main(rinkeby_cfg, caplog):
    caplog.set_level(logging.INFO)

    url = rinkeby_cfg.get_endpoint().url

    async def run_listener() -> None:
        task = asyncio.create_task(tellor_listener_client(ws_url=url, chain_id=4))

        # Wait for 1 second
        await asyncio.sleep(120)

        task.cancel()

        try:
            logger.info("awaiting task")
            await task
        except asyncio.CancelledError:
            logger.info("run_listener(): Task cancelled")

    asyncio.run(run_listener())


@pytest.mark.skip("TODO")
def test_tellor_listener(rinkeby_cfg, event_loop, caplog):
    caplog.set_level(logging.INFO)
    print(rinkeby_cfg)

    from telliot_core.apps.telliot_config import TelliotConfig

    rinkeby_cfg = TelliotConfig()
    rinkeby_cfg.main.chain_id = 4

    url = rinkeby_cfg.get_endpoint().url

    async def run_listener():

        task = event_loop.create_task(tellor_listener_client(ws_url=url, chain_id=4))

        # Wait for 1 second
        await asyncio.sleep(30)

        task.cancel()

        try:
            logger.info("awaiting task")
            await task
        except asyncio.CancelledError:
            logger.info("run_listener(): Task cancelled")

    event_loop.run_until_complete(run_listener())
