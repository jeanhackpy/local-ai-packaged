## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Leakage in AI Agent Pipes
**Vulnerability:** The `n8n_pipe.py` script was leaking internal backend details by including `response.text` and raw exception strings in error messages sent to the frontend.
**Learning:** Returning detailed error messages to the UI can expose sensitive information about the backend infrastructure and external API responses.
**Prevention:** Always use generic error messages for the frontend and log detailed errors internally. Ensure all variables used in response paths are properly initialized to avoid secondary errors (like `UnboundLocalError`) during error handling.
