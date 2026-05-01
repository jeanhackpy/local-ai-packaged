---
type: infrastructure_documentation
tags: [vps, service-map, docker, ports, volumes, connection-strings, infrastructure, supabase, qdrant, neo4j, n8n]
updated: 2026-05-01
status: draft
---

# 🗺️ VPS Service Map — Complete Inventory

> Inventaire complet de tous les services, ports, volumes et connexions.
> Voir aussi : [[VPS_ARCHITECTURE_DIAGRAM]], [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_ACCESS_REFERENCE]]

---

## 1. Docker Stack Overview

**Location:** `/home/phil/local-ai-packaged/`
**Docker Compose:** `docker-compose.yml` + 3 override files

| Container | Image | Ports (Host) | Internal Port | Status | Purpose |
|---|---|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443 | 80, 443 | ✅ Running | Reverse proxy + TLS |
| n8n | ad20607cdd24 | 5678 | 5678 | ✅ Running | Workflow automation |
| qdrant | qdrant/qdrant | 6333, 6334 | 6333, 6334 | ✅ Running | Vector database |
| neo4j | neo4j:latest | 7474, 7687 | 7474, 7687 | ✅ Running | Graph database |
| minio | minio/minio | 9000, 9001 | 9000, 9001 | ✅ Running (healthy) | Object storage |
| valkey | valkey/valkey:8-alpine | 6379 | 6379 | ✅ Running (healthy) | Cache / Queue |
| searxng | searxng/searxng:latest | 8081 | 8081 | ✅ Running | Meta-search engine |
| supabase-kong | kong:2.8.1 | 8000, 8443 | 8000, 8443 | ✅ Running | API Gateway |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 | 5432 | ✅ Running | PostgreSQL database |
| supabase-auth | supabase/gotrue:v2.184.0 | — | 5432 | ✅ Running | Authentication |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 | 3000 | ✅ Running | REST API |
| supabase-studio | supabase/studio:2025.12.17 | 3000 | 3000 | ✅ Running | Dashboard |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 | 5000 | ✅ Running | File storage |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432 | 5432 | ✅ Running | Connection pooler |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | — | — | ✅ Running | Image proxy |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | — | ✅ Running | Edge functions |
| realtime | supabase/realtime:v2.68.0 | — | — | ✅ Running | Realtime subscriptions |
| ollama | ollama/ollama:latest | 11434 | 11434 | ⚠️ **Exited** | LLM local |
| open-webui | ghcr.io/open-webui/open-webui:main | — | — | ⚠️ **Exited** | Ollama WebUI |

---

## 2. Docker Internal Network

**Network:** `local-ai-packaged_local-ai` (bridge)
**Subnet:** 172.18.0.0/16 (approximate — verify with `docker network inspect`)

### Internal Hostnames (from Docker DNS)
```
n8n:5678
qdrant:6333
neo4j:7687
redis:6379 (valkey)
minio:9000
kong:8000
postgres:5432 (supabase-db)
```

### Connection Strings (Docker Internal)

| Service | Connection String | Notes |
|---|---|---|
| **Supabase REST** | `http://kong:8000` | Via Kong gateway |
| **Supabase DB** | `postgres://postgres:PORT@supabase-db:5432` | Check .env for password |
| **Supabase Auth** | Via Kong | Internal only |
| **Qdrant** | `http://qdrant:6333` | Vector store |
| **Neo4j** | `bolt://neo4j:7687` | Graph DB |
| **Valkey/Redis** | `redis://redis:6379` | Cache |
| **n8n** | `http://n8n:5678` | Workflow |
| **MinIO** | `http://minio:9000` | S3-compatible |
| **SearXNG** | `http://searxng:8081` | Search |
| **Ollama** | `http://ollama:11434` | ⚠️ Exited |

### n8n Workflow Environment Variables
```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434   # ⚠️ Ollama stopped
REDIS_HOST=redis:6379
NEO4J_URL=bolt://neo4j:7687
```

---

## 3. Docker Volumes

| Volume | Mount Point | Container | Purpose |
|---|---|---|---|
| `local-ai_caddy-data` | `/data` | caddy | TLS certs |
| `local-ai_qdrant-data` | `/qdrant/storage` | qdrant | Vector store |
| `supabase-db-data` | `/var/lib/postgresql/data` | supabase-db | PostgreSQL data |
| `supabase-db-config` | `/etc/postgresql` | supabase-db | Config |
| `supabase-kong-data` | `/usr/local/kong` | supabase-kong | Kong data |
| `n8n-data` | `/home/node/.n8n` | n8n | Workflows + data |
| `neo4j-data` | `/data` | neo4j | Graph data |
| `minio-data` | `/data` | minio | Object storage |
| `valkey-data` | `/data` | valkey | Redis-compatible |

