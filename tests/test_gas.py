"""
Test covering gas price fetching utils
"""

import pytest
from requests.exceptions import SSLError
from telliot_core.gas.legacy_gas import fetch_gas_price


@pytest.mark.asyncio
async def test_fetch_legacy_gas_price(monkeypatch, caplog):

    def raise_ssl_error():
        raise SSLError

    def raise_exception():
        raise Exception

    monkeypatch.setattr('telliot_core.gas.legacy_gas.fetch_gas_price', lambda x: raise_ssl_error())

    _ = await fetch_gas_price()

    assert "SSLError -- Unable to fetch gas price" in caplog.text


    monkeypatch.setattr('telliot_core.gas.legacy_gas.fetch_gas_price', lambda x: raise_exception())

    _ = await fetch_gas_price()

    assert "Unable to fetch gas price" in caplog.text
