import asyncio
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict

from telliot.datafeed.data_source import DataSource


@dataclass
class DataFeed:
    """Data Feed.

    A data feed produces a data point using an algorithm that operates on
    inputs from a :class:`DataSource`
    """

    #: Descriptive name for the feed.
    name: str

    #: DataFeed identifier.
    #: Uniquely identifies the DataFeed across the entire Tellor network
    id: str

    #: List of data sources that provide inputs to the
    #: DataFeed algorithm
    # sources: list[DataSource] = field(default_factory=list)
    sources: Dict[str, DataSource]

    #: A function which accepts keyword argument pairs and
    #  returns a single result.
    algorithm: Callable[..., Any]

    #: Dictionary of algorithm inputs retrieved from DataSources
    #: Keys correspond to algorithm keyword argument inputs
    inputs: Dict[str, Any] = field(default_factory=dict)

    #: Current value of the Algorithm result
    result: Any = None

    def update(self) -> Any:
        """Get new datapoint and store in result.

        Collect inputs to the algorithm and run the algorithm

        Returns:
            Result of algorithm
        """
        self._collect_inputs()
        self.result = self.algorithm(**self.inputs)
        return self.result

    def _collect_inputs(self) -> None:
        """Get all feed inputs.

        This base implementation fetches inputs from all data sources.
        Subclasses with several inputs might consider concurrent
        implementations using asyncio or threads.
        """

        async def gather_inputs():
            keys = self.sources.keys()
            values = await asyncio.gather(
                *[self.sources[key].fetch() for key in keys]
            )
            self.inputs = dict(zip(keys, values))

        asyncio.run(gather_inputs())
