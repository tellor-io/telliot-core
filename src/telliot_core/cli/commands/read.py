import asyncio
from datetime import datetime
from typing import Tuple

import click

from telliot_core.apps.master_read import disputesById
from telliot_core.apps.master_read import getStakerInfo
from telliot_core.apps.oracle_read import getReporterLastTimestamp
from telliot_core.apps.oracle_read import getTimeBasedReward
from telliot_core.cli.utils import get_app
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


def get_staker_info(ctx: click.Context, address: str) -> Tuple[str, TimeStamp]:
    """Get staker information."""
    _ = get_app(ctx)  # Initialize app

    (staker_status, date_staked), status = asyncio.run(getStakerInfo(address=address))

    return staker_status, date_staked


@master.command()
@click.argument("address", required=False)
@click.pass_context
def getstakerinfo(ctx: click.Context, address: str) -> None:
    """Get staker information."""
    (staker_status, date_staked) = get_staker_info(ctx, address)

    print(f"Status: {staker_status}")
    if staker_status != "NotStaked":
        print(f"Staked on {date_staked} ({date_staked.age} ago)")

    # _ = get_app(ctx)  # Initialize app
    # result, read_response = asyncio.run(getStakerInfo(address=address))
    #
    # if not read_response.ok:
    #     print(read_response)
    # else:
    #     status, date_staked = result
    #     print(f"Status: {status}")
    #     if status is not "NotStaked":
    #         print(f"Staked on {date_staked} ({date_staked.age} ago)")


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
