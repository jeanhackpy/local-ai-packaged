# Bolt's Performance Journal

## 2025-05-15 - Fast-path and Non-blocking I/O in Router Pipe
**Learning:** In Open WebUI pipes, synchronous `requests` calls block the entire event loop, preventing concurrent query handling. Implementing a fast-path for short queries (< 15 characters) and using `asyncio.to_thread` significantly improves responsiveness and throughput.
**Action:** Always wrap synchronous I/O in `asyncio.to_thread` when working in async pipes, and look for heuristic-based shortcuts to bypass expensive LLM calls.
