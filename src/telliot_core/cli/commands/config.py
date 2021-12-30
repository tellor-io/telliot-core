from typing import Optional

import click
import yaml
import os

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

    # remove stakers private keys
    stakers = state.pop("stakers")
    stakers = stakers.pop("stakers")
    for staker in stakers:
        staker.pop("private_key")

    print(yaml.dump(state, sort_keys=False))
    print(yaml.dump(stakers, sort_keys=False))


@config.command()
@click.option('-c', '--chain_id', type=int, default=None, help="Chain ID")
def set(chain_id: Optional[int]) -> None:
    """Set a configuration parameter."""
    cfg = TelliotConfig()
    modified = False

    if chain_id:
        cfg.main.chain_id = chain_id
        modified = True

    if modified:
        cfg._main_config_file.save_config(cfg.main)


@config.command()
def git() -> None:
    """Custom configuration for rinkeby testing on git.

    FOR DEVELOPMENT USE ONLY.
    """
    cfg = TelliotConfig()

    # Override configuration for rinkeby testnet
    override_main = False
    if cfg.main.chain_id != 4:
        cfg.main.chain_id = 4
        override_main = True

    rinkeby_endpoint = cfg.get_endpoint()

    override_endpoint = False
    if os.getenv("NODE_URL", None):
        rinkeby_endpoint.url = os.environ["NODE_URL"]
        override_endpoint = True

    # Replace staker private key
    override_staker = False
    if os.getenv("PRIVATE_KEY", None):
        override_staker = True
        private_key = os.environ["PRIVATE_KEY"]
        rinkeby_stakers = cfg.stakers.find(chain_id=4)
        if len(rinkeby_stakers) == 0:
            raise Exception("No staker/private key defined for rinkeby")
        rinkeby_staker = rinkeby_stakers[0]
        rinkeby_staker.private_key = private_key
        rinkeby_staker.address = "0x8D8D2006A485FA4a75dFD8Da8f63dA31401B8fA2"

    if override_staker:
        cfg._staker_config_file.save_config(cfg.stakers)
    if override_endpoint:
        cfg._ep_config_file.save_config(cfg.endpoints)
    if override_main:
        cfg._main_config_file.save_config(cfg.main)
