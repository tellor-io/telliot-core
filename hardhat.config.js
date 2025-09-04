require("@nomiclabs/hardhat-ethers");

/**
 * @type import('hardhat/config').HardhatUserConfig
 */
module.exports = {
  networks: {
    hardhat: {
      chainId: 1337,
      // Increase timeout for CI environments
      timeout: 120000,
      // Disable auto-mining for more realistic testing
      mining: {
        auto: true,
        interval: 1000
      }
    },
    localhost: {
      url: "http://127.0.0.1:8545",
      chainId: 1337,
      timeout: 120000
    }
  },
  solidity: {
    version: "0.8.19",
    settings: {
      optimizer: {
        enabled: true,
        runs: 200
      }
    }
  },
  // Increase test timeout for CI
  mocha: {
    timeout: 120000
  },
  // For CI environments
  paths: {
    sources: "./contracts",
    tests: "./test",
    cache: "./cache",
    artifacts: "./artifacts"
  }
};
