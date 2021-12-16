""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import click

import telliot_core
from telliot_core.cli.config import config
from telliot_core.cli.queryinfo import queryinfo
from telliot_core.cli.read import read
from telliot_core.plugin.discover import telliot_plugins


@click.group(invoke_without_command=True)
@click.pass_context
@click.option(
    "--chain_id",
    type=int,
    help="Override chain ID (the default is provided by main config file).",
)
@click.option(
    "-v", "--version", is_flag=True, help="Display telliot-core version and exit."
)
def main(ctx: click.Context, version: bool, chain_id: int) -> None:
    ctx.ensure_object(dict)
    ctx.obj["chain_id"] = chain_id
    if version:
        print(f"telliot-core: Version {telliot_core.__version__}")
        if len(telliot_plugins) > 1:
            for name, pkg in telliot_plugins.items():
                if name != "telliot_core":
                    try:
                        print(
                            f"{name} (plugin): Version {pkg.__version__}"  # type: ignore
                        )
                    except AttributeError:
                        print(f"{name} (plugin): Version UNKNOWN")

        return
    """Telliot command line interface"""
    if ctx.invoked_subcommand is None:
        print(ctx.command.get_help(ctx))


main.add_command(config)
main.add_command(read)
main.add_command(queryinfo)

if __name__ == "__main__":
    main()
