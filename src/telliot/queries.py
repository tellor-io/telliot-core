from telliot.answer import TimeStampedFixed
from telliot.query import OracleQuery

# Oracle Queries
# This module lists all DAO-approved queries currently supported by the
# Tellor network.


valid_queries = {
    "btc-usd-median": OracleQuery(
        uid="btc-usd-median",
        request_id=1,
        question="What is the median price of bitcoin in USD?",
        answer_type=TimeStampedFixed,
    )
}
