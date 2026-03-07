## 2025-05-15 - LLM Router Fast-Path Heuristic
**Learning:** Evaluating short, conversational queries (e.g., "Hi", "Thanks") with an LLM for difficulty is a major source of unnecessary latency. A simple length-based heuristic can skip this step entirely for a ~50% reduction in total request time for these queries.
**Action:** Always consider fast-paths for common, simple inputs in routing or classification tasks.
