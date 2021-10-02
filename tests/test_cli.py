from click.testing import CliRunner
from telliot.cli import main


def test_status_cmd():
    """Test telliot CLI."""
    runner = CliRunner()
    result = runner.invoke(main, ["status"])
    expected_output = "State/configuration of current telliot client."

    assert result.exit_code == 0
    assert expected_output in result.output
