from typing import Any
from typing import Optional
from dataclasses import dataclass
from telliot.answer import TimeStampedFloat
from telliot.datafeed.pricing.price_service import WebPriceService
from telliot.model.base import Base
from clamfig import deserialize

from pydantic import BaseModel

class BittrexQuote(BaseModel):
    Bid: float
    Ask: float
    Last: float


class PriceResponse(BaseModel):
    success: bool
    message: str
    result: Optional[BittrexQuote]


class BittrexPriceService(WebPriceService):
    """Bittrex Price Service"""

    def __init__(self, **kwargs: Any):
        super().__init__(
            name="Bittrex Price Service", url="https://api.bittrex.com", **kwargs
        )

    async def get_price(self, asset: str, currency: str) -> Optional[TimeStampedFloat]:
        """Implement PriceServiceInterface

        This implementation gets the price from the Bittrex API

        Note that the timestamp returned form the coinbase API could be used
        instead of the locally generated timestamp.
        """

        request_url = "/api/v1.1/public/getticker?market={}-{}".format(
            currency.lower(), asset.lower()
        )

        d = self.get_url(request_url)

        if "error" in d:
            print(d)  # TODO: Log
            return None

        else:
            r = PriceResponse.parse_obj(d["response"])
            if r.success:
                if r.result is not None:
                    return TimeStampedFloat(r.result.Last)
                else:
                    return None
            else:
                print(r.message)
                return None
