from telliot.pricing.coinbase import CoinbasePriceService


def test_web_price_service():
    ps = CoinbasePriceService()
    result = ps.get_url()
    assert 'response' in result
    assert result['response'] is not None
    btcusd = ps.get_price('btc', 'usd')
    print(btcusd)
    assert isinstance(btcusd, float)


def test_web_price_service_timeout():
    ps = CoinbasePriceService(timeout=.00001)
    result = ps.get_url()
    assert result['error'] == 'Timeout Error'
