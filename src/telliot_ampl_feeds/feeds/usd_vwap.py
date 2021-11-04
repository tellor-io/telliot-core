"""Example datafeed used by AMPLUSDVWAPReporter."""
from telliot.datafeed import DataFeed
from telliot.queries.legacy_query import LegacyRequest
from telliot_ampl.config import AMPLConfig
from telliot_ampl.sources import AMPLUSDVWAPSource


cfg = AMPLConfig()
ampl_usd_vwap_feed = DataFeed(
    query=LegacyRequest(legacy_id=10), source=AMPLUSDVWAPSource(cfg=cfg)
)
