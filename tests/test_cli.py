"""
Unit tests covering telliot CLI commands.
"""
from click.testing import CliRunner
from telliot.cli import main


def test_config_cmd():
    """Test telliot CLI command: report."""
    runner = CliRunner()
    result = runner.invoke(main, ["config", "init"])

    print(result)

