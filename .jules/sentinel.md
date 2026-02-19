## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Hardcoded Secrets in Config Files
**Vulnerability:** `openclaw/openclaw.json` was committed to the repository containing a live Telegram bot token and a gateway authentication token.
**Learning:** Configuration files that require secrets should always be templated (e.g., `.example` files) and added to `.gitignore`. Relying on manual configuration after cloning is prone to accidental commits of sensitive data.
**Prevention:** Implement automated configuration generation in the startup script that injects secrets from a protected `.env` file into the actual configuration files. Use cryptographically secure random generators for tokens that aren't provided by the user.
