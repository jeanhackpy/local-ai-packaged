## 2026-02-14 - Dependency Boundaries vs. Async Best Practices
**Learning:** In this environment, strict adherence to the 'No new dependencies' rule takes precedence over following async best practices (like using 'httpx' over 'requests' in 'async' functions).
**Action:** Always ask for permission before adding 'httpx' even if the existing code uses a blocking library in an 'async' context. Use 'requests.Session()' for connection pooling without new dependencies.
