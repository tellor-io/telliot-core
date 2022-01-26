# New Oracle  Queries

If your smart contract needs data that is not currently provided by the Tellor oracle network, this
section should help you get started.

The process of adding a new query to the Tellor network involves three steps:

1. [Define the new query][query-definition]
2. [Register the new query][query-registration]
3. [Create a data source to provide data for the new query][query-data-sources]

## Query Definition

To define a new query, the first step is to specify its *Query Type*. If possible, it's easiest to
use one of the Query Types already defined for the Tellor network (
e.g. [`SpotPrice`][telliot_core.queries.price.spot_price.SpotPrice]). If none of the existing query
types work, you will need to [define a new query type][new-query-types].

When using an existing Query Type, you'll need to specify the parameter values that correspond to
the data you would like put on-chain. For example, when using the `SpotPrice` query, you'll need to
specify the values for two parameters: `asset` and `currency`.

It is important to note the difference between a *Query Type* and a *Query*, which is an instance of
a Query Type including the values of each parameter.

To formally add the query definition to Tellor network, you'll need
to [propose changes][propose-changes] to
the [Tellor Data Specification Repository](https://github.com/tellor-io/dataSpecs).

## Query Registration

Registering a new query requires the following steps:

1. Add the query to the Query [`Catalog`][telliot_core.queries.catalog.Catalog]
2. 
Add the new query the [`telliot-core` Repository](https://github.com/tellor-io/telliot-core)
and query catalog so that the users are aware and know how to respond to the new query.

## Query Data Sources

in [`telliot-feed-examples`](https://github.com/tellor-io/telliot-feed-examples) so that reporters
know how to fetch data for the new query.

To add a new spot price, you should re-use the existing
[`SpotPrice`][telliot_core.queries.price.spot_price.SpotPrice] Query Type and simply define a
new `asset`/`currency` pair.

## New Query Types

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
Defining a new Query Type creates an entire new class of queries, whereas defining a new query
refers to an instance of a QueryType with specified parameters.

*TODO: Explain process of defining a new query type.*
In the meantime, please reach out to Tellor on discord for more help.

## Propose changes

To propose changes to a Tellor repository, perform the following steps:

1. Fork the tellor repository to your github account.
2. Make the proposed changes in your forked repository.
3. Submit a pull-request to incorporate the changes from your fork into the main tellor repository.


## Example: New Spot Price


###







