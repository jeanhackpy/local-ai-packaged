## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure in AI Pipe Error Handling
**Vulnerability:** AI pipes (`router_pipe.py`, `n8n_pipe.py`) were returning raw exception strings and non-200 response bodies directly to the frontend. This could leak internal API structures, service URLs, or authentication errors to end-users.
**Learning:** While catch-all exception blocks prevent application crashes, returning the error object or response text directly is a security risk. Errors must be sanitized for the user while the original detail is preserved in server-side logs.
**Prevention:** Always wrap external service calls in try-except blocks that log the full error internally and return a generic, user-friendly message. Ensure timeouts are explicitly set to prevent resource exhaustion from hanging external requests.
