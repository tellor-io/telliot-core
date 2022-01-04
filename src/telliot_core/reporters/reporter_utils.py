from typing import Optional

from telliot_core.data.query_catalog import query_catalog
from telliot_core.queries import OracleQuery
from telliot_core.tellorx.oracle import TellorxOracleContract

# List of currently active reporters

reporter_sync_schedule = [
    "eth-usd-legacy",
    "btc-usd-legacy",
    "ampl-legacy",
    "trb-usd-legacy",
    "ohm-eth-spot",
]


async def tellorx_suggested_report(
    oracle: TellorxOracleContract,
) -> Optional[OracleQuery]:
    """Returns the currently suggested query to report against.

    The suggested query changes each time a block contains a query response.
    The time of last report is used to randomly index into the
    `report_sync_schedule` to determine the suggested query.

    """
    timestamp, status = await oracle.getTimeOfLastNewValue()

    if status.ok:
        suggested_idx = timestamp.ts % len(reporter_sync_schedule)

        suggested_query_tag = reporter_sync_schedule[suggested_idx]

        entries = query_catalog.find(tag=suggested_query_tag)
        if len(entries) == 0:
            print(f"Unknown query tag: {suggested_query_tag}.")
            return None
        else:
            catalog_entry = entries[0]
            # Get the query object from the catalog entry
            q = catalog_entry.query
            assert isinstance(q, OracleQuery)
            return q

    else:
        return None
