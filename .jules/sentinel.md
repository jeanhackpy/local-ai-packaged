## 2025-05-14 - Incorrect Security Overrides for AI Stack
**Vulnerability:** Services in the AI stack were not correctly shielded in "public" mode because `docker-compose.override.public.yml` only contained resets for Supabase services, which were not present in the AI stack's `docker-compose.yml`. This left services like `openclaw-gateway` exposed even when the user selected the "public" environment.
**Learning:** In a multi-stack Docker Compose setup, it's easy to copy-paste override files. If an override file is applied to a stack that doesn't contain the specified services, the `!reset null` directives do nothing, leading to a false sense of security.
**Prevention:** Always verify that environment-specific overrides correctly target the services defined in the specific base compose file they are intended for. Use `docker compose config` with the specific files to verify the final effective configuration.

## 2025-05-18 - Hardcoded Secrets in Tracked Configuration Files
**Vulnerability:** A Telegram Bot Token and an Auth Token were found hardcoded in `openclaw/openclaw.json`, which was a tracked file in the git repository. This exposes sensitive credentials to anyone with access to the source code.
**Learning:** Development-time configuration files often get committed by mistake if they are not explicitly added to `.gitignore` from the start. Even "dummy" tokens can lead to poor security hygiene or accidental leaks of real production keys.
**Prevention:** Use `.example` files as templates for configuration. Ensure all files containing secrets (like `.env` or `config.json`) are added to `.gitignore` before the first commit. For existing leaks, remove the file from git tracking using `git rm --cached` and sanitize the content.
