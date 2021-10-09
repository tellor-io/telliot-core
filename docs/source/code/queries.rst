===============
Queries Package
===============

.. automodule:: telliot.queries

Contents
========

.. rubric:: Submodules

.. autosummary::
    :nosignatures:

    query
    string_query
    price_query
    legacy_query

.. rubric:: Classes

.. autosummary::
    :nosignatures:

    telliot.queries.query.OracleQuery
    telliot.queries.string_query.StringQuery
    telliot.queries.price_query.CoinPrice
    telliot.queries.legacy_query.LegacyQuery

Oracle Query Base Class
=======================

.. autoclass:: telliot.queries.query.OracleQuery
    :members:

Oracle Query Types
==================

Legacy Query
------------

.. autoclass:: telliot.queries.legacy_query.LegacyQuery
   :members:

String Query
------------

.. autoclass:: telliot.queries.string_query.StringQuery
   :members:


Coin Price
----------

.. autoclass:: telliot.queries.coin_price.CoinPrice
   :members:




Value Types
============

.. autoclass:: telliot.queries.value_type.ValueType
   :members:
