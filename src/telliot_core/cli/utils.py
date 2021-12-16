import click

from telliot_core.apps.core import TelliotCore


def get_app(ctx: click.Context) -> TelliotCore:
    """Get an app configured using CLI context"""

    app = TelliotCore.get() or TelliotCore()

    chain_id = ctx.obj["chain_id"]
    if chain_id is not None:
        assert app.config
        app.config.main.chain_id = chain_id

    _ = app.connect()

    assert app.config
    assert app.tellorx

    return app
