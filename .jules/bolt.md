## 2025-05-14 - Fast-path heuristic and non-blocking I/O in LLM Router
**Learning:** In Open WebUI pipes, synchronous 'requests' calls block the event loop, causing performance degradation. Implementing a fast-path heuristic for short queries (e.g., < 15 characters) avoids unnecessary LLM-based difficulty evaluations.
**Action:** Always use 'asyncio.to_thread' for synchronous I/O in async pipes and implement fast-path checks for simple operations to reduce latency.
