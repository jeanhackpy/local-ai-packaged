## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Hardcoded Secrets in Tracked Configuration Files
**Vulnerability:** The `openclaw/openclaw.json` configuration file contained a hardcoded Telegram bot token and an API gateway token, and was tracked by Git, exposing these secrets to anyone with access to the repository.
**Learning:** Even if a file is intended to be local-only, it must be explicitly ignored in `.gitignore` and provided as a template (`.example`) to prevent accidental disclosure. Relying on users to "not commit it" is insufficient.
**Prevention:** Use a template-based configuration system where secrets are injected from a `.env` file at runtime. Automate the generation and persistence of internal tokens (like gateway tokens) to ensure security by default while maintaining service continuity.
