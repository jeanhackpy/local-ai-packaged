## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-14 - Hardcoded Secrets in openclaw.json
**Vulnerability:** CRITICAL - Telegram bot token and OpenClaw gateway token were hardcoded and tracked in git in `openclaw/openclaw.json`.
**Learning:** Configuration files that contain both static settings and secrets are often accidentally committed if not properly managed by a template/generation system.
**Prevention:** Use `.example` templates for configuration files containing secrets, add the final configuration file to `.gitignore`, and implement a secure merge/generation script (e.g., in `start_services.py`) to populate secrets from environment variables.
