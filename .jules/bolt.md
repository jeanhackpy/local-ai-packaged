## 2025-05-15 - [Concurrency in Python AI Pipes]
**Learning:** Synchronous `requests.post` calls in `async` methods block the entire Python event loop, causing concurrent requests to be processed sequentially. This significantly increases total execution time when multiple users or processes call the same pipe simultaneously.
**Action:** Use `asyncio.to_thread` to offload synchronous `requests` calls to a separate thread, allowing the event loop to handle other concurrent requests. Ensure all internal call sites (like `evaluate_difficulty`) are updated with `await` if they are converted to `async def`.

## 2025-05-15 - [Git Hygiene and Binary Artifacts]
**Learning:** Python automatically generates `__pycache__` directories and `.pyc` files when compiling or running scripts. These binary artifacts should never be committed to the repository as they bloat the history and can cause environment-specific issues.
**Action:** Explicitly include `__pycache__/`, `*.py[cod]`, and `*$py.class` in the root `.gitignore` file and ensure all such artifacts are removed (e.g., using `find . -name "__pycache__" -type d -exec rm -rf {} +`) before staging changes.
