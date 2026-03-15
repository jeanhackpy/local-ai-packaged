# Bolt's Performance Journal

## 2025-05-22 - [Optimizing AI Pipes with Async I/O and Fast-Path]
**Learning:** In asynchronous Python environments like Open WebUI, synchronous blocking calls (e.g., `requests.post`) stall the entire event loop, effectively making the application sequential regardless of concurrency. Offloading these to threads via `asyncio.to_thread` is essential. Additionally, for classification tasks like routing, capping `num_predict` in LLM options and implementing simple character-length heuristics (Fast-Path) can reduce latency by over 50% for common queries.
**Action:** Always check for synchronous network calls in `async` methods and offload them. Use `num_predict` for classification tasks. Implement heuristics to skip heavy processing for trivial inputs.
