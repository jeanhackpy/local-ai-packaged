## 2025-05-15 - [Initial performance assessment]
**Learning:** Found synchronous `requests` calls in asynchronous Open WebUI pipes (`n8n_pipe.py` and `router_pipe.py`). This blocks the event loop and prevents concurrent request handling. Also, `router_pipe.py` lacks a fast-path for short queries, causing unnecessary LLM evaluations.
**Action:** Use `asyncio.to_thread` for blocking I/O and implement a short-query fast-path heuristic.
