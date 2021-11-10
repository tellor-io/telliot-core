""" Telliot CLI

A simple interface for interacting with telliot_core's functionality.
Configure telliot_core's settings via this interface's command line flags
or in the configuration file.
"""
import click
import yaml
from telliot_core.apps.telliot_config import TelliotConfig


@click.group()
def main() -> None:
    """Telliot command line interface"""
    pass


@main.group()
def config() -> None:
    """Manage telliot_core configuration"""
    pass


@config.command()
def init() -> None:
    """Create initial configuration files"""
    _ = TelliotConfig()


@config.command()
def show() -> None:
    """Create initial configuration files"""
    cfg = TelliotConfig()
    print(yaml.dump(cfg.get_state(), sort_keys=False))


if __name__ == "__main__":
    main()
