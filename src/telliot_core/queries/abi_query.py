from telliot_core.queries.query import OracleQuery


class AbiQuery(OracleQuery):
    """An Oracle Query that uses ABI-encoding to compute the query_data."""

    @property
    def query_data(self) -> bytes:
        """Encode the query `descriptor` to create the query `data` field for
        use in the ``TellorX.Oracle.tipQuery()`` contract call.

        This method uses ABI encoding to encode the values in the Query Descriptor.
        A valid JSON ABI specification is required to perform the encoding.
        (see https://docs.soliditylang.org/en/v0.5.3/abi-spec.html).

        TODO: Implement for AbiQuery
        """
        raise NotImplementedError

    @staticmethod
    def get_query_from_data(query_data: bytes) -> OracleQuery:
        """Recreate an oracle query from `query_data`

        TODO: Implement for AbiQuery
        """
        raise NotImplementedError
