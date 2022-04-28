""" Listener Module

This module adds contract event listening capability for websocket endpoints
(like infura) that is lacking from web3.py.

The goal is to allow users to subscribe to and define async callbacks for each event.

*Work in Progress*
"""
import asyncio
import logging
import warnings
from typing import Any
from typing import Awaitable
from typing import Callable
from typing import List
from typing import Literal

import aiohttp
from aiohttp.client import _WSRequestContextManager
from hexbytes import HexBytes
from web3._utils.method_formatters import block_formatter
from web3._utils.method_formatters import log_entry_formatter
from web3._utils.method_formatters import syncing_formatter

logger = logging.getLogger(__name__)

AsyncCallable = Callable[[Any], Awaitable]

SubscriptionType = Literal["newHeads", "logs", "newPendingTransactions", "syncing"]


async def receive_message_task(
    ws: aiohttp.ClientWebSocketResponse,
    handler: AsyncCallable,
    formatter: Callable[..., Any],
) -> None:
    """A long running task that listens for JSON messages on an open websocket.
    The handler is called once for each message.

    Args:
        ws: Open websocket connection
        handler: An async function that takes the JSON message as a single argument
        formatter: An optional message formatter

    Returns: None
        Does not return until task is cancelled.

    """
    while True:
        try:
            message = await asyncio.wait_for(ws.receive_json(), timeout=60)
            # sub_id = message["params"]["subscription"]
            # logger.info(f"handled block subscription: {sub_id}")
            result = message["params"]["result"]
            formatted_result = formatter(result)
            asyncio.create_task(handler(formatted_result))  # type: ignore

        except asyncio.CancelledError:
            logger.debug("Listener cancelled")
            break
        except asyncio.exceptions.TimeoutError:
            continue


async def eth_subscribe(
    *,
    ws: aiohttp.ClientWebSocketResponse,
    name: SubscriptionType,
    lid: int = 1,
    **kwargs: Any,
) -> HexBytes:
    """Subscribe

    Args:
        ws: Websocket connection
        lid: Listener ID
        name: Subscription type/name, one of "newHeads", "logs", "newPendingTransactions", "syncing"
        **kwargs: Subscription parameter dict.  See (see https://geth.ethereum.org/docs/rpc/pubsub)

    Returns:
        Subscription ID

    """

    logger.debug(f"New {name} subscription")

    if kwargs:
        msg = {
            "jsonrpc": "2.0",
            "id": lid,
            "method": "eth_subscribe",
            "params": [name, kwargs],
        }
    else:
        msg = {"jsonrpc": "2.0", "id": lid, "method": "eth_subscribe", "params": [name]}
    await ws.send_json(msg)

    subscription_response = await ws.receive_json()

    lid_rx = subscription_response.get("id")
    assert lid_rx == lid

    sub_result = subscription_response.get("result")
    if not sub_result:
        logger.error("Subscription failed:")
        logger.error(subscription_response)
        raise Exception("Subscription Failed")

    return HexBytes(sub_result)


