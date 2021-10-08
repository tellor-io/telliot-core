===============
Queries Package
===============

.. automodule:: telliot.queries

The Queries package provides a mechanism to itemize Oracle queries
and specify the format of the query and the response.
:class:`~telliot.queries.query.OracleQuery` an abstract base class
used for all Queries.

There are two basic types of Queries: static and dynamic.
A :class:`~telliot.queries.static_query.StaticQuery` uses a fixed value
for ``data`` when submitting to ``TellorX.Oracle.addTip()``.
It also uses a fixed value for the tip ``id``, which is computed
from the ``data`` using keccak hash algorithm.
A :class:`~telliot.queries.dynamic_query.DynamicQuery`, on the other hand,
is parameterized.  Therefore, a dynamic query can generate different values for
tip ``data`` and ``id`` when calling ``TellorX.Oracle.addTip()``.



.. rubric:: Submodules

.. autosummary::
    :nosignatures:

    query
    static_query
    price_query
    legacy_query
    query_registry

.. rubric:: Classes

.. autosummary::
    :nosignatures:

    telliot.queries.query.OracleQuery
    telliot.queries.dynamic_query.DynamicQuery

Base Query Classes
==================

Oracle Query Base Class
-----------------------

.. autoclass:: telliot.queries.query.OracleQuery
    :members:

Static Query Base Class
-----------------------

.. autoclass:: telliot.queries.static_query.StaticQuery
   :members:

Dynamic Query
-------------

.. autoclass:: telliot.queries.dynamic_query.DynamicQuery
   :members:

Price Query
===========

.. autoclass:: telliot.queries.price_query.PriceQuery
   :members:


Legacy Queries
==============

Legacy Query
------------

.. autoclass:: telliot.queries.legacy_query.LegacyQuery
   :members:

Legacy Price Query
------------------

.. autoclass:: telliot.queries.legacy_query.LegacyPriceQuery
   :members:


Helper Classes
==============


.. autoclass:: telliot.queries.query.SerializableSubclassModel
    :members: