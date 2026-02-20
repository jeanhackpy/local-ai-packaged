# Bolt Performance Journal

## 2025-02-20 - Latency Reduction with Fast-Path Heuristic in LLM Router
**Learning:** LLM-based decision making is powerful but adds significant latency (~100-500ms) even for trivial queries. Simple heuristics (like string length) can effectively bypass these calls for a large percentage of user interactions (greetings, simple commands).
**Action:** Always consider if a lightweight heuristic (regex, length, keyword check) can bypass an expensive LLM call for common edge cases.

## 2025-02-20 - Connection Pooling in Open WebUI Pipes
**Learning:** Re-instantiating HTTP clients for every pipe execution leads to TCP handshake overhead and potential socket exhaustion under load. Using a persistent `httpx.AsyncClient` in the `__init__` method of the `Pipe` class enables connection pooling, significantly improving throughput.
**Action:** In persistent Python classes like Open WebUI Pipes, initialize network clients in `__init__` rather than in the execution method.
