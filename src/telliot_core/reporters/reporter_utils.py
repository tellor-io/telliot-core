from typing import List
from typing import Optional

from telliot_core.tellor.tellorx.oracle import TellorxOracleContract

# List of currently active reporters

reporter_sync_schedule: List[str] = [
    "eth-usd-legacy",
    "btc-usd-legacy",
    "trb-usd-legacy",
    "ohm-eth-spot",
]


async def tellorx_suggested_report(
    oracle: TellorxOracleContract,
) -> Optional[str]:
    """Returns the currently suggested query to report against.

    The suggested query changes each time a block contains a query response.
    The time of last report is used to randomly index into the
    `report_sync_schedule` to determine the suggested query.

    """
    timestamp, status = await oracle.getTimeOfLastNewValue()

    if status.ok:
        suggested_idx = timestamp.ts % len(reporter_sync_schedule)
        suggested_qtag = reporter_sync_schedule[suggested_idx]
        assert isinstance(suggested_qtag, str)
        return suggested_qtag

    else:
        return None
