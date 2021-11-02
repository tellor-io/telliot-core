""" telliot.queries

The Queries package provides a mechanism to define Oracle Query Types
and specify the format of the query and the response.
"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from telliot.queries.coin_price import CoinPrice
from telliot.queries.legacy_query import LegacyRequest
from telliot.queries.query import OracleQuery
from telliot.queries.string_query import StringQuery

__all__ = ["OracleQuery", "LegacyRequest", "StringQuery", "CoinPrice"]
