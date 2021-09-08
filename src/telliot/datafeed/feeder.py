from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict


@dataclass
class DataSource:
    """Abstract Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed` algorithm
    """

    #: Data source identifier
    id: str = None

    #: Descriptive name
    name: str = None

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch Data

        Returns:
            Data returned from source
            TODO: Handle exceptions
        """
        raise NotImplementedError


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
    #: Each keyword corresponds to the `id` of the DataSource
    algorithm: Callable[..., Any]

    #: Dictionary of algorithm inputs retrieved from DataSources
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
        TODO: Consider making DataSource.fetch an async def
        """
        for kw in self.sources:
            self.inputs[kw] = self.sources[kw].fetch()
