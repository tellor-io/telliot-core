from typing import Any
from typing import Dict
from typing import Optional

from pydantic import BaseModel
from telliot.answer import TimeStampedFloat
from telliot.pricing.price_service import WebPriceService


class PriceResponse(BaseModel):
    bid: float
    ask: float
    last: float
    volume: Dict[str, Any]


# Example output
# {'bid': '46696.49',
#  'ask': '46706.28',
#  'volume':
#      {'BTC': '1478.8403795849',
#       'USD': '67545338.339627693826',
#       'timestamp': 1631636700000},
#  'last': '46703.47'}}


class GeminiPriceService(WebPriceService):
    """Gemini Price Service"""

    def __init__(self, **kwargs: Any):
        super().__init__(
            name="Gemini Price Service", url="https://api.gemini.com", **kwargs
        )

    async def get_price(self, asset: str, currency: str) -> Optional[TimeStampedFloat]:
        """Implement PriceServiceInterface

        This implementation gets the price from the Bittrex API

        Note that the timestamp returned form the coinbase API could be used
        instead of the locally generated timestamp.
        """

        request_url = "/v1/pubticker/{}{}".format(asset.lower(), currency.lower())

        d = self.get_url(request_url)
        # print(d)
        if "error" in d:
            print(d)  # TODO: Log
            return None

        else:
            r = PriceResponse.parse_obj(d["response"])

            if r.last is not None:
                return TimeStampedFloat(r.last)
            else:
                return None
