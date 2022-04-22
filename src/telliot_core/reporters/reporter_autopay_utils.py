from time import time
from typing import Any
from typing import Tuple

from eth_abi import decode_single
from telliot_feed_examples.feeds import CATALOG_FEEDS
from telliot_feed_examples.utils.log import get_logger

from telliot_core.data.query_catalog import query_catalog
from telliot_core.tellor.tellorflex.autopay import TellorFlexAutopayContract
from telliot_core.utils.response import error_status
from telliot_core.utils.timestamp import TimeStamp


logger = get_logger(__name__)

# List of currently active queries
query_ids_in_catalog = {query_catalog._entries[tag].query_id: tag for tag in query_catalog._entries}


async def single_tip_suggested_query_id(autopay: TellorFlexAutopayContract) -> Tuple[Any, Any]:
    """Returns the currently suggested query to report against.

    Pulls query_ids with tips available from the tellor autopay
    contract, checks if query ids exist in the query catalog,
    then sorts them from highest tip amount to lowest
    """
    assert isinstance(autopay, TellorFlexAutopayContract)
    query_id_lis, status = await autopay.read("getFundedQueryIds")

    if status.ok:

        tips_dictionary = {i: autopay.get_current_tip(i) for i in query_id_lis if i in query_ids_in_catalog}
        tips_sorted = sorted(tips_dictionary.items(), key=lambda item: item[1])  # type: ignore
        if tips_sorted:
            suggested_qtag = tips_sorted[0][0]
            suggested_qtag_tip = tips_sorted[0][1]
            assert isinstance(suggested_qtag, str)
            return suggested_qtag, suggested_qtag_tip
        else:
            return None, None
    else:
        msg = "can't get FundedQueryIds"
        return error_status(note=msg, log=logger.warning)


feed_details_map = {
    "reward": 0,
    "balance": 1,
    "startTime": 2,
    "interval": 3,
    "window": 4,
    "priceThreshold": 5,
    "feedsWithFundingIndex": 6,
}


async def get_feed_details(query_id: str, autopay: TellorFlexAutopayContract) -> Tuple[Any, Any]:
    assert isinstance(autopay, TellorFlexAutopayContract)
    current_time = TimeStamp(time()).ts
    feed_ids, status = await autopay.read("getCurrentFeeds", _queryId=query_id)

    if not status.ok:
        msg = "can't get feed details to calculate tips"
        return None, error_status(note=msg, log=logger.warning)

    f_q_dict = {}
    for i in feed_ids:
        if i:
            feed_id = "0x" + i.hex()
            feed_details, status = await autopay.read("getDataFeed", _feedId=feed_id)

            if not status.ok:
                msg = "couldn't get feed details from contract"
                return None, error_status(note=msg, log=logger.warning)

            if feed_details[feed_details_map["balance"]] <= 0:
                msg = f"{feed_id}, feed has no remaining balance"
                return None, error_status(note=msg, log=logger.warning)

        n = (current_time - feed_details[feed_details_map["startTime"]]) / feed_details[feed_details_map["interval"]]
        c = feed_details[feed_details_map["startTime"]] / feed_details[feed_details_map["interval"]] * n
        response, status = await autopay.read("getDataBefore", _queryId=query_id, _timestamp=current_time)
        if not status.ok:
            msg = "couldn't get DataBefore"
            return None, error_status(note=msg, log=logger.warning)
        value_before_now = (
            decode_single("(uint256)", response[1])[0] / 1e18
        )  # there might be an issue here with decimals!!!!!!!!!
        timestamp_before_now = response[2]
        if not status.ok:
            msg = "couldn't get value before from getDataBefore"
            return None, error_status(note=msg, log=logger.warning)

        rules = [
            feed_details[feed_details_map["priceThreshold"]] == 0,
            feed_details[feed_details_map["balance"]] > 0,
            current_time - c < feed_details[feed_details_map["window"]],
            timestamp_before_now < c,
        ]

        if all(rules):
            f_q_dict[i] = feed_details[feed_details_map["reward"]]
        else:
            datafeed = CATALOG_FEEDS[query_ids_in_catalog[query_id]]
            value_now = await datafeed.source.fetch_new_datapoint()
            value_now = value_now[0]

            if value_before_now == 0:
                price_change = 10000
            elif value_now >= value_before_now:
                price_change = (10000 * (value_now - value_before_now)) / value_before_now
            else:
                price_change = (10000 * (value_before_now - value_now)) / value_before_now

            if price_change > feed_details[feed_details_map["price_threshold"]]:
                f_q_dict[i] = feed_details[feed_details_map["reward"]]

    tips_total = sum(f_q_dict.values())
    return query_id, tips_total


async def autopay_suggested_report(autopay: TellorFlexAutopayContract) -> Tuple[Any, Any]:
    chain = autopay.node.chain_id

    if chain in (1, 4, 137, 80001):
        assert isinstance(autopay, TellorFlexAutopayContract)
        datafeed_suggested_qtag = {j: await get_feed_details(i, autopay) for i, j in query_ids_in_catalog.items()}
        datafeed_tips_sorted = sorted(datafeed_suggested_qtag.items(), key=lambda item: item[1][1])  # type: ignore
        single_suggested_qtag, single_suggested_tip = await single_tip_suggested_query_id(autopay=autopay)

        if datafeed_tips_sorted and single_suggested_qtag:
            if datafeed_tips_sorted[-1][1][1] > single_suggested_tip:
                return datafeed_tips_sorted[-1][0], datafeed_tips_sorted[-1][1][1]
            else:
                return query_ids_in_catalog[single_suggested_qtag[0]], single_suggested_tip
        elif not datafeed_suggested_qtag and single_suggested_qtag:
            return query_ids_in_catalog[single_suggested_qtag[0]], single_suggested_tip
        elif datafeed_suggested_qtag and not single_suggested_qtag:
            return datafeed_tips_sorted[-1][0], datafeed_tips_sorted[-1][1][1]
        else:
            return None, None

    else:
        return None, None
