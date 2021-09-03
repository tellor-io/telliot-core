from abc import abstractmethod
from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import Callable
from typing import Dict
from typing import List


@dataclass
class DataSource:
    """Abstract Base Class for a DataSource.

    A data source provides an input to a `DataFeed`
    """

    #: Data source identifier.
    #: Should uniquely identify the datasource within a DataFeed
    id: str

    @abstractmethod
    def fetch(self):
        """Fetch Data

        Returns:
            any : Data returned from source
        """
        raise NotImplementedError


@dataclass
class DataFeed:
    """Data Feed.

    A data feed produces a data point using an algorithm that operates on inputs from a :class:`DataSource`
    """

    #: Descriptive name for the feed.
    name: str

    #: DataFeed identifier.
    #: Should uniquely identify the DataFeed across the entire Tellor Oracle
    id: str

    #: List of data sources that provide inputs to the
    #: DataFeed algorithm
    # sources: list[DataSource] = field(default_factory=list)
    sources: List[DataSource]

    #: Algorithm -
    #: a function which accepts keyword argument pairs and returns a single result
    #: Each keyword corresponds to the `id` of the DataSource
    algorithm: Callable

    #: Dictionary of algorithm inputs retrieved from DataSources
    inputs: Dict[str, Any] = field(default_factory=dict)

    #: Current value of the Algorithm result
    result: Any = None

    def update(self):
        """Get new datapoint and store in `result`.

        Collect inputs to the algorithm and run the algorithm

        Returns:
            any : algorithm result
        """
        self._collect_inputs()
        self.result = self.algorithm(**self.inputs)
        return self.result

    def _collect_inputs(self):
        """Get all feed inputs.

        This base implementation fetches inputs from all data sources.
        Subclasses with several inputs might consider concurrent implementations
        using asyncio or threads.
        TODO: Consider making DataSource.fetch an async def
        """
        for source in self.sources:
            self.inputs[source.id] = source.fetch()
