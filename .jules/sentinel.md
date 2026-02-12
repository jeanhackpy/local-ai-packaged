## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Persistent Service Name Mismatch in Overrides
**Vulnerability:** The 'openclaw' service was incorrectly referred to as 'openclaw-gateway' in both private and public Docker Compose overrides. This meant security configurations (like binding to 127.0.0.1 or resetting ports) failed to apply, leaving the service exposed on 0.0.0.0.
**Learning:** Even after a vulnerability is "fixed" (as noted in previous journal entries), mismatches can persist if renaming is not applied consistently across all compose files. Infrastructure-as-code requires exact string matching for overrides to function.
**Prevention:** Use 'docker compose config' to verify the final merged configuration and ensure all intended overrides (especially '!reset null') are actually reflected in the output for the target services.
