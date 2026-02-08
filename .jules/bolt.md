## 2026-02-08 - Connection Pooling in AI Agent Pipes
**Learning:** Using synchronous `requests.post` in an `async` function blocks the event loop, and failing to use a `Session` object leads to redundant TCP/TLS handshakes for every request.
**Action:** Implement `requests.Session()` for connection pooling and use `asyncio.to_thread` for non-blocking I/O in async pipes.
