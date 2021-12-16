import click
import yaml

from telliot_core.apps.telliot_config import TelliotConfig


@click.group()
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
