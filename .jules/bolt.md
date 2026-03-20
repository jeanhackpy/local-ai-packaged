## 2025-05-14 - [Offloading blocking I/O and Repository Hygiene]
**Learning:** Synchronous network calls like `requests.post` block the entire event loop in Python async applications, leading to sequential execution of concurrent requests. Additionally, committing `__pycache__` directories is a major repository hygiene violation and blocker for PR approval.
**Action:** Always wrap synchronous I/O in `asyncio.to_thread` when using async frameworks. Ensure `.gitignore` properly excludes Python binary artifacts and never use `git add .` to avoid staging unintended files.
