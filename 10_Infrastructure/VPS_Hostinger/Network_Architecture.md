---
type: infrastructure_documentation
tags: [vps, network, caddy, kong, supabase, ports, ip]
updated: 2026-06-01
status: active
---

# 🏗️ VPS Network Architecture — Caddy + Kong + Supabase

> **Date** : 2026-06-01 | **VPS** : 31.97.67.145 (Tailscale 100.78.110.61) | **Docker Network** : `localai_default` (172.18.0.0/16)

---

## External Ports (0.0.0.0)

| Port | Service | Notes |
|:---|:---|:---|
| **22** | SSH | `ssh phil@31.97.67.145` |
| **80** | Caddy HTTP | ACME challenges, redirects to 443 |
| **443** | Caddy HTTPS | TLS termination (TCP + UDP) |
| **2019** | Caddy Admin API | local only |
| **5432** | supabase-pooler | PostgreSQL pooler (⚠️ exposé sans restriction) |
| **5678** | n8n | Aussi proxied via Caddy |
| **6333** | Qdrant | Vector DB REST (⚠️ sans auth) |
| **6334** | Qdrant | gRPC interface (⚠️ sans auth) |
| **7473** | Neo4j | HTTPS (⚠️ exposé) |
| **7474** | Neo4j Browser | aussi proxied via Caddy |
| **7687** | Neo4j Bolt | (⚠️ exposé) |
| **8000** | Kong HTTP | Supabase API gateway |
| **8081** | SearXNG | ⚠️ exposé sans auth (devrait être internal) |
| **8443** | Kong HTTPS | Supabase API gateway (TLS) |
| **8765** | Palanthai API | `nohup uvicorn` (PAS Docker, PAS systemd) — ⚠️ sans auth |
| **11434** | Ollama | ⚠️ exposé (devrait être internal) |
| **9119** | HERMES Dashboard | bindé sur `100.78.110.61` (Tailscale) uniquement |

---

## Network Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTERNET                                           │
│                                                                             │
│   Browser ──▶ https://n8n.recall-agency.com         (port 443)               │
│   Browser ──▶ https://supabase.recall-agency.com    (port 443)               │
│   Browser ──▶ https://neo4j.recall-agency.com       (port 443)               │
│   Browser ──▶ https://recall-agency.com             (port 443) ── WordPress  │
│   n8n/wf ──▶ https://n8n.recall-agency.com/webhook/...                      │
│   Browser ──▶ http://31.97.67.145:8765              (Palanthai API direct)  │
│   Tailscale ──▶ http://100.78.110.61:9119           (HERMES dashboard)      │
└─────────────────────────────────────────────────────────────────────────────┘
                                     │
                                     ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CADDY (172.18.0.x)  :80  :443  :2019                   │
