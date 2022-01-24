"""  Oracle Query Module

"""
from clamfig import Serializable
from web3 import Web3

from telliot_core.dtypes.value_type import ValueType


class OracleQuery(Serializable):
    """Oracle Query

    An OracleQuery specifies how to pose a question to the
    Tellor Oracle and how to format/interpret the response.

    The OracleQuery class serves
    as the base class for all Queries, and implements default behaviors.
    Each subclass corresponds to a unique Query Type supported
    by the TellorX network.

    All public attributes of an OracleQuery represent an input that can
    be used to customize the query.

    The base class provides:

    - Calculation of the contents of the `data` field to include with the
      `TellorX.Oracle.tipQuery()` contract call.

    - Calculation of the `id` field field to include with the
      `TellorX.Oracle.tipQuery()` and `TellorX.Oracle.submitValue()`
      contract calls.

    """

    @property
    def value_type(self) -> ValueType:
        """Returns the ValueType expected by the current Query configuration

        The value type defines required data type/structure of the
        ``value`` submitted to the contract through
        ``TellorX.Oracle.submitValue()``

        This method *must* be implemented by subclasses
        """
        raise NotImplementedError

    @property
    def descriptor(self) -> str:
        """Get the query descriptor string.

        The Query descriptor is a unique, human-readable string representation
        of the query (including it's parameters).  There must be a one-to-one
        correspondence between the descriptor string and the query_data.

        This method *must* be implemented by subclasses
        """
        raise NotImplementedError

    @property
    def query_data(self) -> bytes:
        """Returns the ``data`` field for use in ``TellorX.Oracle.tipQuery()``
        contract call.

        This method *must* be implemented by subclasses
        """
        raise NotImplementedError

    @property
    def query_id(self) -> bytes:
        """Returns the query ``id`` for use with the
        ``TellorX.Oracle.tipQuery()`` and ``TellorX.Oracle.submitValue()``
        contract calls.
        """
        return bytes(Web3.keccak(self.query_data))
