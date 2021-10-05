""" This script exports the tellor query registry to json
"""
from telliot.query_registry import query_registry

exported = query_registry.json()
print(exported)
with open("query_registry_export.json", "w") as f:
    f.write(exported)
