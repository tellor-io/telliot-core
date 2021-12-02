""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import asyncio

import click
import yaml

import telliot_core
from telliot_core.apps.core import TelliotCore  # type: ignore
from telliot_core.apps.master_read import getStakerInfo
from telliot_core.apps.oracle_read import getTimeBasedReward
from telliot_core.apps.telliot_config import TelliotConfig


def get_app(ctx: click.Context) -> TelliotCore:
    """Get an app configured using CLI context"""

    app = TelliotCore.get() or TelliotCore()

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
@click.pass_context
def gettimebasedreward(ctx: click.Context) -> None:
    _ = get_app(ctx)  # Initialize app

    result, status = asyncio.run(getTimeBasedReward())

    if not status.ok:
        print(status)
    else:
        print(f"{result} TRB")


@read.command()
@click.argument("address", required=False)
@click.pass_context
def getstakerinfo(ctx: click.Context, address: str) -> None:
    _ = get_app(ctx)  # Initialize app
    result, read_response = asyncio.run(getStakerInfo(address=address))

    if not read_response.ok:
        print(read_response)
    else:
        print(result)


@main.command()
@click.pass_context
@click.argument("lid", type=int)
@click.option("--data", is_flag=True, help="Retrieve all datapoints from blockchain")
def legacyqueryinfo(ctx: click.Context, lid: int, data: bool) -> None:
    """Show query info"""
    from telliot_core.apps.oracle_read import (
        getTimestampCountById,
        getBlockNumberByTimestamp,
        getTipsById,
        getReportTimestampByIndex,
        getCurrentReward,
    )
    from telliot_core.apps.oracle_read import (
        getCurrentValue,
        getTimeOfLastNewValue,
        getValueByTimestamp,
        getReporterByTimestamp,
    )

    _ = get_app(ctx)  # Initialize app
    from telliot_core.queries import LegacyRequest

    q = LegacyRequest(legacy_id=lid)
    print(f"Descriptor: {q.descriptor}")
    queryId = f"0x{q.query_id.hex()}"
    print(f"queryId: {queryId}")

    count, status = asyncio.run(getTimestampCountById(queryId))
    print(f"Timestamp count: {count}")

    bytes_value, status = asyncio.run(getCurrentValue(queryId))
    if bytes_value is not None:
        value = q.value_type.decode(bytes_value)
        print(f"Current value: {value}")
    else:
        print("Current value: None")

    tlnv, status = asyncio.run(getTimeOfLastNewValue())
    print(f"Time of last new value (all queryIds): {tlnv}")

    tips, status = asyncio.run(getTipsById(queryId))
    print(f"Tips (TRB): {tips}")

    (tips2, reward), status = asyncio.run(getCurrentReward(queryId))
    print(f"Tips/reward (TRB): {tips2} / {reward}")

    if data:
        print("On-chain data:")
        for k in range(count):
            ts, status = asyncio.run(getReportTimestampByIndex(queryId, k))
            blocknum, status = asyncio.run(getBlockNumberByTimestamp(queryId, ts))
            bytes_value, status = asyncio.run(getValueByTimestamp(queryId, ts))
            value = q.value_type.decode(bytes_value)
            reporter, status = asyncio.run(getReporterByTimestamp(queryId, ts))
            print(
                f" index: {k}, timestamp: {ts}, block: {blocknum}, "
                f"value:{value}, reporter: {reporter} "
            )


if __name__ == "__main__":
    main()
