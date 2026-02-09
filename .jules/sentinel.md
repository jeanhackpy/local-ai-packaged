## 2026-02-09 - Inconsistent Port Exposure across Profiles
**Vulnerability:** The `openclaw-gateway` service was exposing port 18789 on all interfaces in the main `docker-compose.yml`, bypassing the security promise of the `--environment public` flag which intended to keep only ports 80 and 443 open.
**Learning:** Hardcoded port mappings in base Docker Compose files can leak internal management interfaces even when using override files meant to restrict access.
**Prevention:** Always use `expose` for internal service communication and only define `ports` in environment-specific override files, preferably bound to `127.0.0.1` unless explicitly intended for public exposure.
