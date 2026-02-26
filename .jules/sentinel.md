## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2026-02-26 - Hardcoded Secrets in Configuration Files
**Vulnerability:** Critical secrets (Telegram Bot Token, Gateway Token) were hardcoded in `openclaw/openclaw.json` and tracked in Git.
**Learning:** Even if a project uses environment variables for most things, third-party configuration files can easily slip through and contain hardcoded secrets if not properly templatized and added to `.gitignore`.
**Prevention:** Use `.example` templates for all configuration files containing secrets. Implement an initialization script (like `start_services.py`) to inject environment variables into these templates at runtime, and ensure the final configuration files are ignored by Git.