│                     Reverse Proxy + ACME TLS                                │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  Route rules (Caddyfile, juin 2026):                                │   │
│   │                                                                       │   │
│   │  {$N8N_HOSTNAME}/*       ──────▶  n8n:5678                          │   │
│   │  {$SUPABASE_HOSTNAME}/*  ──────▶  kong:8000  (Supabase API)         │   │
│   │  {$NEO4J_HOSTNAME}/*     ──────▶  neo4j:7474  (✅ ACTIF)             │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                 │                           │                           │
                 │ (n8n subdomain)           │ (supabase subdomain)       │ (neo4j subdomain)
                 ▼                           ▼                           ▼
┌──────────────────────────┐  ┌───────────────────────────────────────────────┐
│  KONG (172.18.0.x)       │  │         OTHER INTERNAL SERVICES                │
│  Port 8000 / 8443        │  │                                                │
│  Supabase API Gateway     │  │  ┌──────────┐   ┌────────────┐  ┌──────────┐  │
│                          │  │  │  n8n     │   │  Qdrant    │  │  Valkey  │  │
│  Routes:                  │  │  │ :5678    │   │ :6333-34   │  │ :6379    │  │
│  /rest/v1/* ──────────▶ supabase-rest:3000    │ (direct)   │  │ (Redis)  │  │
│  /auth/v1/* ──────────▶ supabase-auth:9999   └────────────┘  └──────────┘  │
│  /storage/v1/* ────────▶ supabase-storage:5000                                │
│  /functions/v1/* ──────▶ supabase-edge-functions:9000                         │
│  /realtime/v1/* ──────▶ realtime:4000                                         │
│  /pg/* ───────────────▶ supabase-meta:8080                                    │
│  / ──────────────────▶ supabase-studio:3000  (basic-auth)                   │
│                          │                                                │
│  Auth: key-auth + CORS  │                                                │
│  Consumer: anon + admin │                                                │
└──────────────────────────┘                                                │
                 │                                                            │
                 ▼                                                            │
┌──────────────────────────────────────────────────────────────────────────────┐
│                    SUPABASE INTERNAL SERVICES                                │
│                                                                              │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────────────┐  │
│  │ supabase-rest    │  │ supabase-auth    │  │ supabase-edge-functions │  │
│  │ postgrest:v14.1  │  │ gotrue:v2.184.0  │  │ edge-runtime:v1.69.28   │  │
│  │ :3000            │  │ :9999            │  │ :9000                   │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────────┬─────────────┘  │
│           │                     │                        │                 │
│  ┌────────┴─────────┐  ┌────────┴─────────┐  ┌────────────┴─────────────┐  │
│  │ supabase-pooler  │  │ supabase-meta    │  │ supabase-storage        │  │
│  │ supavisor:2.7.4  │  │ postgres-meta    │  │ storage-api:v1.33.0     │  │
│  │ :5432 / :6543    │  │ v0.95.1 :8080    │  │ :5000                   │  │
│  │ (pool + tx)      │  │                  │  │                         │  │
│  └────────┬─────────┘  └──────────────────┘  └─────────────────────────┘  │
│           │                                                               │
│           ▼                                                               │
│  ┌──────────────────┐                                                     │
│  │  supabase-db     │                                                     │
│  │  postgres:15.8.1 │   145 tables public / 2.5 GB                        │
│  │  :5432 (Docker)  │                                                     │
│  └──────────────────┘                                                     │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │ realtime         │  │ supabase-imgproxy│  │ ollama ✅        │       │
│  │ realtime:v2.68.0 │  │ imgproxy:v3.8.0  │  │ ollama:latest    │       │
│  │ :4000            │  │ :8080            │  │ :11434 (10.6 GB) │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐                               │
│  │ neo4j ✅         │  │ searxng          │                               │
│  │ neo4j:latest     │  │ searxng:latest   │                               │
│  │ :7473 / :7474    │  │ :8080 (→ 8081)   │                               │
│  │ :7687 (bolt)     │  │                  │                               │
│  └──────────────────┘  └──────────────────┘                               │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                  PALANTHAI API (host network, port 8765)                   │
│                                                                             │
│  ┌─────────────────────┐     ┌─────────────────┐  ┌─────────────────────┐  │
│  │ Palanthai API       │     │ bulk_embed.log  │  │ wf_proto.py        │  │
│  │ nohup uvicorn       │     │ (crawl4ai log)  │  │ (FastAPI, port 8765│  │
│  │ port 8765           │     │ (348 KB)        │  │  49 routes)        │  │
│  │ PID 776             │     └─────────────────┘  └──────────┬──────────┘  │
│  │ version 1.0.0       │                                       │            │
│  └──────────┬──────────┘                                       │            │
│             │                                                  │            │
│             ▼                    ┌─────────────────┐           │            │
│  ┌─────────────────────────┐     │ Crawl4AI +      │           │            │
│  │  /scraper/run           │────▶│ Puppeteer Chrome │           │            │
│  │  /wf_proto/*           │     │ (headless)       │           │            │
│  │  /lockdown/sync/*      │     └─────────────────┘           │            │
│  │  /sync/* /units/*      │───────────────────────────────────┘            │
│  │  /seo/* /content/*     │                                                │
│  │  /queue/* /memory/*    │                                                │
│  │  /subjects             │                                                │
│  └───────────┬──────────────────────────────────────────────────────────────┘│
│              │                                                               │
│              ▼                                                               │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐         │
│  │  Supabase        │  │  Qdrant          │  │  Neo4j ✅        │         │
│  │  (Docker)        │  │  :6333           │  │  :7687 (bolt)    │         │
│  │  kong:8000       │  │  units 45 039    │  │  + :7474 browser │         │
│  │  pooler:5432     │  │  units_v3 200    │  │                  │         │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘         │
│                             │                                               │
│                             ▼                                               │
│                      ┌──────────────────┐                                  │
│                      │ n8n workflows     │   Appelle 8765 (correct)        │
│                      │ WF-006, 008, 010 │                                  │
│                      │ Local_RAG_AI_…    │                                  │
│                      └──────────────────┘                                  │
└────────────────────────────────────────────────────────────────────────────┘
```

---

## Kong Routes Detail

| External Path | Upstream Service | Internal Port | Auth |
|:---|:---|:---|:---|
| `/rest/v1/*` | supabase-rest | 3000 | key-auth (apikey) |
| `/auth/v1/*` | supabase-auth | 9999 | CORS (some open) |
| `/storage/v1/*` | supabase-storage | 5000 | Self-managed |
| `/functions/v1/*` | supabase-edge-functions | 9000 | CORS |
| `/realtime/v1/*` | supabase-realtime | 4000 | key-auth (ws) |
| `/pg/*` | supabase-meta | 8080 | key-auth |
| `/` | supabase-studio | 3000 | basic-auth |

---

## Docker Network — `localai_default`

| Service | IP (approx.) | Ports exposés |
|:---|:---|:---|
| supabase-imgproxy | 172.18.0.2 | 8080 |
| supabase-edge-functions | 172.18.0.3 | 9000 |
| supabase-studio | 172.18.0.4 | 3000 |
| **supabase-kong** | 172.18.0.5 | 8000/8443 |
| supabase-db | 172.18.0.6 | 5432 (interne) |
| realtime | 172.18.0.7 | 4000 |
| supabase-pooler | 172.18.0.8 | 5432/6543 |
| supabase-rest | 172.18.0.9 | 3000 |
| supabase-auth | 172.18.0.10 | 9999 |
| supabase-meta | 172.18.0.11 | 8080 |
| supabase-storage | 172.18.0.12 | 5000 |
| searxng | 172.18.0.13 | 8080 |
| **caddy** | 172.18.0.14 | 80/443 |
| n8n | 172.18.0.16 | 5678 |
| valkey/redis | 172.18.0.18 | 6379 |
| minio | 172.18.0.19 | 9000-9001 |
| qdrant | 172.18.0.21 | 6333-6334 |
| ollama | 172.18.0.x | 11434 |
| neo4j | 172.19.0.2 | 7473-7474, 7687 (réseau secondaire) |

> IPs indicatives — vérifier avec `docker network inspect localai_default`.

---

## ⚠️ Issues Found (au 2026-06-01)

### 1. ✅ RÉSOLU — n8n workflows appellent le bon port
Les workflows n8n pointent vers `http://172.18.0.1:8765` ou `http://31.97.67.145:8765` → Palanthai API répond bien sur 8765. **OK.**

### 2. ✅ RÉSOLU — Neo4j est actif
`neo4j.recall-agency.com` est exposé via Caddy et `neo4j:latest` tourne sur 7473/7474/7687. Conteneurs healthy.

### 3. ✅ RÉSOLU — Ollama tourne
`ollama/ollama:latest` répond sur :11434 (image 10.6 GB sur disque).

### 4. ⚠️ Qdrant exposé sans auth (port 6333/6334)
Qdrant REST + gRPC sont exposés sans auth. Considérer restriction localhost ou ajout auth.

### 5. ⚠️ supabase-pooler exposé sur 5432 (public)
PostgreSQL pooler est directement accessible sur port 5432. Renforcer passwords + IP allowlist.

### 6. ⚠️ Ollama et SearXNG exposés sur 11434/8081
Bien que désactivés côté Caddy, les ports host sont publiés et accessibles depuis Internet sans auth.

### 7. ⚠️ Neo4j Browser et Bolt exposés (7473/7474/7687)
Pas d'auth par défaut sur le container `neo4j:latest`. Activer `NEO4J_AUTH` (déjà dans `.env`).

### 8. ⚠️ Palanthai API (8765) sans auth
L'API v1.0.0 (49 routes) n'a pas d'auth visible — toute route peut être hitée.

### 9. ⚠️ Erreur runtime sur `/seo/sync-subjects`
`ModuleNotFoundError: No module named 'analytics'` — pipeline SEO cassé jusqu'à install de la dépendance.

---

## Key Files

| File | Purpose |
|---|---|
| `/home/phil/local-ai-packaged/Caddyfile` | Caddy reverse proxy config (3 routes actives) |
| `/home/kong/kong.yml` (in Kong container) | Kong declarative routing |
| `/home/phil/local-ai-packaged/.env` | 40 secrets + hostnames + API keys |
| `/home/phil/palanthai/start_api.sh` | nohup uvicorn launcher (port 8765) |
| `/home/phil/palanthai/palanthai_api.py` | FastAPI app (49 routes) |
| `/home/phil/palanthai/config/.env` | 20 clés ops (GA4, GSC, Neo4j, Qdrant, Ollama, WordPress) |

> Note: `/etc/systemd/system/palanthai-sync.service` existe mais est **disabled** — l'API ne démarre PAS via systemd. C'est `start_api.sh` (nohup) qui gère l'auto-restart via `--reload`.

---

*Dernière mise à jour : 2026-06-01 | Refresh sur base inspection live VPS*
*Voir : [[VPS_ACCESS_REFERENCE]], [[VPS_SERVICE_MAP]], [[VPS_INFRASTRUCTURE_REFERENCE]]*
