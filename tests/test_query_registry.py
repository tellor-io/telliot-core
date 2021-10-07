""" Unit tests for query registry

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from telliot.queries.query_registry import query_registry
from telliot.queries.query_registry import QueryRegistry


def test_registry_import_export():
    """Validate query registry JSON round trip"""

    exported = query_registry.json(indent=2)

    qr_restored = QueryRegistry.parse_raw(exported)

    reexported = qr_restored.json(indent=2)

    assert exported == reexported

    print(reexported)
