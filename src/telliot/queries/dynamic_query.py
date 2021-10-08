""" :mod:`telliot.queries.dynamic_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import List
from typing import Dict
from typing import Any
from pydantic import Field
from telliot.queries.query import OracleQuery
from web3 import Web3


class DynamicQuery(OracleQuery, ABC):
    """ Dynamic Oracle Query

    A DynamicQuery is a parameterized OracleQuery that can be customized to
    generate different values for tip data and tip ID, depending upon
    it's configuration.
    """

    type: str = Field("DynamicQuery", constant=True)


    pass