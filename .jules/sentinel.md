## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Hardcoded Secrets in Tracked Configuration Files
**Vulnerability:** The `openclaw/openclaw.json` configuration file was tracked in version control and contained a live Telegram bot token and a gateway authentication token.
**Learning:** Hardcoding secrets in configuration files that are checked into Git is a common but critical security risk. Even if the file is intended for local use, its inclusion in the repository exposes sensitive credentials to anyone with access to the source code.
**Prevention:** Use configuration templates (e.g., `openclaw.json.example`) with placeholders and ensure the actual configuration file is ignored via `.gitignore`. Implement dynamic configuration generation in the application's startup or initialization scripts to inject secrets from environment variables or secure stores at runtime.
