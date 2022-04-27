// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract AutopayMock {

    function getCurrentTip(bytes32 _queryId) public pure returns (uint256) {
        return _queryId.length;
    }
}
