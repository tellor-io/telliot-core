import json

from telliot_core.queries.query import OracleQuery


class JsonQuery(OracleQuery):
    """An Oracle Query that uses JSON-encoding to compute the query_data."""

    @property
    def descriptor(self) -> str:
        """Get the query descriptor string.
        The Query descriptor is a unique string representation of the query that,
        in encoded form, is also used as the `query_data`.

        """
        state = self.get_state()
        jstr = json.dumps(state, separators=(",", ":"))
        return jstr

    @property
    def query_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.tipQuery()``
        contract call.

        """
        return self.descriptor.encode("utf-8")
