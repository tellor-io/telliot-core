import click

from telliot_core.apps.staker import Staker
from telliot_core.apps.telliot_config import TelliotConfig
from telliot_core.cli.commands.read import get_staker_info
from telliot_core.cli.utils import async_run
from telliot_core.cli.utils import cli_config


@click.group()
@click.pass_context
@click.option(
    "-sa",
    "--staker_address",
    required=False,
    help="Staker address (beginning with 0x).",
)
@click.option("-st", "--staker_tag", required=False, help="Staker tag.")
def staker(ctx: click.Context, staker_address: str, staker_tag: str) -> None:
    """Manage Telliot stakers."""
    ctx.obj["STAKER_ADDRESS"] = staker_address
    ctx.obj["STAKER_TAG"] = staker_tag

    # If address not provided, try to get it from tag
    staker_tag = ctx.obj.get("STAKER_TAG", None)
    if staker_tag and not staker_address:
        cfg = cli_config(ctx)
        stakers = cfg.stakers.find(tag=staker_tag)
        if not stakers:
            print(f"Staker {staker_tag} not found.")
            return
        else:
            staker_obj = stakers[0]
            assert isinstance(staker_obj, Staker)
            ctx.obj["STAKER_ADDRESS"] = staker_obj.address


@staker.command()
@click.pass_context
@async_run
async def status(ctx: click.Context) -> None:
    """Get on-chain staker status."""

    staker_address = ctx.obj.get("STAKER_ADDRESS", None)
    staker_tag = ctx.obj.get("STAKER_TAG", None)

    staker_status, date_staked = await get_staker_info(ctx, staker_address)

    if not staker_status:
        print("Failed to retrieve staker status.  Check command arguments")
        return

    if staker_tag:
        print(f"Staker tag: {staker_tag}")
    if staker_address:
        print(f"Staker address: {staker_address}")

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
