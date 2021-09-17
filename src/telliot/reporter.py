""" Telliot Reporter

Runs datafeed server as a background task and populates
the database with off-chain data at scheduled times.
Submits local data to Tellor Oracle at scheduled times.
Configuration is handled through CLI flags or in the
config file.
"""
from abc import ABC
from abc import abstractmethod
from multiprocessing import Process
from typing import Any
from typing import Dict

import uvicorn  # type: ignore

from .datafeed import server


class Reporter(ABC):
    """
    Runs local db for off-chain data as a background task.
    Populates db & submits local data to Tellor Oracle.
    """

    def __init__(self, datafeeds: Dict[str, Any]) -> None:
        self.datafeeds = datafeeds
        # self.database = Process(
        #     target=uvicorn.run,
        #     args=(server.app,),
        #     kwargs={"host": "127.0.0.1", "port": 8000, "log_level": "info"},
        #     daemon=True,
        # )

    @abstractmethod
    async def update_datafeeds(self) -> None:
        """Update all off-chain values for each datafeed
        and store those values locally."""

        raise NotImplementedError

    @abstractmethod
    async def submit_data(self) -> None:
        """Submit latest values for each datafeed to the Tellor oracle."""

        raise NotImplementedError

    @abstractmethod
    async def run(self) -> None:
        """Used by telliot CLI to run db in background and
        execute all desired Reporter functions."""

        # Run database server api as background process.
        # self.database.start()

        # TODO: Replace with update_datafeeds() & submit_data() function calls.
        raise NotImplementedError

        # Execution will block here until Ctrl+C (Ctrl+Break on Windows) is pressed.
        # try:
        #     # TODO: Run asyncio loop forever.
        #     pass
        # except (KeyboardInterrupt, SystemExit):
        #     self.background_server.terminate()
