from typing import List
from typing import Optional

from telliot_core.data.query_catalog import query_catalog
from telliot_core.tellor.tellorflex.autopay import TellorFlexAutopayContract

# List of currently active query ids
query_ids_in_catalog: List[str] = [lis.query_id for lis in query_catalog._entries.values()]
print(query_ids_in_catalog)


async def autopay_suggested_report(autopay: TellorFlexAutopayContract) -> Optional[str]:
    """Returns the currently suggested query to report against.

    Pulls query_ids with tips available from the tellor autopay
    contract, checks if query ids exist in the query catalog,
    then sorts them from highest tip amount to lowest
    """
    chain = autopay.node.chain_id

    if chain in (1, 4, 137, 80001):
        assert isinstance(autopay, TellorFlexAutopayContract)
        queryIdLis, status = await autopay.read("getFundedQueryIds")
    else:
        return None

    if status.ok:

        tips_dictionary = {i: autopay.get_current_tip(i) for i in queryIdLis if i in query_ids_in_catalog}
        tips_sorted = list(sorted(tips_dictionary.items(), key=lambda item: item[1]))  # type: ignore

        suggested_qtag = tips_sorted[0][0]
        assert isinstance(suggested_qtag, str)
        return suggested_qtag

    else:
        return None
