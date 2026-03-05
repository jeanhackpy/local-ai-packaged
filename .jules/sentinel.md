## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure and DoS in Python Pipes
**Vulnerability:** Open WebUI Pipes (router_pipe.py, n8n_pipe.py) leaked internal error details (e.g., full response bodies via `response.text`) to end-users and lacked network timeouts, creating risks for sensitive data exposure and Denial-of-Service.
**Learning:** Returning `Exception(str(e))` or raw API responses to the frontend is dangerous as they often contain environment details or stack traces. Additionally, synchronous `requests` calls in an `async` pipe block the entire event loop.
**Prevention:** Always wrap synchronous IO in `asyncio.to_thread`. Implement explicit timeouts for all network requests. Return generic, safe error messages to users while logging details to `sys.stderr`.
