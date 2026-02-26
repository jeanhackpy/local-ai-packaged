## 2025-05-15 - Optimizing LLM Router with Fast-Path Heuristic and Non-blocking I/O
**Learning:** For LLM classification tasks (like routing or difficulty evaluation), limiting token generation with `num_predict` significantly reduces latency without sacrificing accuracy if the response is just a single word. Also, always ensure `async` functions don't perform blocking synchronous I/O; use `asyncio.to_thread` with `requests` if `httpx` is not available.
**Action:** Use a short query heuristic to bypass LLM calls for trivial inputs and always limit generation tokens for classification tasks.
