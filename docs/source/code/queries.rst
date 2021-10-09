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
    telliot.queries.price_query.PriceQuery
    telliot.queries.legacy_query.LegacyQuery

Oracle Query Base Class
=======================


A , on the other hand,
is parameterized.  Therefore, a dynamic query can generate different values for
tip ``data`` and ``id`` when calling ``TellorX.Oracle.addTip()``.


.. autoclass:: telliot.queries.query.OracleQuery
    :members:

String Query Base Class
-----------------------

.. autoclass:: telliot.queries.string_query.StringQuery
   :members:


Price Query
-----------

.. autoclass:: telliot.queries.price_query.PriceQuery
   :members:


Legacy Query
------------

.. autoclass:: telliot.queries.legacy_query.LegacyQuery
   :members:


