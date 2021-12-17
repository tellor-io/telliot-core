import click
from telliot_core.cli.commands.read import get_staker_info


@click.group()
@click.pass_context
@click.option("--address", required=False, help="Staker address (beginning with 0x).")
def staker(ctx: click.Context, address: str) -> None:
    """Manage Telliot stakers."""
    ctx.obj['address'] = address


@staker.command()
@click.pass_context
def status(ctx: click.Context) -> None:
    address = ctx.obj.get('address', None)

    staker_status, date_staked = get_staker_info(ctx, address)

    print(f"Status: {staker_status}")
    if staker_status != "NotStaked":
        print(f"Staked on {date_staked} ({date_staked.age} ago)")
