from telliot_core.queries.query import OracleQuery


class AbiQuery(OracleQuery):
    """An Oracle Query that uses ABI-encoding to compute the query_data."""

    @property
    def descriptor(self) -> str:
        """Get the query descriptor string.

        The Query descriptor is a unique, human-readable string representation
        of the query (including it's parameters).  There must be a one-to-one
        correspondence between the descriptor string and the query_data.

        TODO: Implement for AbiQuery
        """
        raise NotImplementedError

    @property
    def query_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.tipQuery()``
        contract call.

        TODO: Implement for AbiQuery
        """
        raise NotImplementedError
