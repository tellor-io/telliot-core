from typing import Any

from clamfig import deserialize
from eth_abi import decode_abi
from eth_abi import encode_abi

from telliot_core.queries.query import OracleQuery
from telliot_core.queries.query_abis import PARAMETERS_ABI_LOOKUP


class AbiQuery(OracleQuery):
    """An Oracle Query that uses ABI-encoding to compute the query_data."""

    # Mapping from query parameter name to abi type
    params_abi: list[dict[str, Any]]

    @property
    def query_data(self) -> bytes:
        """Encode the query type and parameters to create the query data.

        This method uses ABI encoding to encode the query's parameter values.
        A valid JSON ABI specification is required to perform the encoding.
        (see https://docs.soliditylang.org/en/v0.5.3/abi-spec.html).
        """

        param_values = [p["value"] for p in self.params_abi]
        param_types = [p["abi_type"] for p in self.params_abi]
        encoded_params = encode_abi(param_types, param_values)

        return encode_abi(["string", "bytes"], [type(self).__name__, encoded_params])

    @staticmethod
    def get_query_from_data(query_data: bytes) -> OracleQuery:
        query_type, encoded_param_values = decode_abi(["string", "bytes"], query_data)
        params_abi = PARAMETERS_ABI_LOOKUP[query_type]

        param_types = [p["abi_type"] for p in params_abi]
        param_values = decode_abi(param_types, encoded_param_values)

        for idx, val in enumerate(param_values):
            params_abi[idx]["value"] = val

        q = deserialize({"type": query_type, "params_abi": params_abi})
        q.__post_init__()

        return q  # type: ignore
