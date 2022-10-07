"""
Unit tests covering telliot_core CLI commands.

Note: Pytest Live Logs breaks some CliRunner tests.
The bug prevents CliRunner from capturing logger output
  - https://github.com/pallets/click/issues/2156
  - https://github.com/pallets/click/issues/824
"""
import pytest
from click.testing import CliRunner

from telliot_core.cli.main import main


def test_main_help():
    """Test telliot_core CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, [])

    assert "Usage:" in result.stdout


def test_config_cmd():
    """Test telliot_core CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["config", "init"])
    assert not result.exception
    print(result.stdout)


@pytest.mark.skip("Infura rinkeby node deprecated, needs to use brownie")
def test_disputesbyid(caplog):
    """Test disputes by ID"""
    runner = CliRunner()
    result = runner.invoke(main, ["--test_config", "read", "master", "disputesbyid", "1"])
    assert "DisputeReport" in result.stdout
    assert not result.exception


def test_getStakerInfo():
    """Test telliot_core CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["--test_config", "read", "master", "getstakerinfo"])

    print(result.stdout)
    # expect a tuple of integers
    # output = eval(result.output.strip())
    # assert len(output) == 2
    # assert isinstance(output[0], int)
    # assert isinstance(output[1], int)


@pytest.mark.skip()
def test_gettimebasedreward():
    """Test contract method"""
    runner = CliRunner()
    result = runner.invoke(main, ["--test_config", "read", "gettimebasedreward"])
    assert "TRB" in result.output


def test_config_show():
    """Make sure config is running"""
    runner = CliRunner()
    result = runner.invoke(main, ["--test_config", "config", "show"])
    assert not result.exception


@pytest.mark.skip("Infura rinkeby node deprecated, needs to use brownie")
def test_account_status():
    """Test account status."""
    runner = CliRunner()
    result = runner.invoke(main, ["--test_config", "account", "status"])
    assert not result.exception
