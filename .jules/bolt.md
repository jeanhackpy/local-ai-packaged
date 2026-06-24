# Bolt's Performance Journal ⚡

## 2025-05-15 - LLM Router Optimization
**Learning:** For LLM-based routing systems, performing a model inference for every query is a significant latency bottleneck, especially for simple greetings or short commands. A simple string-length heuristic (< 15 chars) can bypass this overhead for a large percentage of user interactions without sacrificing routing accuracy for complex tasks. Additionally, using synchronous `requests` in an async Pipe blocks the event loop, which can degrade overall application responsiveness under load.

**Action:** Always implement a fast-path heuristic for trivial inputs in routing logic. Use `httpx.AsyncClient` with connection pooling for all network-bound operations in Open WebUI pipes to ensure non-blocking execution and reduced connection overhead.
