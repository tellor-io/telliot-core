from telliot_core.queries.query_catalog import query_catalog

with open('query_catalog.md', 'w') as f:
    f.write(query_catalog.to_markdown())

with open('query_catalog.yaml', 'w') as f:
    f.write(query_catalog.to_yaml())

