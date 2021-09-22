""" Telliot CLI

A simple interface for interacting with telliot's functionality.
Configure telliot's settings via this interface's command line flags
or in the configuration file.
"""
import click

from .plugins.rinkeby_btc_usd.reporter import btc_usd_reporter


@click.group()
def main() -> None:
    """Run the CLI."""
    pass


@main.command()
def report() -> None:
    """Report data to Tellor oracle."""
    click.echo("Reporting data to Tellor oracle.")
    btc_usd_reporter.run()


@main.command()
def status() -> None:
    """Print state & configurations of current telliot client."""
    click.echo("State/configuration of current telliot client.")


if __name__ == "__main__":
    main()
