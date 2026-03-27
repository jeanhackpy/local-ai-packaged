## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2026-02-14 - Hardcoded Secrets in Configuration Files
**Vulnerability:** Real Telegram bot tokens and gateway authentication tokens were found hardcoded in `openclaw/openclaw.json`, which was committed to the repository.
**Learning:** Configuration files like `openclaw.json` are often overlooked when scrubbing for secrets compared to `.env` files. If a project uses custom JSON/YAML configs for service initialization, these must be templated with placeholders before being committed.
**Prevention:** Use a pre-commit hook or automated scanner to detect patterns resembling API keys and tokens in all file types, not just `.env`. Ensure all configuration templates use generic placeholders and that real configurations are excluded via `.gitignore`.
