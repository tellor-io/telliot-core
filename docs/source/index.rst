.. pytelliot documentation master file, created by
   sphinx-quickstart on Thu Sep  2 14:15:56 2021.
   You can adapt this file completely to your liking, but it should at least
   contain the root `toctree` directive.

Welcome to Telliot's documentation
===================================

Telliot is a Python framework for interacting with the decentralized TellorX network.
With Telliot, you (or your smart contract) can:

- Ask the TellorX Decentralized Oracle to answer a question

  - (we call that *tipping*)

- Submit answers to questions that other people (or smart contracts) ask.

  - (we call that *reporting*.  Reporters earn tips, but must stake TRB
    as collateral against incorrect answers)

- Look up historical answers.

- Help maintain the security of the TellorX network by disputing inaccurate
  answers and voting on other disputes.

Of course, TellorX supports DeFi with questions such as "What is the
current price of Bitcoin in US Dollars?"  But that is just the beginning.
TellorX also supports arbitrary questions and answers.  Any question is OK, provided
that the We are Tellor community can answer it with a reasonable
degree of confidence (remember, Reporters may lose TRB if the network votes
the answer incorrect!)

Scope
-----

Telliot aims to make it easier to ask questions in a format that the Oracle
can understand, and specify the format (i.e. data structure) of the
answers you would like to receive - so that the community can answer
them more reliably.

The TellorX network is open to everyone, and Telliot is just
one way to access it.  You can use all of Telliot, parts of it, or not
use it at all.  You can also make contributions to improve it.

Use Telliot at your own risk.  **It may have bugs!  Bugs may cost you real money!**
If you find any, please `submit an issue`_, or better yet `create a pull request`_ with a
suggested fix.



.. _submit an issue: https://github.com/tellor-io/pytelliot/issues

.. _create a pull request: https://github.com/tellor-io/pytelliot/pulls


Contents
--------

.. toctree::
   :maxdepth: 1

   Code Reference <code/code>
   Examples <examples>
   Getting Started <getting_started>
   Reporter Application <reporter_app>



Indices and tables
==================

* :ref:`genindex`
* :ref:`modindex`
* :ref:`search`
