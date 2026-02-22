## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-15 - Hardcoded Secrets in OpenClaw Configuration
**Vulnerability:** The `openclaw/openclaw.json` configuration file contained hardcoded Telegram bot tokens and gateway authentication tokens, and was being tracked by Git.
**Learning:** Initial setup scripts or "onboarding" wizards often generate configuration files that are easily overlooked during security reviews. If these files are not explicitly ignored, they can leak credentials to the repository.
**Prevention:** Always use template files (e.g., `.example`, `.template`) for configurations containing secrets. Implement a robust orchestration script that populates these templates from environment variables at runtime and ensures the actual config files are in `.gitignore`.
