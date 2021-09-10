from typing import Any
from typing import Optional

from telliot.pricing.price_service import WebPriceService


class CoinbasePriceService(WebPriceService):
    """Coinbase Price Service"""

    def __init__(self, **kwargs: Any) -> None:
        kwargs["name"] = "Coinbase Price Service"
        kwargs["url"] = "https://api.pro.coinbase.com"
        super().__init__(**kwargs)

    def get_price(self, asset: str, currency: str) -> Optional[float]:
        """Implement of PriceServiceInterface

        Get price from API
        """

        # Get Price URL according to
        # https://docs.pro.coinbase.com/#products API
        request_url = "/products/{}-{}/ticker".format(
            asset.lower(), currency.lower()
        )

        d = self.get_url(request_url)
        if "error" in d:
            price = None
            print(d)  # TODO: Log

        elif "response" in d:
            response = d["response"]

            if "message" in response:
                print(
                    "API ERROR ({}): {}".format(self.name, response["message"])
                )
                return None
            else:
                return float(response["price"])

        else:
            raise Exception("Invalid response from get_url")

        return price
