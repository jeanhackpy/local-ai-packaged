# Bolt's Journal - Critical Learnings Only

## 2025-05-15 - Optimizing LLM Router Concurrency and Latency
**Learning:** In Python-based AI pipes (like `router_pipe.py`), using synchronous `requests` inside an `async pipe` method blocks the entire event loop, preventing concurrent request processing. Additionally, LLM-based classification (difficulty evaluation) can be significantly sped up by limiting token generation with `num_predict`.

**Action:** Always offload blocking `requests` calls to `asyncio.to_thread` and use `num_predict: 5` (or similar low value) for simple "Easy/Hard" classification tasks to minimize latency. Ensure `__pycache__` is never staged by using specific file paths with `git add`.
