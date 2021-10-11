===============
Queries Package
===============

.. automodule:: telliot.queries

.. rubric:: Submodules

.. autosummary::
    :nosignatures:

    query
    legacy_query
    coin_price
    string_query

.. rubric:: Classes

.. autosummary::
    :nosignatures:

    telliot.queries.query.OracleQuery
    telliot.queries.legacy_query.LegacyQuery
    telliot.queries.coin_price.CoinPrice
    telliot.queries.string_query.StringQuery

Query Types
===========

Base Query Class
----------------


.. autoclass:: telliot.queries.query.OracleQuery
    :members:


Legacy Query
------------

See Also: :ref:`Legacy Query Example <legacy_query_example>`

.. autoclass:: telliot.queries.legacy_query.LegacyQuery
   :members:

Coin Price
----------

See Also: :ref:`CoinPrice Example <coinprice_query_example>`

.. autoclass:: telliot.queries.coin_price.CoinPrice
   :members:

String Query
------------

See Also: :ref:`Text Query Example <text_query_example>`

.. autoclass:: telliot.queries.string_query.StringQuery
   :members:


Value Types
============

Base Value Type
---------------

.. autoclass:: telliot.queries.value_type.ValueType
   :members:

Legacy Value Type
-----------------

.. autoclass:: telliot.queries.legacy_query.LegacyValueType
   :members:

CoinPrice Value Type
--------------------

.. autoclass:: telliot.queries.coin_price.CoinPriceValue
   :members:

