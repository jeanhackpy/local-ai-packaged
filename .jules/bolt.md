## 2025-05-22 - Optimized LLM Router Pipe Performance
**Learning:** Evaluated query difficulty by calling a local LLM for every request adds significant latency (~200ms) and blocks the event loop when using synchronous libraries like `requests`.
**Action:** Implement a fast-path heuristic for trivial queries (e.g., < 15 chars) to bypass the LLM and offload all blocking network calls to background threads using `asyncio.to_thread`. Use `num_predict` to minimize classification latency.
