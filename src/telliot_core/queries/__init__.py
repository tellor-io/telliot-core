""" telliot_core.queries

The Queries package provides a mechanism to define Oracle Query Types
and specify the format of the query and the response.
"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from telliot_core.queries.legacy_query import LegacyRequest
from telliot_core.queries.price.spot_price import SpotPrice
from telliot_core.queries.query import OracleQuery
from telliot_core.queries.string_query import StringQuery

__all__ = ["OracleQuery", "LegacyRequest", "StringQuery", "SpotPrice"]
