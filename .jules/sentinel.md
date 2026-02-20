## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure in AI Pipes
**Vulnerability:** Open WebUI Pipes (e.g., `n8n_pipe.py`) were returning detailed error messages (including `str(e)` and raw response bodies) directly to users. This could leak internal workflow details, stack traces, or server state.
**Learning:** Even internal AI orchestration layers must follow the "fail securely" principle. Synchronous libraries like `requests` also risk DoS of the event loop in async environments.
**Prevention:** Always sanitize error messages for users, log detailed exceptions to `sys.stderr`, and use `httpx.AsyncClient` with connection pooling in persistent AI pipes.
