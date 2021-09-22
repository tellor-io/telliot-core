""" Submit Data

This module's purpose is to submit off-chain data on-chain.
"""

from abc import ABC
from abc import abstractmethod
from typing import Any


class Submitter(ABC):
    """"""

    @abstractmethod
    async def submit_data(self, value: Any, request_id: str) -> Any:
        """Submit latest values for each datafeed to the Tellor oracle."""

        raise NotImplementedError