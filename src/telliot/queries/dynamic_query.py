""" :mod:`telliot.queries.dynamic_query`

"""
# Copyright (c) 2021-, Tellor Development Community
# Distributed under the terms of the MIT License.
from abc import ABC
from abc import abstractmethod
from typing import ClassVar
from typing import List
from pydantic import Field
from telliot.queries.query import OracleQuery
from web3 import Web3


class DynamicQuery(OracleQuery, ABC):
    """ Dynamic OracleQuery

    A parameterized OracleQuery that generates different values for tip data
    and request ID, depending upon its configuration.
    """

    type: str = Field("DynamicQuery", constant=True)

    parameters: ClassVar[List[str]]

    @property
    def tip_id(self) -> bytes:
        """Return the modern or legacy request ID

        Returns:
            bytes: 32-byte Request ID
        """
        return bytes(Web3.keccak(self.tip_data))

    @abstractmethod
    def check_parameters(self) -> bool:
        """Check query parameters

        This method must validate all query parameters to ensuree that
        the query is ready to generate proper tip data, request id,
        and response type.

        Returns:
            True if all query parameters are valid
        """
        pass
