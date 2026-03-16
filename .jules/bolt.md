# Bolt's Performance Journal

## 2025-05-15 - LLM Router Latency Optimization
**Learning:** Evaluating every query's difficulty with a separate LLM call (even short ones like "Hi") adds significant fixed latency (~200-400ms) to every request. Offloading synchronous network calls (using `requests`) to a separate thread is essential for preventing event-loop congestion in Python-based pipes.

**Action:** Implement a fast-path heuristic for short queries (< 15 chars) and offload `requests.post` to `asyncio.to_thread`. Use `num_predict: 5` for evaluation calls to further reduce latency.
