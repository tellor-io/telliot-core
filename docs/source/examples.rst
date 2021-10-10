========
Examples
========


CoinPrice Query
---------------

.. jupyter-execute::
    :hide-code:

    import sys
    import os
    from decimal import Decimal
    sys.path.insert(0, os.path.abspath('../src'))

Create a CoinPrice query:

.. jupyter-execute::

    from telliot.queries.coin_price import CoinPrice
    q = CoinPrice(coin='btc')
    print(repr(q))

The :attr:`tip_data` attribute provides the ``data`` field to be provided with
the ``TellorX.Oracle.addTip()`` contract call.

.. jupyter-execute::

    print(q.tip_data)

or, in hex format:

.. jupyter-execute::

    print(f"0x{q.tip_data.hex()}")

The :attr:`tip_id` attribute provides the ``id`` field to be provided with
the ``TellorX.Oracle.addTip()`` contract call.

.. jupyter-execute::

    print(f"0x{q.tip_id.hex()}")

To encode response to the query, use the
ValueType.encode() method:

.. jupyter-execute::

    value = 99.1234567
    encoded_bytes = q.value_type.encode(value)
    print(f"0x{encoded_bytes.hex()}")

Validate the decoded bytes, with 6 decimals of precision:

.. jupyter-execute::

    decoded_value = q.value_type.decode(encoded_bytes)
    print(decoded_value)

