import asyncio

import click

from telliot_core.cli.utils import async_run
from telliot_core.cli.utils import cli_core
from telliot_core.contract.listener import event_logger
from telliot_core.directory import contract_directory


@click.command()
@click.pass_context
@async_run
async def listen(ctx: click.Context) -> None:
    """Listen for Tellor network events."""

    async with cli_core(ctx) as core:

        chain_id = core.config.main.chain_id

        if chain_id in [1, 4]:

            master = contract_directory.find(name="tellorx-master", chain_id=chain_id)[0]
            oracle = contract_directory.find(name="tellorx-oracle", chain_id=chain_id)[0]

        # elif chain_id in [137, 80001]:
        #     oracle = contract_directory.find(name='tellorflex-oracle', chain_id=chain_id)[0]

        else:
            click.echo(f"Listening not supported on network: {chain_id}")
            return

        # await core.listener.subscribe_new_blocks(handler=block_logger)

        # Subscribe to contract events
        await core.listener.subscribe_contract_events(
            handler=event_logger,
            address=master.address[core.config.main.chain_id],
        )
        await core.listener.subscribe_contract_events(
            handler=event_logger,
            address=oracle.address[core.config.main.chain_id],
        )

        try:
            while True:
                await asyncio.sleep(1)

        except asyncio.exceptions.CancelledError:
            core.log.debug("CLI Listener cancelled.")
