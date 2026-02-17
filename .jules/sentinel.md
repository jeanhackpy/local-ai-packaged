## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-14 - Hardcoded Secrets in Configuration Templates
**Vulnerability:** `openclaw/openclaw.json` contained hardcoded Telegram Bot and Gateway tokens.
**Learning:** Committing active configuration files with real secrets is a common risk when transitioning from local development to a public repository.
**Prevention:** Always use template files (e.g., `.example`) for configurations containing secrets, add the real configuration files to `.gitignore`, and implement automated injection/generation of secrets during the environment setup process.