**Volume locations (on host):**
```bash
docker volume inspect --format '{{.Mountpoint}}' local-ai_caddy-data
docker volume inspect --format '{{.Mountpoint}}' local-ai_qdrant-data
# PostgreSQL (Supabase)
docker volume inspect --format '{{.Mountpoint}}' supabase-db-data
# n8n
docker volume inspect --format '{{.Mountpoint}}' n8n-data
```

---

## 4. Bare Metal / Systemd Services

| Service | Type | Port | Access URL | Status | Notes |
|---|---|---|---|---|---|
| **Palanthai API** | systemd (uvicorn) | **8500** (HTTP) | `http://31.97.67.145:8500` | ✅ Running | `palanthai-sync.service` |
| **HERMES Agent** | Python venv | ? | ? | ✅ Running | PID 2126464 |
| **HERMES Dashboard** | Python venv | **9119** | `http://100.78.110.61:9119` | ✅ Running | PID 828746, bound to internal IP |
| **Next.js (temp-app)** | node | **3000** (public) | `http://31.97.67.145:3000` | ✅ Running | v16.0.10, phase5-mapping |
| **Next.js (dev)** | node | **5173** (localhost) | `http://localhost:5173` | ✅ Running | Only on localhost |
| **Syncthing** | binary | **8384** | `http://localhost:8384` | ✅ Running | sendonly → Mac |
| **MinIO (binary)** | binary | 9000, 9001 | `http://localhost:9000` | ✅ Running | PID 936942 |
| **Fail2ban** | systemd | — | — | ✅ Running | SSH protection |
| **Tailscale** | systemd | — | — | ✅ Running | VPN |

### Palanthai API Details
- **Service:** `palanthai-sync.service`
- **Binary:** `/home/phil/venv/bin/uvicorn` with `palanthai_api:app`
- **Config:** `/home/phil/palanthai/config/.env`
- **Log:** `/home/phil/palanthai/logs/api.log`
- **PID file:** `/home/phil/api.pid`
- **Version:** 2.0.0
- **Endpoints:** `/api/v1/source/projects`, `/api/v1/sync`, `/api/v1/sync/neo4j/*`
- **⚠️ Security:** Hardcoded PG password + command injection in `sync_service.py`

### HERMES Agent Details
- **Install:** `/home/phil/.hermes/` (Python venv, not Docker)
- **Processes:** PID 2126464 (main), PID 828746 (dashboard)
- **Dashboard:** Port 9119, bound to `100.78.110.61` (internal IP, not Caddy-proxied)
- **Replaces:** OpenClaw (npm packages still installed but unused)
- **Note:** npm packages `clawdock@0.3.2`, `clawhub@0.7.0` at `/home/phil/local-ai-packaged/node_modules/` — cleanup candidate

---

## 5. Exposed Ports Summary

### Internet-Accessible (VPS Firewall)
| Port | Service | URL | Auth |
|---|---|---|---|
| 22 | SSH | `ssh phil@31.97.67.145` | SSH key only |
| 80 | Caddy HTTP | `http://31.97.67.145` | — |
| 443 | Caddy HTTPS | `https://n8n.recall-agency.com` | TLS |
| 3000 | Next.js | `http://31.97.67.145:3000` | None (⚠️) |
| 5432 | PostgreSQL | Internal only | Password |
| 6333 | Qdrant | `http://31.97.67.145:6333` | None (⚠️) |
| 8500 | Palanthai API | `http://31.97.67.145:8500` | Unknown |
| 9119 | HERMES Dashboard | `http://100.78.110.61:9119` | Internal only |

### Shared Hosting (92.113.28.34)
| Port | Service | URL | Auth |
|---|---|---|---|
| 65002 | WordPress | `https://reflexion.asia` | LiteSpeed |
| 65002 | WordPress | `https://recall-agency.com` | LiteSpeed |
| 65002 | WordPress | `https://patrimonasia.com` | Not built |

---

## 6. Syncthing Configuration

**Config file:** `~/.config/syncthing/config.xml`

### Synced Folders (sendonly — VPS → Mac)

