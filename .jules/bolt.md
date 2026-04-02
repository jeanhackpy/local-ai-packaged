# Bolt's Performance Journal

## 2025-05-15 - Fast-path for short queries in router_pipe.py
**Learning:** Short queries (e.g., "Hi", "Thanks") don't need expensive LLM-based difficulty evaluation. Bypassing it saves significant latency.
**Action:** Implemented a `fast_path_threshold` in `router_pipe.py` to skip evaluation for queries under 15 characters.
