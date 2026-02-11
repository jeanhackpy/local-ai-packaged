## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.
## 2026-02-11 - [Information Leakage in n8n_pipe.py]
**Vulnerability:** Raw API error responses (including `response.text`) were being returned directly to the end-user.
**Learning:** Returning uncurated error messages from upstream APIs can leak sensitive internal state, authentication details, or system architecture information.
**Prevention:** Always log detailed error information to server logs/stdout and return only generic status messages or sanitized errors to the client.
