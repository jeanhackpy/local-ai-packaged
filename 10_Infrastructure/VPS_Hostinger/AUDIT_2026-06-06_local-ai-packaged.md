# Repository Audit — `local-ai-packaged` (Palanthai stack)

**Date:** 2026-06-06 · **Scope:** secrets hygiene, Docker/networking, Python & shell scripts, config governance · **Reviewer:** Senior AI Architect pass
> (Doc d'infra — centralisée dans 10_Infrastructure, pas dans le repo public.)

---

## Executive Summary

The repo is clean on the basics: no secrets in the tree or git history, sane `.gitignore`, real reverse-proxy hardening in the base compose. The risk concentrates in one place: the `private` environment override binds 11 service ports to `0.0.0.0`, several (Neo4j, Redis, Qdrant, Ollama) with weak/no auth — dangerous the moment this runs on a public VPS.

A few correctness bugs (dead `searxng` patch, `UnboundLocalError` in `n8n_pipe.py`, hardcoded path in `config-guard.sh`) and reproducibility gaps (`:latest` everywhere) round out the findings.

---

## Findings by Severity

### 🔴 HIGH

**H1 — `private` override exposes unauthenticated services to `0.0.0.0`.** `override.private.yml` publishes host ports for n8n (5678), Qdrant (6333/6334), Neo4j (7474/7687), Redis (6379), SearXNG (8081), Ollama (11434). Docker `ports:` binds all interfaces and bypasses UFW. On a public VPS = remote DB access + open LLM endpoint. The name "private" is misleading — it's the most exposed profile. *Fix:* bind loopback/Tailscale; only n8n/Supabase/Neo4j-browser public, via Caddy. **→ On Oracle, always `--environment public`.**

**H2 — Neo4j APOC unrestricted + strict validation disabled.** `neo4j.conf` sets `dbms.security.procedures.unrestricted=apoc.*` + `strict_validation.enabled=false`. With H1's exposed bolt port + weak default password = host read/write path. *Fix:* scope APOC, keep bolt off public, strong `NEO4J_AUTH`.

### 🟠 MEDIUM

**M1 — `public` override is a no-op for the AI stack (known, unfixed).** `override.public.yml` only `!reset`s kong/supavisor (Supabase services), absent from the AI compose. AI services are internal only because base compose uses `expose:` — by accident, not design. `config-guard` then "protects" the misleading file.

**M2 — Hardcoded personal Telegram chat ID as default** in `docker-compose.yml` (`TELEGRAM_CHAT_ID:-471505542`).

**M3 — `:latest` tags throughout** (n8n, neo4j, ollama, qdrant, minio, caddy, searxng) — defeats the golden-config reproducibility goal.

**M4 — Supabase `FUNCTIONS_VERIFY_JWT=false`** — edge functions unauthenticated by default.

### 🟡 LOW / Correctness

- **L1 — `n8n_pipe.py` `UnboundLocalError`:** `return n8n_response` reachable when `messages` is empty.
- **L2 — Dead SearXNG patch in `start_services.py`:** `content.replace("cap_drop: - ALL", …)` never matches the multi-line YAML.
- **L3 — `config-guard.sh` hardcoded `BASE="/home/phil/local-ai-packaged"`** — breaks on other paths.
- **L4 — Missing request timeouts** in `router_pipe.py` (`call_ollama`/`call_openrouter`).
- **L5 — SearXNG `limiter: false`** — acceptable only while internal.
- **L6 — Repo hygiene:** stale `bolt-*` remote branches, large commented-out blocks, no CI.

---

## Notes

- **Network model is the core issue.** Rule: nothing published except via Caddy; everything else over the bridge. Removes the firewall-bypass class entirely.
- **Secrets are env-driven and uncommitted** — good. Next: Docker secrets/vault for `POSTGRES_PASSWORD`, `NEO4J_AUTH`, `N8N_ENCRYPTION_KEY`.
- **Reproducibility:** pin images + CI `docker compose config` per profile to catch override regressions (M1).

## Priority order

1. H1/H2 — rewrite `override.private.yml` loopback-only; strong `NEO4J_AUTH`; scope APOC.
2. M2 — drop hardcoded Telegram default.
3. L1/L2 — fix the `n8n_pipe` crash; delete dead SearXNG patch.
4. M3 — pin image versions.
5. L3 — de-hardcode `config-guard.sh` base path.
6. M1/L6 — remove misleading public override; minimal CI.
