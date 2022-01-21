import asyncio
from functools import wraps

import click

from telliot_core.apps.core import TelliotCore
from telliot_core.apps.telliot_config import override_test_config
from telliot_core.apps.telliot_config import TelliotConfig


def async_run(f):  # type: ignore
    """Call and run an async function.

    Handy Click CLI tests of async functions."""

    @wraps(f)
    def wrapper(*args, **kwargs):  # type: ignore
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def cli_config(ctx: click.Context) -> TelliotConfig:
    """Return a telliot configuration using the CLI context"""
    if ctx.obj["TEST_CONFIG"]:
        cfg = override_test_config(TelliotConfig())

    else:
        cfg = TelliotConfig()
        if ctx.obj.get("CHAIN_ID", None):
            cfg.main.chain_id = ctx.obj["CHAIN_ID"]

    return cfg


def cli_core(ctx: click.Context) -> TelliotCore:
    """Returns a TelliotCore configured with the CLI context

    The returned object should be used as a context manager for CLI commands
    """
    account_name = ctx.obj.get("ACCOUNT_NAME", None)

    cfg = cli_config(ctx)
    core = TelliotCore(config=cfg, account_name=account_name)
    return core
