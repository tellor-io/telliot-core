""" Telliot Reporter

Runs datafeed server as a background task and populates
the database with off-chain data at scheduled times.
Submits local data to Tellor Oracle at scheduled times.
Configuration is handled through CLI flags or in the
config file.
"""
from abc import ABC
from abc import abstractmethod


class Reporter(ABC):
    """
    Runs local db for off-chain data as a background task.
    Populates db & submits local data to Tellor Oracle.
    """

    @abstractmethod
    async def run(self) -> None:
        """Used by telliot CLI to run db in background and
        execute all desired Reporter functions."""

        raise NotImplementedError
