# Legacy Query Example

The following example demonstrates how to create a 
[`LegacyRequest`][telliot_core.queries.legacy_query.LegacyRequest]
requesting the ETH/USD price.  The legacy request ID for ETH/USD is `1`, 
in accordance with the 
[Legacy Data Feed ID Specifications](https://docs.tellor.io/tellor/integration/data-ids/current-data-feeds).

Create a LegacyQuery and view the corresponding query descriptor:

```python hl_lines="4-5"
--8<-- "examples/legacy_query_example.py"
```

The query descriptor string uniquely identifies this query to the 
TellorX Oracle network.

```json
{"type":"LegacyRequest","legacy_id":1}
```

To make the corresponding on-chain Query request, 
the `TellorX.Oracle.tipQuery()` contract call
requires two arguments: `queryData` and `queryId`.  These arguments are provided by 
the `query_data` and `query_id` attributes of the `LegacyQuery` object:

```python hl_lines="6 7"
--8<-- "examples/legacy_query_example.py"
```

which, for this example, are:

    tipQuery data: 0x7b2274797065223a224c656761637952657175657374222c226c65676163795f6964223a317d
    tipQuery ID: 0x0000000000000000000000000000000000000000000000000000000000000001

The `LegacyQuery` object also demonstrates how to encode a response
to submit on-chain using the `TellorX.Oracle.submitValue()` contract call.

For example, to submit the value `10000.1234567`, use the 
[`encode`][telliot_core.types.value_type.ValueType.encode] and 
[`decode`][telliot_core.types.value_type.ValueType.decode] methods of the response
[`ValueType`][telliot_core.types.value_type.ValueType].

```python hl_lines="9-16"
--8<-- "examples/legacy_query_example.py"
```

Note that the on-chain and decoded values are limited to 
6 decimals of precision in accordance with the on-chain data type:

    submitValue (float): 10000.1234567
    submitValue (bytes): 0x00000000000000000000000000000000000000000000000000000002540dc641
    Decoded value (float): 10000.123457
