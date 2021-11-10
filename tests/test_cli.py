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
