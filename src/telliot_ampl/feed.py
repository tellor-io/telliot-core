"""Example datafeed used by AMPLUSDVWAPReporter."""
import statistics

from telliot.datafeed import DataFeed
from telliot_feed_examples.sources.price_aggregator import PriceAggregator
from telliot.queries.legacy_query import LegacyRequest

from telliot_ampl.sources import AnyBlockSource
from telliot_ampl.sources import BraveNewCoinSource


data_sources = [AnyBlockSource(), BraveNewCoinSource()]


ampl_usd_vwap_feed = DataFeed(
    query=LegacyRequest(legacy_id=10),
    source=PriceAggregator(
        sources=data_sources, asset="ampl", currency="usd", algorithm=statistics.median
    ),
)
