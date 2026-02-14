# Bolt's Performance Journal ⚡

## 2025-05-14 - Async Pipe Optimization
**Learning:** Python-based Open WebUI Pipes run in an asynchronous environment (FastAPI/Starlette). Using synchronous `requests` blocks the entire event loop, preventing concurrent message handling. Switching to `httpx.AsyncClient` with connection pooling significantly improves throughput and responsiveness.

**Learning:** LLM-based decision making (like routing difficulty) has a non-trivial overhead even for tiny models (e.g., Granite-350m). A simple heuristic "fast path" for trivial queries (greetings, confirmations) saves a full network roundtrip and LLM inference cycle, reducing latency for common interactions by 100-500ms.

**Action:** Always prefer `httpx.AsyncClient` in Open WebUI Pipes. Implement fast-path heuristics for logic that depends on LLM evaluation of simple user input.
