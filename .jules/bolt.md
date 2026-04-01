## 2025-05-14 - Non-blocking I/O without new dependencies
**Learning:** In environments where adding new dependencies (like `httpx`) is restricted, `asyncio.to_thread` with `requests` is an effective way to achieve non-blocking I/O in async Open WebUI pipes.
**Action:** Use `asyncio.to_thread(requests.post, ...)` when `httpx` is not available to prevent blocking the event loop during LLM inference calls.
