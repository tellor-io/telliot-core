""" Feeder module concept

"""
from abc import abstractmethod

from atom.api import Atom, List, Str, Dict, Callable, Value, Float


class DataSource(Atom):
    """ Abstract Base Class for a DataSource

    A data source provides an input to a `DataFeed`
    """

    #: Data source identifier
    #: Should uniquely identify the datasource within a DataFeed
    id = Str()

    @abstractmethod
    def fetch(self):
        """ Fetch Data

        Returns
        -------
        <type> : Data returned from source
        """
        raise NotImplementedError


class DataFeed(Atom):
    """ Data Feed

    """

    #: Descriptive name
    name = Str()

    #: DataFeed identifier
    #: Should uniquely identify the DataFeed across the entire Tellor Oracle
    id = Str()

    #: List of data sources that provide inputs to the
    #: DataFeed algorithm
    sources = List(DataSource)

    #: Dictionary of algorithm inputs retrieved from DataSources
    inputs = Dict(key=str)

    #: Algorithm
    #: A function which accepts keyword argument pairs and returns a single result
    #: Each keyword corresponds to the `id` of the DataSource
    algorithm = Callable()

    #: Current value of the Algorithm result
    result = Value()

    def update(self):
        """ Get new datapoint and store in `result`

        Collect inputs to the algorithm and run the algorithm
        """
        self._collect_inputs()
        self.result = self.algorithm(**self.inputs)
        return self.result

    def _collect_inputs(self):
        """ Get all feed inputs

        This base implementation fetches inputs from all data sources.
        Subclasses with several inputs might consider concurrent implementations
        using asyncio or threads.
        TODO: Consider making DataSource.fetch an async def
        """
        for source in self.sources:
            self.inputs[source.id] = source.fetch()


