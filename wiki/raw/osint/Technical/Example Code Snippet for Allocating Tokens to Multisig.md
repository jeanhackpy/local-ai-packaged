### Example Code Snippet for Allocating Tokens to Multisig

Here's a simplified example of how you might allocate tokens to the multisig wallet after minting:

```solidity
// SPDX-License-Identifier: MIT
pragma solidity ^0.8.0;

import "@openzeppelin/contracts/token/ERC20/ERC20.sol";

contract MyToken is ERC20 {
    address public multisigWallet;

    constructor(address _multisigWallet) ERC20("MyToken", "MTK") {
        require(_multisigWallet != address(0), "Invalid multisig wallet address");
        multisigWallet = _multisigWallet;
        _mint(msg.sender, 499600000 * 10 ** decimals()); // Mint initial supply to deployer
        _mint(multisigWallet, 400000 * 10 ** decimals()); // Mint allocated tokens to multisig
    }
}
```

In this example:
- `MyToken` is an ERC20 token contract.
- The `multisigWallet` address is provided at deployment and used to allocate a portion of the minted tokens.