import asyncio
from datetime import datetime

import click

from telliot_core.apps.master_read import disputesById
from telliot_core.apps.master_read import getStakerInfo
from telliot_core.apps.oracle_read import getReporterLastTimestamp
from telliot_core.apps.oracle_read import getTimeBasedReward
from telliot_core.cli.utils import get_app


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
def gettimebasedreward(ctx: click.Context) -> None:
    _ = get_app(ctx)  # Initialize app

    result, status = asyncio.run(getTimeBasedReward())

    if not status.ok:
        print(status)
    else:
        print(f"{result} TRB")


@oracle.command()
@click.option("--address", type=str, help="Reporter address (starting with 0x).")
@click.pass_context
def getteporterlasttimestamp(ctx: click.Context, address: str) -> None:
    _ = get_app(ctx)  # Initialize app

    ts, status = asyncio.run(getReporterLastTimestamp(address))

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


@master.command()
@click.argument("address", required=False)
@click.pass_context
def getstakerinfo(ctx: click.Context, address: str) -> None:
    """Get staker information."""
    _ = get_app(ctx)  # Initialize app
    result, read_response = asyncio.run(getStakerInfo(address=address))

    if not read_response.ok:
        print(read_response)
    else:
        status, ts_staked = result
        date_staked = datetime.fromtimestamp(ts_staked)
        length_staked = datetime.now() - date_staked  # todo: check timezone
        print(f"Status: {status}")
        print(f"Date Staked: {ts_staked} ({datetime.fromtimestamp(ts_staked)})")
        print(
            f"Staked for: {length_staked.days} days, "
            f"{round(length_staked.seconds / 60.0 / 60.0, 2)} hours"
        )


@master.command()
@click.argument("dispute_id", type=int, required=True)
@click.pass_context
def disputesbyid(ctx: click.Context, dispute_id: int) -> None:
    """Get disputes by ID."""
    _ = get_app(ctx)  # Initialize app
    result, read_response = asyncio.run(disputesById(dispute_id))

    if not read_response.ok:
        print(read_response)
    else:
        print(result)
