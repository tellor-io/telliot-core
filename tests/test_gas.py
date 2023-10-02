"""
Test covering gas price fetching utils
"""
import pytest
from requests.exceptions import SSLError

from src.telliot_core.gas.legacy_gas import fetch_gas_price
from src.telliot_core.gas.legacy_gas import legacy_gas_station


def raise_ssl_error(*args, **kwargs):
    raise SSLError


def raise_exception():
    raise Exception


@pytest.mark.asyncio
async def test_fetch_legacy_gas_price(monkeypatch, caplog):

    monkeypatch.setattr("requests.get", lambda x: raise_ssl_error())
    gp = await fetch_gas_price()

    assert gp is None
    assert "SSLError -- Unable to fetch gas price" in caplog.text

    monkeypatch.setattr("requests.get", lambda x: raise_exception())
    gp = await fetch_gas_price()

    assert gp is None
    assert "Error fetching gas price:" in caplog.text


@pytest.mark.asyncio
async def test_legacy_gasstation(monkeypatch, caplog):
    """Test legacy_gasstation"""

    gp = await legacy_gas_station(chain_id=0)

    assert gp is None
    assert "Please add gas station API for chain id: 0" in caplog.text

    gp = await legacy_gas_station(chain_id=1, speed_parse_lis="premium")

    assert gp is None
    assert "Unable to parse gas price from gasstation: premium" in caplog.text

    monkeypatch.setattr("requests.get", lambda x: raise_ssl_error())
    gp = await legacy_gas_station(chain_id=1)

    assert gp is None
    assert "SSLError: Unable to fetch gas price" in caplog.text

    monkeypatch.setattr("requests.get", lambda x: raise_exception())
    gp = await legacy_gas_station(chain_id=1)

    assert gp is None
    assert "Error fetching gas price:" in caplog.text
