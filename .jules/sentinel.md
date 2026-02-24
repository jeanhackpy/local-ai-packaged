## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2026-02-16 - Hardcoded Secrets in Config Files
**Vulnerability:** Critical secrets (Telegram Bot Token and OpenClaw Gateway Token) were hardcoded and committed to the repository in `openclaw/openclaw.json`.
**Learning:** Even when a file is intended to be generated or modified by a startup script, it must be explicitly added to `.gitignore` and provided as a `.example` template to prevent accidental leakage of secrets during development or deployment.
**Prevention:** Never commit files containing secrets. Always use templates (`.example`) and environment variables (`.env`) for sensitive configuration. Add all generated configuration files to `.gitignore`.
