""" Telliot CLI

A simple interface for interacting with telliot's functionality.
Configure telliot's settings via this interface's command line flags
or in the configuration file.
"""
import click
from telliot.apps.telliot_config import TelliotConfig

@click.group()
def main() -> None:
    """Telliot command line interface

    """
    pass


@main.group()
def config() -> None:
    """Manage telliot configuration

    """
    pass

@config.command()
def init() -> None:
    """Create initial configuration files"""
    cfg = TelliotConfig()



if __name__ == "__main__":
    main()
