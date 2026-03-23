## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2026-03-23 - Information Disclosure via AI Pipe Exceptions
**Vulnerability:** Technical exception details (stack traces, status codes, raw error messages) were being returned directly to the user interface in `n8n_pipe.py` and `router_pipe.py` when an external API call failed.
**Learning:** Returning raw exception messages to the UI can disclose internal system architecture, library versions, and sensitive configuration details to potential attackers.
**Prevention:** Always catch exceptions at the edge of external integrations, log technical details to secure logs (`sys.stderr`), and return generic, non-informative error messages to the user.
