## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-14 - Hardcoded Secrets in Config File
**Vulnerability:** Critical secrets (Telegram Bot Token and OpenClaw Gateway Token) were hardcoded and committed in `openclaw/openclaw.json`.
**Learning:** Hardcoding secrets in "default" config files is a common shortcut that leads to credential leakage if the file is tracked by Git. Even if intended for local use, these files often end up in version control.
**Prevention:** Use template files (e.g., `.example`) for configurations containing secrets. Add actual config files to `.gitignore` and implement an automated setup script that injects secrets from environment variables or secure sources into the local config at runtime.
