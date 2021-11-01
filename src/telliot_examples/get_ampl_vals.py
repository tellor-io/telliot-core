from telliot.datafeed.data_source import DataSource
from telliot.datafeed.data_feed import DataFeed
from telliot.queries.query import OracleQuery


class BraveNewCoinSource(DataSource):
    pass


class AnyBlockSource(DataSource):
    pass


class AMPLQuery(OracleQuery):
    pass


ampl_sources = {
    "ampl-brave-new-coin": BraveNewCoinSource(),
    "ampl-anyblock": AnyBlockSource()
}
ampl_query = AMPLQuery()

ampl_feed = DataFeed(
    sources = None,
    query = None
)

# run update value for ampl_feed at the needed interval