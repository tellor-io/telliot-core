""" This script exports the tellor query registry to json
"""
from telliot.queries.query_registry import query_registry
from telliot.queries.query_registry import QueryRegistry

exported = query_registry.json(indent=2)
print(exported)
with open("query_registry_export.json", "w") as f:
    f.write(exported)

imported = QueryRegistry.parse_raw(exported)
