// SPDX-License-Identifier: MIT
pragma solidity ^0.8.10;

contract DIVAOracleMock {
    function getMinPeriodUndisputed() public pure returns (uint256) {
        return 3600;
    }
}
