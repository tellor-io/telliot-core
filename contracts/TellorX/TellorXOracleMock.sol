// SPDX-Licence-Identifier: MIT
pragma solidity ^0.8.10;

contract TellorXOracleMock {
    function getReportTimestampByIndex(bytes32 _queryId, uint256 _index)
        public
        pure
        returns (uint256)
    {
        return 1234;
    }
}
