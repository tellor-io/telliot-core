""" Telliot CLI

A simple interface for interacting with telliot's functionality.
Configure telliot's settings via this interface's command line flags
or in the configuration file.
"""
import click

from telliot.reporter.simple_interval import IntervalReporter
from telliot.datafeed.example import data_feeds


@click.group()
def main() -> None:
    """Run the CLI."""
    pass


@main.command()
@click.argument('datafeed_uid')
def report(datafeed_uid) -> None:
    """Report data to Tellor oracle."""
    click.echo(f"Reporting to the Tellor oracle.")
    reporter = IntervalReporter(data_feeds, datafeed_uid)
    reporter.run()


@main.command()
def status() -> None:
    """Print state & configurations of current telliot client."""
    click.echo("State/configuration of current telliot client.")


if __name__ == "__main__":
    main()
