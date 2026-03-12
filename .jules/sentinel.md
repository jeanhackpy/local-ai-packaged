## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure in Open WebUI Pipes
**Vulnerability:** Detailed error messages, including stack traces and raw API response text (often containing internal URLs and status codes), were returned directly to the user interface in `n8n_pipe.py` and `router_pipe.py`.
**Learning:** Returning raw exceptions or response objects in a production environment leaks implementation details that can be used to map the internal network or exploit downstream services.
**Prevention:** Implement a standard error-handling pattern for all pipes: catch exceptions, log the technical details to `sys.stderr` for internal observability, and return a sanitized, generic error message to the client.
