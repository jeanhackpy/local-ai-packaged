# Bolt's Journal - Critical Learnings

## 2025-05-15 - Initial Journal Entry
**Learning:** The development environment is extremely sparse. It lacks standard Python libraries like `requests` and `pydantic` in the base environment, despite them being used in the codebase (`n8n_pipe.py`, `router_pipe.py`).
**Action:** Always verify the presence of dependencies before attempting to run tests or benchmarks. Use `pip install` only when absolutely necessary and allowed.
