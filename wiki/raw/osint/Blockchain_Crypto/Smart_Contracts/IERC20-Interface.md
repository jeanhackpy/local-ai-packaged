---
tags: [blockchain, smart-contract, erc20, interface]
---
### IERC20 Interface
This interface defines the standard functions for ERC20 tokens, including:
- `totalSupply()`: Returns the total supply of tokens.
- `balanceOf(address account)`: Returns the balance of a specific account.
- `transfer(address to, uint256 value)`: Transfers tokens to a specified address.
- `allowance(address owner, address spender)`: Returns the remaining number of tokens that a spender is allowed to spend on behalf of the owner.
- `approve(address spender, uint256 value)`: Sets the allowance for a spender.
- `transferFrom(address from, address to, uint256 value)`: Transfers tokens from one address to another using the allowance mechanism.

These interfaces provide a structured and standardized way to handle errors and operations for ERC20, ERC721, and ERC1155 tokens, improving the robustness and clarity of smart contract implementations.