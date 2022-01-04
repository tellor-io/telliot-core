import pytest
from click.testing import CliRunner

import telliot_core.cli.main
from telliot_core.apps.core import TelliotCore
from telliot_core.data.query_catalog import query_catalog
from telliot_core.queries import OracleQuery
from telliot_core.reporters.reporter_utils import tellorx_suggested_report


@pytest.mark.asyncio
async def test_suggested_report(rinkeby_cfg):
    async with TelliotCore(config=rinkeby_cfg) as core:
        qtag = await tellorx_suggested_report(core.tellorx.oracle)
        assert isinstance(qtag, str)
        entries = query_catalog.find(tag=qtag)
        assert len(entries) == 1
        catalog_entry = entries[0]
        q = catalog_entry.query
        assert isinstance(q, OracleQuery)


def test_suggested_report_cli():
    """Test suggested report CLI"""
    runner = CliRunner()
    result = runner.invoke(
        telliot_core.cli.main.main, ["--test_config", "query", "suggest"]
    )
    assert "Suggested query" in result.output
