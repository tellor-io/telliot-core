from datetime import datetime
from typing import Tuple

import click

from telliot_core.apps.core import TelliotCore
from telliot_core.cli.utils import async_run
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
    async with TelliotCore(chain_id=ctx.obj["chain_id"]) as core:

        result, status = await core.tellorx.oracle.getTimeBasedReward()

        if not status.ok:
            print(status)
        else:
            print(f"{result} TRB")


@oracle.command()
@click.option("--address", type=str, help="Reporter address (starting with 0x).")
@click.pass_context
@async_run
async def getteporterlasttimestamp(ctx: click.Context, address: str) -> None:
    async with TelliotCore(chain_id=ctx.obj["chain_id"]) as core:

        ts, status = await core.tellorx.oracle.getReporterLastTimestamp(address)

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

    async with TelliotCore(chain_id=ctx.obj["chain_id"]) as core:
        (staker_status, date_staked), status = await core.tellorx.oracle.getStakerInfo(
            address=address
        )
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

    async with TelliotCore(chain_id=ctx.obj["chain_id"]) as core:
        result, read_response = await core.tellorx.master.disputesById(dispute_id)

    if not read_response.ok:
        click.echo(read_response)
    else:
        click.echo(result)
