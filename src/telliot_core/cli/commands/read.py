from datetime import datetime
from typing import Tuple

import click

from telliot_core.cli.utils import async_run
from telliot_core.cli.utils import cli_core
from telliot_core.utils.timestamp import TimeStamp


@click.group()
def read() -> None:
    """Read on-chain TellorX contracts."""
    pass


# ------------------------------------------------------------------
# Oracle Contract
# ------------------------------------------------------------------
@read.group()
def oracle() -> None:
    """Read from the TellorX oracle contract."""
    pass


@oracle.command()
@click.pass_context
@async_run
async def gettimebasedreward(ctx: click.Context) -> None:
    async with cli_core(ctx) as core:

        tellorx = core.get_tellorx_contracts()
        result, status = await tellorx.oracle.getTimeBasedReward()

        if not status.ok:
            print(status)
        else:
            print(f"{result} TRB")


@oracle.command()
@click.option("--address", type=str, help="Reporter address (starting with 0x).")
@click.pass_context
@async_run
async def getreporterlasttimestamp(ctx: click.Context, address: str) -> None:
    async with cli_core(ctx) as core:

        tellorx = core.get_tellorx_contracts()
        ts, status = await tellorx.oracle.getReporterLastTimestamp(address)

        if not status.ok:
            print(status)
        else:
            print(f"{ts} ({datetime.fromtimestamp(ts)})")


# ------------------------------------------------------------------
# Master Contract
# ------------------------------------------------------------------
@read.group()
def master() -> None:
    """Read from the TellorX master contract."""
    pass


async def get_staker_info(ctx: click.Context, address: str) -> Tuple[str, TimeStamp]:
    """Get staker information."""
    async with cli_core(ctx) as core:
        if not address:
            address = core.get_account().address

        tellorx = core.get_tellorx_contracts()
        (staker_status, date_staked), status = await tellorx.master.getStakerInfo(address=address)
        return staker_status, date_staked


@master.command()
@click.argument("address", required=False)
@click.pass_context
@async_run
async def getstakerinfo(ctx: click.Context, address: str) -> None:
    """Get staker information."""
    (staker_status, date_staked) = await get_staker_info(ctx, address)

    print(f"Status: {staker_status}")
    if staker_status != "NotStaked":
        print(f"Staked on {date_staked} ({date_staked.age} ago)")


@master.command()
@click.argument("dispute_id", type=int, required=True)
@click.pass_context
@async_run
async def disputesbyid(ctx: click.Context, dispute_id: int) -> None:
    """Get disputes by ID."""

    async with cli_core(ctx) as core:
        tellorx = core.get_tellorx_contracts()
        result, read_response = await tellorx.master.disputesById(dispute_id)

    if not read_response.ok:
        click.echo(read_response)
    else:
        click.echo(result)
