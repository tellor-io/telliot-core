""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import click
from telliot_core.apps.telliot_config import TelliotConfig
import json

@click.group()
def main() -> None:
    """Telliot command line interface

    """
    pass


@main.group()
def config() -> None:
    """Manage telliot_core configuration

    """
    pass

@config.command()
def init() -> None:
    """Create initial configuration files"""
    cfg = TelliotConfig()

@config.command()
def show() -> None:
    """Create initial configuration files"""
    cfg = TelliotConfig()
    print(json.dumps(cfg.get_state(), indent=2))


if __name__ == "__main__":
    main()
