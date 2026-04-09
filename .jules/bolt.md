## 2025-05-15 - Event Loop Blocking via Synchronous I/O
**Learning:** Synchronous `requests.post` calls inside `async` methods block the entire Python event loop, causing concurrent requests to be serialized. In `n8n_pipe.py`, this meant three 1s requests took 3s total, as the loop was unable to switch tasks while waiting for I/O.
**Action:** Always offload synchronous I/O to a separate thread using `asyncio.to_thread` when working in an `async` context to ensure the event loop remains responsive and handles requests concurrently.

## 2025-05-15 - Importance of Manual Cleanup for Binary Artifacts
**Learning:** Tools like `ruff` or benchmark runs can generate `__pycache__` directories containing `.pyc` files, which are a major blocker for PR approval if not removed.
**Action:** Manually search for and remove all `__pycache__` directories (e.g., using `find . -name "__pycache__" -type d -exec rm -rf {} +`) before final submission to maintain repository hygiene.
