# Bolt's Performance Journal

## 2026-02-09 - [n8n_pipe.py optimization]
**Learning:** Found that `n8n_pipe.py` uses synchronous `requests.post` inside an async `pipe` method, which blocks the event loop and doesn't use connection pooling.
**Action:** Implement `requests.Session()` for connection pooling and use `asyncio.to_thread()` to avoid blocking the event loop.
