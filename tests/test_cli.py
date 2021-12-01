"""
Unit tests covering telliot_core CLI commands.
"""
from click.testing import CliRunner

from telliot_core.cli import main


def test_config_cmd():
    """Test telliot_core CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["config", "init"])

    print(result)


def test_getStakerInfo(rinkeby_core):
    """Test telliot_core CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["read", "getstakerinfo"])

    print(result.output)
    # expect a tuple of integers
    # output = eval(result.output.strip())
    # assert len(output) == 2
    # assert isinstance(output[0], int)
    # assert isinstance(output[1], int)


def test_gettimebasedreward(rinkeby_core):
    runner = CliRunner()
    result = runner.invoke(main, ["read", "gettimebasedreward"])
    print(result.output)
    assert "TRB" in result.output
