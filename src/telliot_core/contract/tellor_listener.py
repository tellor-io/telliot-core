import asyncio
import logging

from telliot_core.contract.listener import AddressEventListener
from telliot_core.contract.listener import event_message_handler
from telliot_core.contract.listener import listener_client
from telliot_core.directory.tellorx import tellor_directory

logger = logging.getLogger("__name__")


async def tellor_listener_client(ws_url: str, chain_id: int) -> None:
    master_info = tellor_directory.find(name="master", chain_id=chain_id)[0]
    oracle_info = tellor_directory.find(name="oracle", chain_id=chain_id)[0]

    listeners = [
        AddressEventListener(
            address=master_info.address, handler=event_message_handler
        ),
        AddressEventListener(
            address=oracle_info.address, handler=event_message_handler
        ),
    ]

    await listener_client(ws_url=ws_url, listeners=listeners)


if __name__ == "__main__":

    logging.basicConfig(level=logging.INFO)
    logger.info("begin test")
    from telliot_core.apps.telliot_config import TelliotConfig

    rinkeby_cfg = TelliotConfig()
    rinkeby_cfg.main.chain_id = 4

    ep = rinkeby_cfg.get_endpoint()
    if ep:
        url = ep.url

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
