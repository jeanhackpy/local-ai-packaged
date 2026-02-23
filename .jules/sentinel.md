## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure and Resource Management in Pipes
**Vulnerability:** Open WebUI pipes were leaking sensitive API response details (like `response.text`) in error messages and used blocking `requests` calls within an `async` context.
**Learning:** Direct exposure of exceptions and raw response text to the UI can leak credentials or internal architecture. Additionally, mixing blocking I/O in async loops can lead to performance degradation.
**Prevention:** Use `httpx.AsyncClient` with proper lifecycle management (context managers) to perform non-blocking I/O safely. Always sanitize error messages for the frontend while logging detailed diagnostics to `sys.stderr`.
