## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure and DoS in AI Pipes
**Vulnerability:** AI pipes (`n8n_pipe.py`, `router_pipe.py`) were leaking technical error details (backend responses, stack traces) to the end-user interface. Additionally, they used synchronous network calls that blocked the Python event loop, creating a DoS risk.
**Learning:** Returning `str(e)` directly to the user is a common pattern for "easy debugging" that creates significant security risks in production. In async environments like Open WebUI pipes, synchronous I/O can hang the entire service for all users.
**Prevention:** Always log technical details to `sys.stderr` and return generic, non-informative error messages to the client. Use `asyncio.to_thread` or an async HTTP client for all network operations in `async` methods.
