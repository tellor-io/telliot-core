import click
from chained_accounts import ChainedAccount
from chained_accounts import find_accounts

from telliot_core.cli.commands.read import get_staker_info
from telliot_core.cli.utils import async_run
from telliot_core.cli.utils import cli_config


@click.group()
@click.pass_context
@click.option("-n", "--name", required=False, help="ChainedAccount name.")
def staker(ctx: click.Context, name: str) -> None:
    """Manage Telliot stakers."""
    ctx.obj["ACCOUNT_NAME"] = name


@staker.command()
@click.pass_context
@async_run
async def status(ctx: click.Context) -> None:
    """Get on-chain staker status."""
    cfg = cli_config(ctx)
    account_name = ctx.obj["ACCOUNT_NAME"]
    if account_name:
        account = ChainedAccount.get(account_name)
    else:
        accounts = find_accounts(chain_id=cfg.main.chain_id)
        account = accounts[0]

    staker_status, date_staked = await get_staker_info(ctx, account.address)

    if not staker_status:
        print("Failed to retrieve staker status.  Check command arguments")
        return

    if account_name:
        print(f"Account name: {account_name}")

    print(f"Status: {staker_status}")
    if staker_status != "NotStaked":
        print(f"Staked on {date_staked} ({date_staked.age} ago)")
