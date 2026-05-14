---
tags: [blockchain, smart-contract, erc20, errors, interface]
---
### IERC20Errors Interface
This interface defines custom error types for ERC20 tokens, facilitating more descriptive error handling in smart contracts. The errors include:
- `ERC20InsufficientBalance`: Thrown when a sender's balance is insufficient for a transfer.
- `ERC20InvalidSender`: Thrown when the sender address is invalid.
- `ERC20InvalidReceiver`: Thrown when the receiver address is invalid.
- `ERC20InsufficientAllowance`: Thrown when the spender's allowance is insufficient.
- `ERC20InvalidApprover`: Thrown when the approver address is invalid.
- `ERC20InvalidSpender`: Thrown when the spender address is invalid.