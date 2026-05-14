### GnosisSafeProxyFactory

- **Purpose**: Allows creation of new `GnosisSafeProxy` instances and executes calls on them.
- **Events**: `ProxyCreation` is emitted when a new proxy is created.
- **Functions**:
  - **createProxy**: Creates a new proxy and optionally executes a transaction on it.
  - **proxyRuntimeCode**: Returns the runtime bytecode of the `GnosisSafeProxy` contract.
  - **proxyCreationCode**: Returns the creation bytecode of the `GnosisSafeProxy` contract.
  - **deployProxyWithNonce**: Internal function to create a proxy using `CREATE2` opcode, allowing predictable address generation based on a salt.
  - **createProxyWithNonce**: Public function to create a proxy with `CREATE2`, execute an initializer call, and emit an event.
  - **createProxyWithCallback**: Creates a proxy, executes an initializer call, and invokes a callback after successful deployment.
  - **calculateCreateProxyWithNonceAddress**: Calculates the address of a proxy that would be created using `CREATE2` without actually deploying it. This is useful for address prediction.