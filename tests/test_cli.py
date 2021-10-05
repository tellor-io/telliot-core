"""
Unit tests covering telliot CLI commands.
"""
from click.testing import CliRunner
from telliot.cli import main


def test_report_cmd():
    """Test telliot CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["report", "btc-usd-median"])

    assert result.exit_code == 0
    assert "Reporting to the Tellor oracle." in result.output
    assert "Chosen datafeed uid: btc-usd-median" in result.output


def test_status_cmd():
    """Test telliot CLI command: status."""
    runner = CliRunner()
    result = runner.invoke(main, ["status"])
    expected_output = "State/configuration of current telliot client."

    assert result.exit_code == 0
    assert expected_output in result.output
