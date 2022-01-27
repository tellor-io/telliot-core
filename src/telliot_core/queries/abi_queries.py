from eth_abi import decode_abi

from telliot_core.queries.price.aws_spot_price import AWSSpotPrice
from telliot_core.queries.query import OracleQuery


ABI_QUERIES = {
    "AWSSpotPrice": AWSSpotPrice(
        parameters=[
            {
                "type": "string",
                "name": "zone",
                "value": "",
            },
            {
                "type": "string",
                "name": "instance",
                "value": "",
            },
        ]
    )
}


def get_query_from_data(query_data: bytes) -> OracleQuery:
    """Recreate an oracle query from `query_data`."""
    query_type, encoded_param_values = decode_abi(["string", "bytes"], query_data)
    query = ABI_QUERIES[query_type]

    param_types = [p["type"] for p in query.parameters]
    param_values = decode_abi(param_types, encoded_param_values)

    for idx, val in enumerate(param_values):
        query.parameters[idx]["value"] = val

    return query
