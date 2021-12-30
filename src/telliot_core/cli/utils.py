import asyncio
from functools import wraps

import click

from telliot_core.apps.core import TelliotCore
from telliot_core.apps.telliot_config import override_test_config
from telliot_core.apps.telliot_config import TelliotConfig


def get_app(ctx: click.Context) -> TelliotCore:
    """Get an app configured using CLI context"""

    app = TelliotCore.get() or TelliotCore()

    chain_id = ctx.obj["chain_id"]
    if chain_id is not None:
        assert app.config
        app.config.main.chain_id = chain_id

    _ = app.startup()

    assert app.config
    assert app.tellorx

    return app


def async_run(f):  # type: ignore
    """Call and run an async function.

    Handy Click CLI tests of async functions."""

    @wraps(f)
    def wrapper(*args, **kwargs):  # type: ignore
        return asyncio.run(f(*args, **kwargs))

    return wrapper


def cli_core(ctx: click.Context) -> TelliotCore:
    """Returns a TelliotCore configured with the CLI context"""
    if ctx.obj["test_config"]:
        cfg = override_test_config(TelliotConfig())

    else:
        cfg = TelliotConfig()
        if ctx.obj["chain_id"]:
            cfg.main.chain_id = ctx.obj["chain_id"]

    return TelliotCore(config=cfg)
