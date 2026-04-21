# 🏗️ VPS Network Architecture — Caddy + Kong + Supabase

> **Date**: 2026-04-21 | **VPS**: 31.97.67.145 | **Docker Network**: `localai_default` (172.18.0.0/16)

---

## External Ports (0.0.0.0)

| Port | Service | Notes |
|:---|:---|:---|
| **80** | Caddy HTTP | ACME challenges, redirects to 443 |
| **443** | Caddy HTTPS | TLS termination |
| **8000** | Kong HTTP | Supabase API gateway |
| **8443** | Kong HTTPS | Supabase API gateway (TLS) |
| **5432** | Supabase-pooler | PostgreSQL (pooler mode) |
| **5678** | n8n | Also proxied via Caddy |
| **6333** | Qdrant | Vector DB (REST API) |
| **6334** | Qdrant | gRPC interface |
| **8500** | Palanthai API | **uvicorn/systemd** (not Docker) |
| 8081 | SearXNG | Internal only |

---

## Network Map

```
┌─────────────────────────────────────────────────────────────────────────────┐
│                          INTERNET                                           │
│                                                                             │
│   Browser ──▶ https://n8n.recall-agency.com        (port 443)                │
│   Browser ──▶ https://supabase.recall-agency.com  (port 443)                │
│   Browser ──▶ https://recall-agency.com            (port 443) ── WordPress  │
│   n8n/wf ──▶ https://n8n.recall-agency.com/webhook/...                     │
└─────────────────────────────────────────────────────────────────────────────┘
                                    │
                                    ▼
┌─────────────────────────────────────────────────────────────────────────────┐
│                     CADDY (172.18.0.14)  :80  :443  :2019                  │
│                     Reverse Proxy + ACME TLS                               │
│                                                                             │
│   ┌─────────────────────────────────────────────────────────────────────┐   │
│   │  Route rules (Caddyfile):                                           │   │
│   │                                                                       │   │
│   │  n8n.recall-agency.com/*    ──────▶  n8n:5678                       │   │
│   │  supabase.recall-agency.com/* ──▶  kong:8000   (Supabase API)      │   │
│   │  neo4j.recall-agency.com/*     ───▶  neo4j:7474  (⚠️ INACTIVE)     │   │
│   │  /notebooks/*                  ───▶  /data/shared/notebooks          │   │
│   └─────────────────────────────────────────────────────────────────────┘   │
└─────────────────────────────────────────────────────────────────────────────┘
                │                           │                           │
                │ (n8n subdomain)           │ (supabase subdomain)       │
                ▼                           ▼                           ▼
┌──────────────────────────┐  ┌───────────────────────────────────────────────┐
│  KONG (172.18.0.5)       │  │         OTHER INTERNAL SERVICES                │
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
│  /analytics/v1/* ─────▶ analytics:4000                                        │
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
│  │ 172.18.0.9:3000  │  │ 172.18.0.10:9999 │  │ 172.18.0.3:9000        │  │
│  │ (PostgREST)      │  │ (GoTrue)         │  │ (Deno Edge)             │  │
│  └────────┬─────────┘  └────────┬─────────┘  └────────────┬─────────────┘  │
│           │                     │                        │                 │
│  ┌────────┴─────────┐  ┌────────┴─────────┐  ┌────────────┴─────────────┐  │
│  │ supabase-pooler  │  │ supabase-meta    │  │ supabase-storage        │  │
│  │ 172.18.0.8:5432  │  │ 172.18.0.11:8080 │  │ 172.18.0.12:5000       │  │
│  │ :6543 (transaction│  │ (pg-meta)        │  │ (S3-compatible)         │  │
│  │  mode)           │  │                  │  │                         │  │
│  └────────┬─────────┘  └──────────────────┘  └────────────────────────┘  │
│           │                                                               │
│           ▼                                                               │
│  ┌──────────────────┐                                                     │
│  │  supabase-db     │                                                     │
│  │  172.18.0.6:5432  │  (PostgreSQL 15)                                    │
│  │  (Docker volume) │                                                     │
│  └──────────────────┘                                                     │
│                                                                           │
│  ┌──────────────────┐  ┌──────────────────┐  ┌──────────────────┐       │
│  │ realtime         │  │ supabase-imgproxy│  │ supabase-meta    │       │
│  │ 172.18.0.7:4000  │  │ 172.18.0.2:8080  │  │ 172.18.0.11:8080 │       │
│  │ (Phoenix/Channels│  │                  │  │                  │       │
│  └──────────────────┘  └──────────────────┘  └──────────────────┘       │
└────────────────────────────────────────────────────────────────────────────┘

┌────────────────────────────────────────────────────────────────────────────┐
│                  PALANTHAI API (172.18.0.x via Docker bridge)              │
│                                                                             │
│  ┌─────────────────────┐     ┌─────────────────┐  ┌─────────────────────┐  │
│  │ Palanthai API       │     │ bulk_embed.log  │  │ sync_service.py    │  │
│  │ systemd/uvicorn     │     │ (crawl4ai log)  │  │ (FastAPI, port 8500│  │
│  │ port 8500           │     └─────────────────┘  └──────────┬──────────┘  │
│  │ PID 4530            │                                       │            │
│  └──────────┬──────────┘                                       │            │
│             │                                                  │            │
│             ▼                    ┌─────────────────┐           │            │
│  ┌─────────────────────────┐     │ Crawl4AI +      │           │            │
│  │  /api/v1/source/*       │────▶│ Puppeteer Chrome │           │            │
│  │  /api/v1/admin/*       │     │ (headless)       │           │            │
│  │  /api/v1/sync/neo4j/*  │     └─────────────────┘           │            │
│  │  /api/v1/export_embed  │───────────────────────────────────┘            │
│  └───────────┬──────────────────────────────────────────────────────────────┘│
│              │                                                               │
│              ▼                                                               │
│  ┌──────────────────┐  ┌──────────────────┐                                 │
│  │  Supabase        │  │  Qdrant          │   ⚠️ Ollama STOPPED             │
│  │  (Docker)        │  │  :6333           │   → Embedding via Kaggle/Colab  │
│  │  172.18.0.6/8    │  │  172.18.0.21     │                                 │
│  └──────────────────┘  └──────────────────┘                                 │
│                             │                                               │
│                             ▼                                               │
│                      ┌──────────────────┐                                  │
│                      │ n8n workflows     │   ⚠️ All call port 8765 (DEAD)   │
│                      │ WF-006, 008, 010 │   → Should be 8500               │
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
| `/analytics/v1/*` | analytics | 4000 | None |
| `/` | supabase-studio | 3000 | basic-auth |

---

## Docker Network — `localai_default`

| IP | Container | Ports |
|:---|:---|:---|
| 172.18.0.2 | supabase-imgproxy | 8080 |
| 172.18.0.3 | supabase-edge-functions | 9000 |
| 172.18.0.4 | supabase-studio | 3000 |
| **172.18.0.5** | **supabase-kong** | **8000/8443** |
| 172.18.0.6 | supabase-db | 5432 |
| 172.18.0.7 | realtime | 4000 |
| 172.18.0.8 | supabase-pooler | 5432/6543 |
| 172.18.0.9 | supabase-rest | 3000 |
| 172.18.0.10 | supabase-auth | 9999 |
| 172.18.0.11 | supabase-meta | 8080 |
| 172.18.0.12 | supabase-storage | 5000 |
| 172.18.0.13 | searxng | 8080 |
| **172.18.0.14** | **caddy** | **80/443** |
| 172.18.0.16 | n8n | 5678 |
| 172.18.0.18 | valkey/redis | 6379 |
| 172.18.0.19 | minio | 9000-9001 |
| 172.18.0.21 | qdrant | 6333-34 |
| 172.19.0.2 | neo4j | 7473-7474, 7687 |

---

## ⚠️ Issues Found

### 1. n8n workflows call dead port 8765
All Palanthai n8n workflows point to `http://172.18.0.1:8765` but Palanthai API is on **8500**. See: [[n8n Agent]]

### 2. Neo4j INACTIVE
`neo4j.recall-agency.com` routes to `neo4j:7474` in Caddy but container is not running.

### 3. Ollama STOPPED
Ollama Docker container is stopped — no local LLM inference available.

### 4. Qdrant directly exposed (port 6333)
Qdrant REST API is exposed on port 6333 without authentication. Consider restricting to localhost or adding authentication.

### 5. Supabase-pooler on 5432 (external)
PostgreSQL pooler is directly accessible on port 5432. Ensure strong passwords and IP allowlisting.

---

## Key Files

| File | Purpose |
|:---|:---|
| `/home/phil/local-ai-packaged/Caddyfile` | Caddy reverse proxy config |
| `/home/kong/kong.yml` (in Kong container) | Kong declarative routing |
| `/home/phil/local-ai-packaged/.env` | Hostnames + API keys |
| `/etc/systemd/system/palanthai-sync.service` | Palanthai systemd unit |
