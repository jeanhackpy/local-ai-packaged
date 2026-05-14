---
tags: [blockchain, smart-contract, erc1155, errors, interface]
---
### IERC1155Errors Interface
This interface defines custom error types for ERC1155 tokens. The errors include:
- `ERC1155InsufficientBalance`: Thrown when a sender's balance is insufficient for a transfer.
- `ERC1155InvalidSender`: Thrown when the sender address is invalid.
- `ERC1155InvalidReceiver`: Thrown when the receiver address is invalid.
- `ERC1155MissingApprovalForAll`: Thrown when the operator lacks approval for all tokens.
- `ERC1155InvalidApprover`: Thrown when the approver address is invalid.
- `ERC1155InvalidOperator`: Thrown when the operator address is invalid.
- `ERC1155InvalidArrayLength`: Thrown when there is a mismatch in array lengths for batch transfers.