class Listener:
    def __init__(self, *, session: aiohttp.ClientSession, ws_url: str):

        self._session = session

        self._url: str = ws_url
        self._tasks: List[asyncio.Task[None]] = []
        self._listener_id: int = 0

    def connect(self) -> _WSRequestContextManager:  # aiohttp.ClientWebSocketResponse:
        return self._session.ws_connect(self._url)

    def _get_listener_id(self) -> int:
        """Generate sequential IDs for subscription requests"""
        self._listener_id += 1
        return self._listener_id

    async def eth_subscribe(
        self,
        handler: AsyncCallable,
        name: SubscriptionType,
        formatter: Callable[..., Any],
        **kwargs: Any,
    ) -> None:
        """Create a subscription using eth_subscribe

        Args:
            handler:
                An async function that takes the JSON message as a single argument
            name:
                Subscription type/name, one of:
                    "newHeads", "logs", "newPendingTransactions", "syncing"
            **kwargs:
                Subscription parameter dict.
                See (see https://geth.ethereum.org/docs/rpc/pubsub)

        Returns:

        """

        # Create a unique ID/name for the subscription
        lid = self._get_listener_id()
        task_name = f"listener_task_{lid}"

        # Launch a task and store a reference locally for later cancellation
        # Note that storing this reference delays exceptions until garbage collection.
        # Therefore, task is wrapped with a task_done callback to immediately catch exceptions
        task = asyncio.create_task(
            self._eth_subscribe_task(handler=handler, name=name, lid=lid, formatter=formatter, **kwargs),
            name=task_name,
        )

        task.add_done_callback(_handle_task_result)
        self._tasks.append(task)

    async def subscribe_new_blocks(self, handler: AsyncCallable) -> None:

        await self.eth_subscribe(handler=handler, name="newHeads", formatter=block_formatter)

    async def subscribe_contract_events(self, handler: AsyncCallable, address: str) -> None:

        await self.eth_subscribe(handler=handler, name="logs", address=address, formatter=log_entry_formatter)

    async def subscribe_pending_transactions(self, handler: AsyncCallable) -> None:

        await self.eth_subscribe(
            handler=handler,
            name="newPendingTransactions",
            formatter=pending_transaction_formatter,
        )
        # await self.eth_subscribe(handler=handler, name='newPendingTransactions')

    async def subscribe_syncing(self, handler: AsyncCallable) -> None:

        await self.eth_subscribe(handler=handler, name="syncing", formatter=syncing_formatter)

    async def _eth_subscribe_task(
        self,
        handler: AsyncCallable,
        name: SubscriptionType,
        lid: int,
        formatter: Callable[..., Any],
        **kwargs: Any,
    ) -> None:
        """A long running listener task.

        Note: Does not return until asyncio.Cancelled event
        """

        async with self.connect() as ws:
            sub_result = await eth_subscribe(ws=ws, name=name, lid=lid, **kwargs)
            if name == "logs":
                logger.info(f"Subscribed to contract address={kwargs['address']} (id={sub_result.hex()})")
            else:
                logger.info(f"New {name} subscription (id={sub_result.hex()})")
            await receive_message_task(ws=ws, handler=handler, formatter=formatter)

    async def shutdown(self) -> None:
        """Shut down all asyncio subscription tasks"""
        for task in self._tasks:
            logger.info(f"Shutting down listener {task.get_name()}")
            task.cancel()
        await asyncio.gather(*self._tasks)
        self._tasks = []

    def __del__(self) -> None:
        if self._tasks:
            warnings.warn("Listener.shutdown() not awaited.")


def _handle_task_result(task: asyncio.Task[Any]) -> None:
    # https://quantlane.com/blog/ensure-asyncio-task-exceptions-get-logged/
    try:
        task.result()
    except asyncio.CancelledError:
        pass  # Task cancellation should not be logged as an error.
    except Exception:
        logger.exception("Exception raised by task = %r", task)


async def event_logger(log: Any) -> None:
    # sub_id = msg["params"]["subscription"]
    # logger.info(f"handled block subscription: {sub_id}")
    # log_entry = msg["params"]["result"]
    # log_receipt: LogReceipt = log_entry_formatter(log_entry)
    logger.info(f"handled event message: {log}")


async def block_logger(block: Any) -> None:
    # sub_id = msg["params"]["subscription"]
    # logger.info(f"handled block subscription: {sub_id}")
    # block = msg["params"]["result"]
    logger.info(f"New block: {block}")


async def pending_transaction_logger(msg: Any) -> None:
    logger.info(f"New pending transaction: {msg!r}")


def pending_transaction_formatter(hash_str: str) -> HexBytes:
    return HexBytes(hash_str)


async def syncing_logger(msg: Any) -> None:
    logger.info(f"New sync: {msg}")


if __name__ == "__main__":
    from telliot_core.apps.core import TelliotCore
    import asyncio

    logging.basicConfig(level=logging.INFO)

    async def main() -> None:
        async with TelliotCore() as core:
            master_info = core.config.directory.find(name="tellorx-master", chain_id=core.config.main.chain_id)[0]
            oracle_info = core.config.directory.find(name="tellorx-oracle", chain_id=core.config.main.chain_id)[0]

            # Subscribe to blocks
            assert core.listener  # typing
            await core.listener.subscribe_new_blocks(handler=block_logger)
            # await core.listener.subscribe_syncing(handler=syncing_logger)

            # Subscribe to contract events
            await core.listener.subscribe_contract_events(
                handler=event_logger,
                address=master_info.address[core.config.main.chain_id],
            )
            await core.listener.subscribe_contract_events(
                handler=event_logger,
                address=oracle_info.address[core.config.main.chain_id],
            )

            # Subscribe to pending transactions:
            # Warning: Very high RPC transaction rate
            await core.listener.subscribe_pending_transactions(handler=pending_transaction_logger)

            await asyncio.sleep(1011)

    asyncio.run(main())
