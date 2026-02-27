## 2025-02-27 - Optimizing LLM Router Latency
**Learning:** For LLM-based routing/classification, every millisecond counts. Short queries (e.g., "Hi", "Hello") can be reliably routed using simple heuristics (length-based) without calling an LLM, saving 100% of evaluation latency. For queries that must be evaluated, using 'num_predict: 5' (or similar small value) significantly reduces inference time for single-word classifications by preventing the model from generating unnecessary tokens.

**Action:** Always implement a fast-path for trivial queries in routing logic. Use 'num_predict' for any classification task to minimize generation time.
