# Bolt's Performance Journal

## 2025-05-15 - Fast-path Heuristics for LLM Routing
**Learning:** For routing tasks that involve an LLM evaluation, a simple string length check can bypass network I/O and inference for common simple queries (e.g., greetings), reducing latency by ~43% for those cases.
**Action:** Always consider fast-path heuristics (length checks, regex, or keyword matching) before delegating decision-making to a model.

## 2025-05-15 - Async I/O in Python Pipes
**Learning:** Blocking `requests` calls in an asynchronous environment like Open WebUI Pipes can stall the entire event loop.
**Action:** Use `asyncio.to_thread` to offload blocking I/O to a thread pool when using synchronous libraries like `requests` in an async context.
