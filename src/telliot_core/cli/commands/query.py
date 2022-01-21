import click

from telliot_core.cli.utils import async_run
from telliot_core.cli.utils import cli_core
from telliot_core.data.query_catalog import query_catalog
from telliot_core.reporters.reporter_utils import tellor_suggested_report


@click.group()
def query() -> None:
    """Access on-chain query information."""
    pass


@query.command()
@click.pass_context
@click.argument("query_tag", type=str)
@click.option(
    "--npoints",
    type=int,
    default=1,
    help="Number of datapoints to retrieve from block chain (most recent)",
)
@async_run
async def status(ctx: click.Context, query_tag: str, npoints: int) -> None:
    """Show query information

    QUERY_TAG: Choose from query catalog:

    \b https://github.com/tellor-io/dataSpecs/blob/main/catalog.md
    """

    async with cli_core(ctx) as core:

        entries = query_catalog.find(tag=query_tag)
        if len(entries) == 0:
            print(f"Unknown query tag: {query_tag}.")
            return
        else:
            catalog_entry = entries[0]

        # Get the query object from the catalog entry
        q = catalog_entry.query

        queryId = f"0x{q.query_id.hex()}"

        tellorx = core.get_tellorx_contracts()
        count, status = await tellorx.oracle.getTimestampCountById(queryId)
        print(f"Timestamp count: {count}")

        bytes_value, status = await tellorx.oracle.getCurrentValue(queryId)
        if bytes_value is not None:
            value = q.value_type.decode(bytes_value)
            print(f"Current value: {value}")
        else:
            print("Current value: None")

        tlnv, status = await tellorx.oracle.getTimeOfLastNewValue()
        print(f"Time of last new value (all queryIds): {tlnv}")

        tips, status = await tellorx.oracle.getTipsById(queryId)
        print(f"Tips (TRB): {tips}")

        (tips2, reward), status = await tellorx.oracle.getCurrentReward(queryId)
        print(f"Tips/reward (TRB): {tips2} / {reward}")

        print(f"{npoints} most recent on-chain datapoints:")
        for k in range(count - npoints, count):
            ts, status = await tellorx.oracle.getReportTimestampByIndex(queryId, k)
            blocknum, status = await tellorx.oracle.getBlockNumberByTimestamp(queryId, ts)
            bytes_value, status = await tellorx.oracle.getValueByTimestamp(queryId, ts)
            value = q.value_type.decode(bytes_value)
            reporter, status = await tellorx.oracle.getReporterByTimestamp(queryId, ts)
            print(f" index: {k}, timestamp: {ts}, block: {blocknum}, value:{value}, reporter: {reporter} ")


@query.command()
@click.pass_context
@async_run
async def suggest(ctx: click.Context) -> None:
    """Get the current suggested query for reporter synchronization."""

    async with cli_core(ctx) as core:
        tellorx = core.get_tellorx_contracts()
        qtag = await tellor_suggested_report(tellorx.oracle)
        assert isinstance(qtag, str)
        print(f"Suggested query: {qtag}")
