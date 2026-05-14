### GnosisSafeProxy

- **Purpose**: Acts as a generic proxy that delegates calls to a master contract (singleton).
- **Constructor**: Initializes the proxy with the address of the singleton contract.
- **Fallback Function**: 
  - Uses inline assembly to handle all calls and forwards them to the singleton contract.
  - If the function signature matches `masterCopy()`, it returns the address of the singleton.
  - Otherwise, it delegates the call to the singleton and returns its result.