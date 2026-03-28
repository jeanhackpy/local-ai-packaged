## 2025-05-15 - Event Loop Congestion in Async Pipes
**Learning:** Open WebUI Pipes are asynchronous, but the `requests` library is synchronous and blocking. Using `requests.post` directly inside an `async def pipe` method blocks the entire server's event loop, causing concurrent requests to scale linearly in latency (5 requests take 5x the time of 1).
**Action:** Always offload synchronous network I/O to separate threads using `asyncio.to_thread` when working within the Open WebUI Pipe architecture to maintain system responsiveness and throughput.

## 2025-05-15 - Token Generation Overhead in Classification
**Learning:** Even for single-word responses like "Easy" or "Hard", LLMs may generate trailing whitespace or unnecessary tokens if not constrained. This adds measurable latency to the critical path of routing.
**Action:** Use the `num_predict` option (e.g., set to 5) in Ollama's API to cap token generation for classification tasks, significantly reducing the "time to last token".
