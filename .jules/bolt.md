## 2025-05-15 - [Concurrency in Async Python Pipes]
**Learning:** In Open WebUI Python pipes, the `pipe` method is asynchronous, but using synchronous libraries like `requests` will block the entire event loop, preventing concurrent request processing.
**Action:** Always offload blocking I/O (like `requests.post`) to a thread using `asyncio.to_thread` or use an asynchronous HTTP client like `httpx` (if available) to maintain system responsiveness.

## 2025-05-15 - [LLM Classification Latency]
**Learning:** When using an LLM for classification (e.g., Easy/Hard), the model may continue generating tokens after the answer. This adds unnecessary latency.
**Action:** Use `num_predict: 5` (or similar constraints) in the model options to stop generation early and reduce response time.
