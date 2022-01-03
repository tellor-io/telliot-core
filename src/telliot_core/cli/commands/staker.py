import click

from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.cli.commands.read import get_staker_info
from telliot_core.cli.utils import async_run


@click.group()
@click.pass_context
@click.option("--address", required=False, help="Staker address (beginning with 0x).")
def staker(ctx: click.Context, address: str) -> None:
    """Manage Telliot stakers."""
    ctx.obj["address"] = address


@staker.command()
@click.pass_context
@async_run
async def status(ctx: click.Context) -> None:
    """Get on-chain staker status"""
    address = ctx.obj.get("address", None)

    staker_status, date_staked = await get_staker_info(ctx, address)

    print(f"Status: {staker_status}")
    if staker_status != "NotStaked":
        print(f"Staked on {date_staked} ({date_staked.age} ago)")


@staker.command()
@click.pass_context
def list(ctx: click.Context) -> None:
    """Print a list of currently configured stakers."""
    cfg = TelliotConfig()
    stakers = cfg.stakers.find()

    taglen = max([len(s.tag) for s in stakers])

    print("Tag / Chain ID / Address")
    for s in stakers:
        print(f"{s.tag:{taglen}} {s.chain_id:3} {s.address}")
