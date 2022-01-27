from typing import Any

from eth_abi import encode_abi

from telliot_core.queries.query import OracleQuery


class AbiQuery(OracleQuery):
    """An Oracle Query that uses ABI-encoding to compute the query_data."""

    parameters: list[dict[str, Any]]

    @property
    def query_data(self) -> bytes:
        """Encode the query type and parameters to create the query data.

        This method uses ABI encoding to encode the query's parameter values.
        A valid JSON ABI specification is required to perform the encoding.
        (see https://docs.soliditylang.org/en/v0.5.3/abi-spec.html).
        """

        param_types = [p["type"] for p in self.parameters]
        param_values = [p["value"] for p in self.parameters]
        encoded_params = encode_abi(param_types, param_values)

        return encode_abi(["string", "bytes"], [self.type, encoded_params])

    @staticmethod
    def get_query_from_data(query_data: bytes) -> OracleQuery:
        # Implemented in telliot_core.queries.abi_queries
        pass
