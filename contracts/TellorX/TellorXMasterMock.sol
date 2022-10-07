// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.10;

contract TellorXMasterMock {

    struct Dispute {
        bytes32 hash;
        int256 tally;
        bool executed;
        bool disputeVotePassed;
        bool isPropFork;
        address reportedMiner;
        address reportingParty;
        address proposedForkAddress;
        mapping(bytes32 => uint256) disputeUintVars;
        mapping(address => bool) voted;
    }
    mapping(uint256 => Dispute) public disputesById;

    function getStakerInfo(address _staker)
        external view
        returns (uint256, uint256)
    {
        return (uint256(1), uint256(123456789));
    }
}
