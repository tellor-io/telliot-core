""" Submit Data

This module's provides a base Submitter class to be subclassed
in the `reporter_plugins` module. Submitters submit off-chain data on-chain
to the Tellor oracle.
"""
from abc import ABC
from abc import abstractmethod
from typing import Any


class Submitter(ABC):
    """Base class for a Submitter.

    A Submitter provides a standard interface for the `telliot`
    CLI to interact with and submit off-chain data to the
    Tellor oracle."""

    @abstractmethod
    async def submit_data(self, value: Any, request_id: str) -> Any:
        """Submit latest values for each datafeed to the Tellor oracle."""

        raise NotImplementedError
