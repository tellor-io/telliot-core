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


@click.group(invoke_without_command=True)
@click.pass_context
def main(ctx: click.Context) -> None:
    """Telliot command line interface"""
    print(f"Telliot Core Version {telliot_core.__version__}")
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
def getstakerinfo(address: str) -> None:
    app = BaseApplication(name="CLI")
    _ = app.connect()

    assert app.tellorx

    result, read_response = asyncio.run(
        app.tellorx.master.read("getStakerInfo", _staker=address)
    )
    if not read_response.ok:
        print(read_response)
    else:
        print(result)


@read.command()
def gettimebasedreward() -> None:
    app = BaseApplication(name="CLI")
    _ = app.connect()
    assert app.tellorx is not None

    result, read_response = asyncio.run(app.tellorx.oracle.read("getTimeBasedReward"))

    if not read_response.ok:
        print(read_response)
    else:
        trb_reward = result / 1.0e18  # type: ignore
        print(f"{trb_reward} TRB")


if __name__ == "__main__":
    main()
