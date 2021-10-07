from telliot.queries.query_registry import query_registry
from telliot.queries.query_registry import QueryRegistry


def test_query_registry():
    qr = query_registry

    exported = query_registry.json(indent=2)

    qr_restored = QueryRegistry.parse_raw(exported)

    reexported = qr_restored.json(indent=2)

    assert exported == reexported

    print(reexported)
