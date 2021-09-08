from dataclasses import dataclass
from abc import abstractmethod
from typing import Any


@dataclass
class DataSource:
    """Abstract Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed` algorithm
    """

    #: Data source identifier
    id: [str, None] = None

    #: Descriptive name
    name: [str, None] = None

    @abstractmethod
    def fetch(self) -> Any:
        """Fetch Data

        Returns:
            Data returned from source
            TODO: Handle exceptions
        """
        raise NotImplementedError
