"""
Test covering gas price fetching utils
"""
import pytest
from requests.exceptions import SSLError

from telliot_core.gas.legacy_gas import fetch_gas_price


@pytest.mark.asyncio
async def test_fetch_legacy_gas_price(monkeypatch, caplog):
    def raise_ssl_error(*args, **kwargs):
        raise SSLError

    def raise_exception():
        raise Exception

    monkeypatch.setattr("requests.get", lambda x: raise_ssl_error())
    gp = await fetch_gas_price()

    assert gp is None
    assert "SSLError -- Unable to fetch gas price" in caplog.text

    monkeypatch.setattr("requests.get", lambda x: raise_exception())
    gp = await fetch_gas_price()

    assert gp is None
    assert "Error fetching gas price:" in caplog.text
