from typing import Any, Optional
from urllib.parse import urlencode

from telliot.pricing.price_service import WebPriceService

# Coinbase API uses the 'id' field from /coins/list.
# Using a manual mapping for now.
coingecko_coin_id = {
    'btc': 'bitcoin'
}


class CoinGeckoPriceService(WebPriceService):
    """ CoinGecko Price Service

    """

    def __init__(self, **kwargs: Any) -> None:
        kwargs['name'] = 'CoinGecko Price Service'
        kwargs['url'] = 'https://api.coingecko.com'
        super().__init__(**kwargs)

    def get_price(self, asset: str, currency: str) -> Optional[float]:
        """ Implement of PriceServiceInterface

        Get price from API
        """

        asset = asset.lower()
        currency = currency.lower()

        coin_id = coingecko_coin_id.get(asset, None)
        if not coin_id:
            raise Exception('Asset not supported: {}'.format(asset))

        # Get Price URL according to
        # https://docs.pro.coinbase.com/#products API
        url_params = urlencode({'ids': coin_id, 'vs_currencies': currency})
        request_url = '/api/v3/simple/price?{}'.format(url_params)

        d = self.get_url(request_url)

        if 'response' in d:
            response = d['response']
            try:
                price = float(response[coin_id][currency])
            except KeyError as e:
                msg = 'Error parsing API response: KeyError: {}'.format(e)
                print(msg)
                price = None
        else:
            price = None

        return price

    @staticmethod
    def _get_price_url(asset: str, currency: str) -> str:
        """

        """
