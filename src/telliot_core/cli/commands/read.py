import asyncio

import click

from telliot_core.apps.master_read import getStakerInfo
from telliot_core.apps.oracle_read import getTimeBasedReward
from telliot_core.cli.utils import get_app


@click.group()
def read() -> None:
    """Execute a command"""
    pass


@read.command()
@click.pass_context
def gettimebasedreward(ctx: click.Context) -> None:
    _ = get_app(ctx)  # Initialize app

    result, status = asyncio.run(getTimeBasedReward())

    if not status.ok:
        print(status)
    else:
        print(f"{result} TRB")


@read.command()
@click.argument("address", required=False)
@click.pass_context
def getstakerinfo(ctx: click.Context, address: str) -> None:
    _ = get_app(ctx)  # Initialize app
    result, read_response = asyncio.run(getStakerInfo(address=address))

    if not read_response.ok:
        print(read_response)
    else:
        print(result)
