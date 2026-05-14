---
tags: [blockchain, smart-contract, erc721, errors, interface]
---
### IERC721Errors Interface
This interface defines custom error types for ERC721 tokens. The errors include:
- `ERC721InvalidOwner`: Thrown when an address can't be an owner, e.g., the zero address.
- `ERC721NonexistentToken`: Thrown when a token with the specified ID does not exist.
- `ERC721IncorrectOwner`: Thrown when the sender is not the owner of the token.
- `ERC721InvalidSender`: Thrown when the sender address is invalid.
- `ERC721InvalidReceiver`: Thrown when the receiver address is invalid.
- `ERC721InsufficientApproval`: Thrown when the operator lacks sufficient approval.
- `ERC721InvalidApprover`: Thrown when the approver address is invalid.
- `ERC721InvalidOperator`: Thrown when the operator address is invalid.