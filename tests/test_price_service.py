from unittest import mock

import pytest
import requests

from telliot_core.pricing.price_service import WebPriceService


@pytest.mark.asyncio
async def test_etherscan_gas_error(caplog):
    class FakePriceService(WebPriceService):
        async def get_price(self, asset, currency):
            return None, None
    
    def json_decode_error(*args, **kwargs):
        raise requests.exceptions.JSONDecodeError()

    with mock.patch("requests.Session.get", side_effect=json_decode_error):
        wsp = FakePriceService(name="FakePriceService", url="https://fakeurl.xyz")
        result = wsp.get_url()

        assert "error" in result
        assert "JSON Decode Error" == result["error"]
