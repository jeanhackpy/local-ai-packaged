## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Hardcoded Secrets in Config Templates
**Vulnerability:** The `openclaw/openclaw.json` file contained hardcoded Telegram bot tokens and gateway authentication tokens, which were committed to version control.
**Learning:** Even if a file is intended to be a "default" config, it often becomes the base for production. Any sensitive placeholder that looks like a real token (even if deactivated) can be a security risk and leaks developer habits/environment details.
**Prevention:** Always use template files (e.g., `.example`) with generic placeholders for secrets and implement a secure injection mechanism (like environment variables) in the startup or orchestration script. Ensure the actual config file is added to `.gitignore`.
