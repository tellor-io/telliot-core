""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import click

from telliot_core.cli.commands.account import account
from telliot_core.cli.commands.config import config
from telliot_core.cli.commands.listen import listen
from telliot_core.cli.commands.read import read
from telliot_core.utils.versions import show_telliot_versions


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--chain_id",
    type=int,
    help="Override chain ID (the default is provided by main config file).",
)
@click.option(
    "--test_config",
    is_flag=True,
    help="Runs command with test configuration (developer use only)",
)
@click.option("--version", is_flag=True, help="Display telliot-core version and exit.")
def main(ctx: click.Context, version: bool, chain_id: int, test_config: bool) -> None:
    ctx.ensure_object(dict)
    ctx.obj["CHAIN_ID"] = chain_id
    ctx.obj["TEST_CONFIG"] = test_config
    if version:
        show_telliot_versions()
        return

    """Telliot command line interface"""
    if ctx.invoked_subcommand is None:
        print(ctx.command.get_help(ctx))


main.add_command(config)
main.add_command(read)
main.add_command(account)
main.add_command(listen)

if __name__ == "__main__":
    main()
