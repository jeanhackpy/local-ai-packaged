## 2025-05-15 - Async I/O in Open WebUI Pipes
**Learning:** Open WebUI Pipes are asynchronous, but using synchronous libraries like `requests` inside them blocks the entire Python event loop. This prevents concurrency and can cause the entire UI to hang while waiting for one slow LLM response. `httpx.AsyncClient` provides a thread-safe connection pool and true non-blocking I/O.
**Action:** Always prefer `httpx` or other async-native libraries for network calls in Pipes. Initialize the client once in `__init__` to benefit from connection pooling.
