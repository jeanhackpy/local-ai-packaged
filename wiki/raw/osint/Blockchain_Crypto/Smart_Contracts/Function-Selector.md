---
tags: [blockchain, smart-contract, function-selector, ethereum, concept]
---
### Function Selector

The first 4 bytes (`0x19ff3a43`) are the function selector, which is derived from the first 4 bytes of the Keccak-256 hash of the function signature. To find out which function this corresponds to, we can use an online tool like [4byte.directory](https://www.4byte.directory/).

Assuming we found the function signature, let's proceed with decoding the rest.