| VPS Folder | Mac Destination | Rescan Interval | Status |
|---|---|---|---|
| `/home/phil/palanthai` | TBC on Mac | 3600s (1h) | sendonly |
| `/home/phil/obsidian-leon` | TBC on Mac | 3600s (1h) | sendonly |

**Mode:** `sendonly` — changes on Mac are NOT synced back to VPS.
**Device:** Mac receives files read-only.

---

## 7. Caddy Proxy Routing

**File:** `/home/phil/local-ai-packaged/Caddyfile`

### ✅ Proxied (HTTPS via Caddy)
```
n8n.recall-agency.com → n8n:5678
supabase.recall-agency.com → kong:8000
```

### ❌ NOT Proxied
- **Palanthai API** (port 8500) — HTTP, no Caddy involvement
- **WordPress sites** — separate server (92.113.28.34), LiteSpeed direct
- **HERMES Dashboard** (port 9119) — bound to internal IP 100.78.110.61
- **Neo4j Browser** (port 7474) — commented out in Caddyfile
- **Ollama** (port 11434) — disabled, internal only
- **SearXNG** (port 8081) — disabled, internal only
- **Next.js** (port 3000) — directly accessible (no Caddy)

---

## 8. WordPress Sites (Shared Hosting)

**Server:** 92.113.28.34 (separate from VPS — LiteSpeed + PHP)

| Site | URL | Theme | SEO | Status |
|---|---|---|---|---|
| reflexion.asia | https://reflexion.asia | Houzez | RankMath | ✅ Production |
| recall-agency.com | https://recall-agency.com | Astra child | RankMath + Polylang | ✅ Production (FR/EN) |
| patrimonasia.com | https://patrimonasia.com | — | — | ❌ Not built |

**Cache:** LiteSpeed cache + LiteSpeed DOCREF active on recall-agency.com

---

## 9. Service Health Matrix

| Service | Container/Binary | Health | Startup | Auto-Restart |
|---|---|---|---|---|
| Caddy | Docker | ✅ | docker compose | Yes |
| n8n | Docker | ✅ | docker compose | Yes |
| Qdrant | Docker | ✅ | docker compose | Yes |
| Neo4j | Docker | ✅ | docker compose | Yes |
| Supabase (10) | Docker | ✅ | docker compose | Yes |
| MinIO | Docker | ✅ | docker compose | Yes |
| Valkey | Docker | ✅ | docker compose | Yes |
| SearXNG | Docker | ✅ | docker compose | Yes |
| Ollama | Docker | ⚠️ Exited | docker compose | No |
| OpenWebUI | Docker | ⚠️ Exited | docker compose | No |
| Palanthai API | systemd | ✅ | palanthai-sync.service | Yes |
| HERMES | Python venv | ✅ | ? | ? |
| HERMES Dashboard | Python venv | ✅ | ? | ? |
| Next.js | node | ✅ | ? | ? |
| Syncthing | binary | ✅ | ? | ? |
| MinIO (binary) | binary | ✅ | ? | ? |
| Fail2ban | systemd | ✅ | auto | Yes |
| Tailscale | systemd | ✅ | auto | Yes |

---

## 10. Palanthai Phase Pipeline — Service Mapping

```mermaid
flowchart TD
    subgraph P1["Phase 1 — Scraping (VPS /home/phil/palanthai)"]
        LP["LivePhuket.com"]
        SC["source_crawler.py"]
        WF["wf_extract/*.py"]
        FR["fullrun/fullrun.py"]
    end

    subgraph P2["Phase 2 — Extraction"]
        SEQ["sequencer_v2.py"]
        UE["unit_extractor_v2.py"]
        DB["db_ingestor_units.py"]
    end

    subgraph P3["Phase 3 — Embedding"]
        CL["data_cleaner.py"]
        EMB["embed_to_qdrant.py"]
        QD["Qdrant (:6333)"]
    end

    subgraph SERVICES["Services"]
        PG["PostgreSQL (:5432)"]
        NX["Next.js (:3000)"]
        HERMES["HERMES (:9119)"]
        N8N["n8n (:5678)"]
    end

    P1 -->|"JSONL batches"| P2
    P2 -->|"units"| PG
    P3 -->|"embeddings"| QD
    HERMES -.->|"Agent queries"| QD
    N8N -.->|"RAG queries"| HERMES
```

---

*Dernière mise à jour : 2026-05-01*
*Voir : [[VPS_ARCHITECTURE_DIAGRAM]], [[VPS_BACKUP_INFRASTRUCTURE]], [[VPS_INFRASTRUCTURE_REFERENCE]]*