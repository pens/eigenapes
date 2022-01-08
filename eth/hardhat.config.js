require('@nomiclabs/hardhat-ethers');
require('@nomiclabs/hardhat-etherscan');

const { etherscanApiKey, mnemonic, mainnetKey, rinkebyKey } = require('./secrets.json');

module.exports = {
  etherscan: {
    apiKey: etherscanApiKey
  },
  networks: {
    rinkeby: {
      url: `https://eth-rinkeby.alchemyapi.io/v2/${rinkebyKey}`,
      accounts: { mnemonic: mnemonic }
    },
    mainnet: {
      url: `https://eth-mainnet.alchemyapi.io/v2/${mainnetKey}`
    }
  },
  solidity: "0.8.11"
};
