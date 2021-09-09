from dataclasses import dataclass
from dataclasses import field
from typing import Any
from typing import List
from typing import Optional

import requests


@dataclass
class DataSource:
    """Abstract Base Class for a DataSource.

    A DataSource provides an input to a `DataFeed` algorithm
    """

    #: Unique data source identifier
    id: str = ""

    #: Descriptive name
    name: str = ""

    def fetch(self) -> Any:
        """Fetch Data

        Returns:
            Data returned from source
            TODO: Handle exceptions
        """
        raise NotImplementedError


@dataclass
class WebJsonPriceApi(DataSource):
    """Web JSON Price API

    A price API accessible through HTTP that returns a JSON dict result.

    """

    #: Asset ID
    asset_id: str = ""

    #: API URL
    url: str = ""

    #: Web request timeout
    timeout: float = 5.0

    #: Dict keywords used to parse API result to get price
    keywords: List[str] = field(default_factory=list)

    async def fetch(self) -> Optional[float]:
        """Fetch Data

        Returns:
            Data returned from source or None if an exception occurred
        """
        with requests.Session() as s:
            try:
                response = s.get(self.url, timeout=self.timeout)
            except Exception as e:
                msg = "API Error ({})\n{}".format(self.name, str(e))
                print(msg)
                return None

            try:
                d = response.json()
            except Exception as e:
                msg = "API Error ({}) returned invalid JSON string\n{}".format(
                    self.name, str(e)
                )
                print(msg)
                return None

            for keyword in self.keywords:
                d = d[keyword]

        price = float(d)

        return price
