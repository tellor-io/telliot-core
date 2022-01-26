# Creating New or Custom Oracle Queries

If your smart contract needs data that is not currently provided by the Tellor oracle network, this
section should help you get started.

The process of adding a new query to the Tellor network involves three steps:

1. [Define the new query][step-1-query-definition]
2. [Register the new query][step-2-query-registration]
3. [Create a data source to provide data for the new query][step-3-query-data-sources]

Technically speaking, the 3rd step above is not required, but it enables Tellor's existing
decentralized reporter network to automatically respond to the query. Without this step, customers
will be required to stand-up their own reporter network.

## Step 1: Query Definition

To define a new query, the first step is to specify its *Query Type*. If possible, it's easiest to
use one of the Query Types already defined for the Tellor network (
e.g. [`SpotPrice`][telliot_core.queries.price.spot_price.SpotPrice]). If none of the existing query
types work, you will need to [define a new query type][defining-new-query-types].

When using an existing Query Type, you'll need to specify the parameter values that correspond to
the data you would like put on-chain. For example, when using the `SpotPrice` query, you'll need to
specify the values for two parameters: `asset` and `currency`.

It is important to note the difference between defining a *Query Type* and a defining a *query*.
Defining a new Query Type creates an entire new class of queries, whereas defining a new *query*
refers to an instance of a QueryType with the value of each parameter specified.

To formally add the query definition to Tellor network, you'll need
to [propose changes][propose-changes] to
the [Tellor Data Specification Repository](https://github.com/tellor-io/dataSpecs).

## Step 2: Query Registration

Registering the new query makes users aware of the query and lets reporters know how to respond. It
requires [proposing changes][propose-changes] to
the [`telliot-core` repository](https://github.com/tellor-io/telliot-core), and must include two
things.

First, it must include a unit test for the new query. Using the pytest framework, create a unit test
that creates an instance of the query and verify that the values query descriptor, query data, and
query ID are sensible.

Second, it must be registered with the Query [`Catalog`][telliot_core.queries.catalog.Catalog].

The [example below][example-adding-a-new-spotprice] demonstrates how to test a new query and
register it in the catalog.

## Step 3: Query Data Sources

A query [`DataSource`][telliot_core.datasource.DataSource] provides a method to fetch new data
points in response to a query. It provides an API that enables Tellor's existing decentralized
reporter network to automatically respond to the query.

Ideally, a [`DataSource`][telliot_core.datasource.DataSource] should provide additional
decentralization and robustness by fetching data from multiple sources and aggregating the result.

A new [`DataSource`][telliot_core.datasource.DataSource] is created
by [proposing changes][propose-changes] to
the [`telliot-feed-examples` repository](https://github.com/tellor-io/telliot-feed-examples).

## Defining New Query Types

If none of the existing Tellor Query Types works for your application, you can define a new *Query
Type*.

A new *Query Type* definition specifies:

- The *name* of the query type
- The data type or structure of the value expected query response (i.e.
  its [`ValueType`][telliot_core.dtypes.value_type.ValueType])
- Optionally, the name and data type of each query *parameter*
- Encoding method - the method used to encode the Query Type and parameter values into
  the [`query_data`][telliot_core.queries.query.OracleQuery.query_data] field used for Tellor
  contract interactions.

It is important to note the difference between defining a *Query Type* and a defining a *query*.
Defining a new Query Type creates an entire new class of queries, whereas defining a new *query*
refers to an instance of a QueryType with the value of each parameter specified.

To define a new Query Type, [propose changes][propose-changes] to
the [`telliot-core` repository](https://github.com/tellor-io/telliot-core) defining a new subclass
of [`OracleQuery`][telliot_core.queries.query.OracleQuery] that implements all required methods and
properties.

New users may choose between subclassing [`JsonQuery`][telliot_core.queries.json_query.JsonQuery]
and the   
[`AbiQuery`][telliot_core.queries.abi_query.AbiQuery]. These queries are identical in every way
except for the coder/decoder that converts between the query name/parameters and the query data
field used in contract interfaces. The latter format is recommended if on-chain read/write access to
parameter values is required.

## Propose changes

To propose changes to a Tellor repository, perform the following steps:

1. Fork the tellor repository to your github account.
2. Make the proposed changes in your forked repository.
3. Submit a pull-request to incorporate the changes from your fork into the main tellor repository.

Alternately, standalone changes can be proposed in a separate repository, but it is the user's
responsibility to ensure compatibility with
the [`telliot-core`](https://github.com/tellor-io/telliot-core) framework.

## Example: Adding a new `SpotPrice`

In this example, a new [`SpotPrice`][telliot_core.queries.price.spot_price.SpotPrice] query is
defined for the price of BTC in USD.

To add a new spot price, use the
existing [`SpotPrice`][telliot_core.queries.price.spot_price.SpotPrice]
Query Type and simply define a new `asset`/`currency` pair.

*Example: Create and test the SpotPrice query for BTC/USD.*

```python
from telliot_core.api import SpotPrice


def test_new_query():
    q = SpotPrice(asset="BTC", currency="USD")
    assert q.descriptor == '{"type":"SpotPrice","asset":"btc","currency":"usd"}'
    assert q.query_data == b'{"type":"SpotPrice","asset":"btc","currency":"usd"}'
    assert q.query_id.hex() == "d66b36afdec822c56014e56f468dee7c7b082ed873aba0f7663ec7c6f25d2c0a"
```

*Example: Add the query to the Query [`Catalog`][telliot_core.queries.catalog.Catalog]*

Add the following statements to `telliot_core.data.query_catalog.py`.

```python
query_catalog.add_entry(
    tag="btc-usd-spot", title="BTC/USD spot price", q=SpotPrice(asset="BTC", currency="USD")
)

```










