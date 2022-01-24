from typing import Optional

import click
import yaml

from telliot_core.apps.telliot_config import override_test_config
from telliot_core.apps.telliot_config import TelliotConfig


@click.group()
def config() -> None:
    """Manage Telliot configuration."""
    pass


@config.command()
def init() -> None:
    """Create initial configuration files."""
    _ = TelliotConfig()


@config.command()
def show() -> None:
    """Show current configuration."""
    cfg = TelliotConfig()
    state = cfg.get_state()

    print(yaml.dump(state, sort_keys=False))


@config.command()
@click.option("-c", "--chain_id", type=int, default=None, help="Chain ID")
def set(chain_id: Optional[int]) -> None:
    """Set a configuration parameter."""
    cfg = TelliotConfig()
    modified = False

    if chain_id:
        cfg.main.chain_id = chain_id
        modified = True

    if modified:
        assert cfg._main_config_file is not None
        cfg._main_config_file.save_config(cfg.main)


@config.command()
def testconfig() -> None:
    """Custom configuration for rinkeby testing on git.

    Modifies the configuration files to use a rinkeby test
    configuration, using github secrets if they are defined

    FOR DEVELOPMENT USE ONLY.
    """
    _ = override_test_config(TelliotConfig(), write=True)
