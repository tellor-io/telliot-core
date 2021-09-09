from typing import Any, Dict, Optional

from telliot.pricing.price_service import WebPriceService


class CoinbasePriceService(WebPriceService):
    """ Coinbase Price Service

    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs['name'] = 'Coinbase Price Service'
        kwargs['url'] = 'https://api.pro.coinbase.com'
        super().__init__(**kwargs)

    def get_price(self, asset: str, currency: str) -> Optional[float]:
        """ Implement of PriceServiceInterface

        Get price from API
        """
        request_url = self._get_price_url(asset, currency)

        response = self.get_url(request_url)

        if 'response' in response:
            price = self._parse_price_response(response['response'])
        else:
            price = None
            print(response)

        return price

    @staticmethod
    def _get_price_url(asset: str, currency: str) -> str:
        """ Get Price URL according to https://docs.pro.coinbase.com/#products API

        """
        return '/products/{}-{}/ticker'.format(asset.upper(), currency.upper())

    def _parse_price_response(self, response: Dict[str, Any]) \
            -> Optional[float]:

        if 'message' in response:
            print('API ERROR ({}): {}'.format(self.name, response['message']))
            return None
        else:
            return float(response['price'])
