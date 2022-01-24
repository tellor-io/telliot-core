from telliot_core.queries.query import OracleQuery


class JsonQuery(OracleQuery):
    """An Oracle Query that uses JSON-encoding to compute the query_data."""

    @property
    def query_data(self) -> bytes:
        """Encode the query `descriptor` to create the query `data` field for
        use in the ``TellorX.Oracle.tipQuery()`` contract call.

        """
        return self.descriptor.encode("utf-8")
