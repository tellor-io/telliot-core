"""Example datafeed used by AMPLUSDVWAPReporter."""
import statistics

from telliot.datafeed.data_feed import DataFeed
from telliot.datafeed.pricing.price_feed import AggregatePriceSource
from telliot.queries.coin_price import CoinPrice

from telliot_ampl.sources import AnyBlockSource
from telliot_ampl.sources import BraveNewCoinSource


data_sources = [AnyBlockSource(), BraveNewCoinSource()]


ampl_usd_vwap_feed = DataFeed(
    query=CoinPrice(coin="ampl", currency="usd", price_type="vwap"),
    source=AggregatePriceSource(
        sources=data_sources, asset="ampl", currency="usd", algorithm=statistics.median
    ),
)
