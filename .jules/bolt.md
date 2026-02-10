# Bolt's Journal - Local AI Packaged

## 2025-05-14 - Initial Assessment
**Learning:** The `n8n_pipe.py` script uses synchronous `requests` calls within an asynchronous `pipe` method, which blocks the event loop. It also lacks connection pooling and has a potential `UnboundLocalError`.
**Action:** Implement `requests.Session()` for connection pooling and `asyncio.to_thread()` to offload blocking I/O to a separate thread.

## 2025-05-14 - Python Bytecode Caution
**Learning:** Running `python3 -m py_compile` can generate `__pycache__` directories even with `PYTHONDONTWRITEBYTECODE=1` if not careful, which are binary artifacts that shouldn't be committed.
**Action:** Always verify and clean up `__pycache__` before submission.
