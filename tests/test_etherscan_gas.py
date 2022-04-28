from unittest import mock

import pytest
import requests

from telliot_core.gas import etherscan_gas
from telliot_core.gas.etherscan_gas import EtherscanGasPrice
from telliot_core.gas.etherscan_gas import EtherscanGasPriceSource


@pytest.mark.asyncio
async def test_etherscan_gas():
    c = EtherscanGasPriceSource()
    result = await c.fetch_new_datapoint()
    assert isinstance(result[0], EtherscanGasPrice)


@pytest.mark.asyncio
async def test_etherscan_gas_error(caplog):
    etherscan_gas.requests.get = mock.Mock(side_effect=requests.exceptions.ConnectionError)
    c = EtherscanGasPriceSource()
    result = await c.fetch_new_datapoint()
    assert result[0] is None
    assert result[1] is None
    # assert "Connection timeout" in caplog.text

    etherscan_gas.requests.get = mock.Mock(side_effect=requests.exceptions.Timeout)
    c = EtherscanGasPriceSource()
    result = await c.fetch_new_datapoint()
    assert result[0] is None
    assert result[1] is None
    # assert "Timeout" in caplog.text

    def invalid_json():
        return "<p>blah<p/>"

    etherscan_gas.requests.get = invalid_json
    c = etherscan_gas.EtherscanGasPriceSource()
    result = await c.fetch_new_datapoint()
    assert result[0] is None
    assert result[1] is None
    # print(caplog.records)
    # assert "JSONDecodeError" in caplog.text
