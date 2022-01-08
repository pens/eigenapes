const { ethers } = require('hardhat');

// From https://docs.openzeppelin.com/learn/deploying-and-interacting#deploying-a-smart-contract
async function main () {
  // From https://github.com/nomiclabs/hardhat/issues/1159#issuecomment-789310120
  const ethProvider = require('eth-provider');
  const frame = ethProvider('frame');

  const factory = await ethers.getContractFactory('Eigenapes');

  /*
  During development:

  const contract = await factory.deploy();
  await contract.deployed();
  console.log('Deployed to:', contract.address);
  */

  /*
  For release:
  */

  const tx = await factory.getDeployTransaction();

  tx.from = (await frame.request({ method: 'eth_requestAccounts' }))[0];
  console.log('Sending from:', tx.from);

  const hash = await frame.request({ method: 'eth_sendTransaction', params: [tx] });
  console.log('Deployed to:', hash);
}

main()
  .then(() => process.exit(0))
  .catch(error => {
    console.error(error);
    process.exit(1);
  });