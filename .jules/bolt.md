## 2025-05-15 - Optimizing Async LLM Pipes
**Learning:** In an asynchronous environment like Open WebUI, synchronous network calls (like `requests.post`) in a Pipe will block the entire event loop. This prevents the system from handling concurrent requests, effectively turning an async server into a sequential one.
**Action:** Always offload synchronous I/O to a thread using `asyncio.to_thread` and ensure all internal call sites use `await`.

## 2025-05-15 - LLM Classification Latency
**Learning:** For simple LLM-based classification tasks (e.g., "Easy" vs "Hard"), the model may generate unnecessary tokens, adding latency.
**Action:** Use `num_predict: 5` (or similar) in the Ollama options to force the model to stop after the initial classification word.

## 2025-05-15 - Fast-path Heuristics
**Learning:** LLM-based routing is expensive regardless of model size. Many queries (like greetings) are structurally simple.
**Action:** Implement simple character-count or keyword-based heuristics to bypass LLM evaluation for trivial inputs, significantly reducing latency for the most common interactions.
