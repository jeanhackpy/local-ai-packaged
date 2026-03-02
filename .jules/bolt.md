## 2025-05-14 - Non-blocking I/O in Async Pipes

**Learning:** In Open WebUI pipes (which are asynchronous), using synchronous `requests` calls blocks the entire event loop, preventing concurrent request handling. This is a common bottleneck in Python-based agentic workflows.

**Action:** Always offload blocking `requests` calls to background threads using `asyncio.to_thread()` when `httpx` is not available, or use `httpx.AsyncClient()` for true non-blocking I/O.
