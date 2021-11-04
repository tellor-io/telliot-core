"""Example datafeed used by AMPLUSDVWAPReporter."""

import statistics

from telliot_ampl.sources import AnyBlockSource, BraveNewCoinSource
from telliot.queries.coin_price import CoinPrice
from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.pricing.price_feed import AggregatePriceSource



data_sources = [
    AnyBlockSource(),
    BraveNewCoinSource()
]


ampl_usd_vwap_feed = DataFeed(
    query=CoinPrice(coin="ampl", currency="usd", price_type="vwap"),
    source=AggregatePriceSource(
        sources=data_sources, 
        asset="ampl", 
        currency="usd", 
        algorithm=statistics.median
    ),
)