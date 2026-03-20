## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2026-03-20 - Hardcoded Secrets in Tracked Configuration
**Vulnerability:** `openclaw/openclaw.json` was tracked in Git and contained a hardcoded Telegram Bot Token and Gateway Auth Token.
**Learning:** External tools often generate configuration files that contain secrets. If these files are not added to `.gitignore` immediately and replaced with templates, secrets will be leaked to the repository.
**Prevention:** Always use `.example` or `.template` files for configuration that requires secrets. Add the actual configuration file to `.gitignore` and implement a startup script that generates the configuration from the environment.
