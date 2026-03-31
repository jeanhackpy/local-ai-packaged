## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Disclosure in AI Pipes
**Vulnerability:** Upstream API error details (like `response.text`) were being returned directly to the end-user in `n8n_pipe.py` and `router_pipe.py`. This could leak sensitive internal state, stack traces from backend services, or even API keys if present in the response body.
**Learning:** Open WebUI Pipes often act as proxies. When proxying requests, blindly returning the upstream error response to the client violates the "Fail Securely" principle.
**Prevention:** Always sanitize error messages returned to the user. Log the raw upstream response to `sys.stderr` for debugging, but provide only a generic, non-descriptive error message to the frontend.
