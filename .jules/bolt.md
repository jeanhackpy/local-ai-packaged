## 2025-05-14 - Pipe Optimization with Connection Pooling and Non-blocking I/O
**Learning:** Open WebUI pipes implemented in Python often use synchronous `requests` calls within an `async` environment. This blocks the event loop, severely limiting concurrency. Additionally, creating new connections for every request adds significant latency.
**Action:** Use `requests.Session()` at the class level for connection pooling and wrap synchronous calls in `asyncio.to_thread()` to maintain event loop responsiveness.
