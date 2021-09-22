""" Submit Data

This module's purpose is to submit off-chain data on-chain.
"""

from abc import ABC
from abc import abstractmethod


class Submitter(ABC):
    """"""

    @abstractmethod
    async def submit_data(self) -> None:
        """Submit latest values for each datafeed to the Tellor oracle."""

        raise NotImplementedError