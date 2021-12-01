""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import asyncio

import click
import yaml

import telliot_core
from telliot_core.apps.app import BaseApplication
from telliot_core.apps.telliot_config import TelliotConfig


def get_app(ctx: click.Context) -> BaseApplication:
    """Get an app configured using CLI context"""

    app = BaseApplication(name="CLI")
    chain_id = ctx.obj["chain_id"]
    if chain_id is not None:
        assert app.config
        app.config.main.chain_id = chain_id
    _ = app.connect()

    assert app.config
    assert app.tellorx

    return app


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
        print(f"Version {telliot_core.__version__}")
        return
    """Telliot command line interface"""
    if ctx.invoked_subcommand is None:
        print(ctx.command.get_help(ctx))


@main.group()
def config() -> None:
    """Manage telliot_core configuration"""
    pass


@config.command()
def init() -> None:
    """Create initial configuration files"""
    _ = TelliotConfig()


@config.command()
def show() -> None:
    """Create initial configuration files"""
    cfg = TelliotConfig()
    print(yaml.dump(cfg.get_state(), sort_keys=False))


@main.group()
def read() -> None:
    """Execute a command"""
    pass


@read.command()
@click.argument("address")
@click.pass_context
def getstakerinfo(ctx: click.Context, address: str) -> None:

    app = get_app(ctx)

    result, read_response = asyncio.run(
        app.tellorx.master.read("getStakerInfo", _staker=address)  # type: ignore
    )
    if not read_response.ok:
        print(read_response)
    else:
        print(result)


@read.command()
@click.pass_context
def gettimebasedreward(ctx: click.Context) -> None:

    app = get_app(ctx)

    result, read_response = asyncio.run(
        app.tellorx.oracle.read("getTimeBasedReward")  # type: ignore
    )

    if not read_response.ok:
        print(read_response)
    else:
        trb_reward = result / 1.0e18
        print(f"{trb_reward} TRB")


if __name__ == "__main__":
    main()
