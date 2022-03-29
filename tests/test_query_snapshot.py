""" Unit tests for Snapshot queries

Copyright (c) 2021-, Tellor Development Community
Distributed under the terms of the MIT License.
"""
from eth_abi import decode_abi

from telliot_core.queries.snapshot import Snapshot


def test_constructor():
    """Validate snapshot query."""
    q = Snapshot(proposal_id="QmbZ6cYVvfoKvkDX14jRcN86z6bfV135npUfhxmENjHnQ1")

    exp = b"\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00@\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x08Snapshot\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x80\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00 \x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00.QmbZ6cYVvfoKvkDX14jRcN86z6bfV135npUfhxmENjHnQ1\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00\x00"  # noqa: E501

    assert q.query_data == exp

    query_type, encoded_param_vals = decode_abi(["string", "bytes"], q.query_data)
    assert query_type == "Snapshot"

    proposal_id = decode_abi(["string"], encoded_param_vals)[0]
    assert isinstance(proposal_id, str)
    assert proposal_id == "QmbZ6cYVvfoKvkDX14jRcN86z6bfV135npUfhxmENjHnQ1"

    exp = "6ec98c95cf3aec7866c0fd1617c62e779a494ed49e689f578e14a5a0a0d99349"
    assert q.query_id.hex() == exp


def test_encode_decode_reported_val():
    """Ensure expected encoding/decoding behavior."""
    q = Snapshot(proposal_id="aDd6cYVvfoKvkDX14jRcN86z6bfV135npUfhxmENjHnQ1")

    # An array of values representing the amount of votes (uints) for each vote option
    votes = [500, 10, 35]

    submit_value = q.value_type.encode(votes)
    assert isinstance(submit_value, bytes)

    decoded_votes = list(q.value_type.decode(submit_value))
    assert isinstance(decoded_votes, list)

    assert decoded_votes[2] == 35
