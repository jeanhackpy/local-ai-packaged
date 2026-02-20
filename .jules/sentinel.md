## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Information Leakage in Open WebUI Pipes
**Vulnerability:** Open WebUI Pipes (n8n_pipe.py, router_pipe.py) were leaking raw exception strings and upstream API response bodies to the end-user via chat messages and status indicators.
**Learning:** Returning raw exception data in a user-facing application is a significant information disclosure risk. In an asynchronous environment, using synchronous libraries like 'requests' also risks blocking the entire system.
**Prevention:** Always catch exceptions in pipes and return generic, safe error messages to users. Log the full details to 'sys.stderr' for server-side debugging. Use 'httpx.AsyncClient' with explicit timeouts to ensure non-blocking and reliable network operations.
