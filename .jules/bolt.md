## 2025-02-11 - Optimized n8n Pipe with Connection Pooling and Non-blocking I/O
**Learning:** Open WebUI pipes (functions) that interact with external services via synchronous HTTP libraries like `requests` can block the main async event loop, leading to poor UI responsiveness and reduced throughput. Additionally, establishing a new TCP connection for every pipe execution adds significant latency.

**Action:** Always use `requests.Session()` within the `Pipe` class's `__init__` method to leverage connection pooling. Furthermore, wrap synchronous HTTP calls in `asyncio.to_thread()` when used inside `async` methods to offload blocking I/O to a thread pool, ensuring the main event loop remains free to handle other tasks and status emissions.
