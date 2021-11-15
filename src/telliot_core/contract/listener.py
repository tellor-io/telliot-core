import asyncio
from dataclasses import dataclass
from typing import Callable, List
import logging
import aiohttp
from web3._utils.method_formatters import log_entry_formatter

logger = logging.getLogger('__name__')


async def event_message_handler(msg):
    log_receipt = log_entry_formatter(msg)
    logger.info(f'handled event message: {log_receipt}')


async def subscribe_contract_events(ws, contract_address):
    logger.info(f"Subscribing to contract events at address {contract_address}")
    request = {"jsonrpc": "2.0",
               "id": 1,
               "method": "eth_subscribe",
               "params": ["logs", {"address": contract_address}]
               }

    await ws.send_json(request)

    subscription_response = await ws.receive_json()
    sub_id = subscription_response.get("id")
    sub_result = subscription_response.get("result")
    logger.info(f"Subscription complete: result={sub_result} for address {contract_address}")


async def subscribe_blocks(ws):
    logger.info(f"Subscribing to newHeads")

    msg = {"jsonrpc": "2.0", "id": 1, "method": "eth_subscribe", "params": ["newHeads"]}

    await ws.send_json(msg)

    subscription_response = await ws.receive_json()
    sub_id = subscription_response.get("id")
    sub_result = subscription_response.get("result")

    logger.info(f"newHead subscription complete: result={sub_result}")


async def receive_messages(ws, handler):
    while True:
        try:
            message = await asyncio.wait_for(ws.receive_json(), timeout=60)
            await handler(message)
        except asyncio.CancelledError:
            logger.debug('Listener cancelled')
            raise
        except asyncio.exceptions.TimeoutError:
            logger.debug('Listener Timed out, restarting.')
            continue


async def block_listener(session, ws_url):
    async def block_message_handler(msg):
        sub_id = msg['params']['subscription']
        logger.info(f"handled block subscription: {sub_id}")

    async with session.ws_connect(ws_url) as ws2:
        await subscribe_blocks(ws2)
        await receive_messages(ws2, block_message_handler)


async def contract_event_listener(session, ws_url, address, message_handler):
    async with session.ws_connect(ws_url) as ws1:
        await subscribe_contract_events(ws1, address)
        await receive_messages(ws1, message_handler)


@dataclass
class AddressEventListener:
    """ A listener that handles all event logs from a contract address

    """

    #: Contract address
    address: str

    #: Handler that takes the received JSON message a single argument
    handler: Callable


async def listener_client(ws_url: str, chain_id: int, listeners: List[AddressEventListener]):
    async with aiohttp.ClientSession() as session:
        logger.info("Listener session created")

        tasks = [block_listener(session, ws_url)]
        for listener in listeners:
            tasks.append(contract_event_listener(session, ws_url, listener.address, listener.handler))

        await asyncio.gather(*tasks)
