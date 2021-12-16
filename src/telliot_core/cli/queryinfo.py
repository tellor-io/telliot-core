import asyncio

import click

from telliot_core.cli.utils import get_app
from telliot_core.data.query_catalog import query_catalog


@click.command()
@click.pass_context
@click.argument("query_tag", type=str)
@click.option("--data", is_flag=True, help="Retrieve all datapoints from blockchain")
def queryinfo(ctx: click.Context, query_tag: str, data: bool) -> None:
    """Show query information

    QUERY_TAG: Choose from query catalog:

    \b https://github.com/tellor-io/dataSpecs/blob/main/catalog.md
    """

    from telliot_core.apps.oracle_read import (
        getTimestampCountById,
        getBlockNumberByTimestamp,
        getTipsById,
        getReportTimestampByIndex,
        getCurrentReward,
        getCurrentValue,
        getTimeOfLastNewValue,
        getValueByTimestamp,
        getReporterByTimestamp,
    )

    _ = get_app(ctx)  # Initialize app

    entries = query_catalog.find(tag=query_tag)
    if len(entries) == 0:
        print(f"Unknown query tag: {query_tag}.")
        return
    else:
        catalog_entry = entries[0]

    # Get the query object from the catalog entry
    q = catalog_entry.query

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
