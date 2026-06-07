---
type: infrastructure_documentation
tags: [vps, service-map, docker, ports, volumes, connection-strings, infrastructure, supabase, qdrant, neo4j, n8n]
updated: 2026-06-01
status: active
---

# 🗺️ VPS Service Map — Complete Inventory

> Inventaire complet de tous les services, ports, volumes et connexions (au 2026-06-01).
> Voir aussi : [[VPS_ARCHITECTURE_DIAGRAM]], [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_ACCESS_REFERENCE]]

---

## 1. Docker Stack Overview

**Location :** `/home/phil/local-ai-packaged/`
**Docker Compose :** `docker-compose.yml` + 3 override files (public, private, public.supabase)
**Network :** `localai_default` (172.18.0.0/16)
**Total containers :** 19 — tous `Up 25 hours` (au 2026-06-01)

| Container | Image | Ports (Host) | Status | Purpose |
|---|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443, 443/udp, 2019 | ✅ Running | Reverse proxy + TLS |
| n8n | n8nio/n8n:latest | 5678 | ✅ Running | Workflow automation |
| qdrant | qdrant/qdrant:latest | 6333, 6334 | ✅ Running | Vector database |
| neo4j | neo4j:latest | 7473, 7474, 7687 | ✅ Running | Graph database |
| minio | minio/minio:latest | 9000, 9001 (interne) | ✅ Running (healthy) | Object storage |
| valkey | valkey/valkey:8-alpine | 6379 | ✅ Running (healthy) | Cache / Queue |
| searxng | searxng/searxng:latest | 8081→8080 | ✅ Running | Meta-search engine |
| supabase-kong | kong:2.8.1 | 8000, 8443 | ✅ Running (healthy) | API Gateway |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 (interne) | ✅ Running (healthy) | PostgreSQL database |
| supabase-auth | supabase/gotrue:v2.184.0 | — | ✅ Running (healthy) | Authentication |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 (interne) | ✅ Running | REST API |
| supabase-studio | supabase/studio:2025.12.17-sha-43f4f7f | 3000 (interne) | ✅ Running (healthy) | Dashboard |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 (interne) | ✅ Running (healthy) | File storage |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432, 6543 | ✅ Running (healthy) | Connection pooler |
| supabase-meta | supabase/postgres-meta:v0.95.1 | 8080 (interne) | ✅ Running (healthy) | pg-meta |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | 8080 (interne) | ✅ Running (healthy) | Image proxy |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | ✅ Running | Edge functions |
| realtime | supabase/realtime:v2.68.0 | — | ✅ Running (healthy) | Realtime subscriptions |
| ollama | ollama/ollama:latest | 11434 | ✅ Running | LLM local (10.6 GB image) |

> ❌ **open-webui** n'est plus dans la stack. Container retiré (le volume `local-ai-packaged_open-webui` existe comme résidu).

---

## 2. Docker Internal Network

**Network :** `localai_default` (bridge, 172.18.0.0/16)
**Subnets supplémentaires :** 172.19.0.0/16 (auto)

### Internal Hostnames (from Docker DNS)
```
n8n:5678
qdrant:6333
neo4j:7687                       (bolt) + 7474 (browser)
redis:6379                       (valkey)
minio:9000
kong:8000                        (Supabase gateway)
postgres / supabase-db:5432
ollama:11434
searxng:8080                     (container port — exposé sur 8081 côté host)
```

### Connection Strings (Docker Internal)

| Service | Connection String | Notes |
|---|---|---|
| **Supabase REST** | `http://kong:8000` | Via Kong gateway |
| **Supabase DB** | `postgres://postgres:PORT@supabase-db:5432` | password dans `.env` |
| **Supabase Auth** | Via Kong | Internal only |
| **Qdrant** | `http://qdrant:6333` | Vector store |
| **Neo4j** | `bolt://neo4j:7687` | Graph DB |
| **Valkey/Redis** | `redis://redis:6379` | Cache |
| **n8n** | `http://n8n:5678` | Workflow |
| **MinIO** | `http://minio:9000` | S3-compatible |
| **SearXNG** | `http://searxng:8080` | ⚠️ container port 8080 (host 8081) |
| **Ollama** | `http://ollama:11434` | ✅ réactivé |

### n8n Workflow Environment Variables
```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434      # ✅ réactivé
REDIS_HOST=redis:6379
NEO4J_URL=bolt://neo4j:7687          # ✅ réactivé
```

---

## 3. Docker Volumes

| Volume | Mount Point | Container | Purpose |
|---|---|---|---|
| `local-ai-packaged_caddy-data` | `/data` | caddy | TLS certs + config |
| `local-ai-packaged_caddy-config` | `/config` | caddy | Caddy config |
| `local-ai-packaged_qdrant_storage` | `/qdrant/storage` | qdrant | Vector store |
| `local-ai-packaged_db-config` | `/etc/postgresql` | supabase-db | Config |
| `local-ai-packaged_n8n_storage` | `/home/node/.n8n` | n8n | Workflows + data |
| `local-ai-packaged_minio_storage` | `/data` | minio | Object storage |
| `local-ai-packaged_valkey-data` | `/data` | valkey | Redis-compatible |
| `local-ai-packaged_open-webui` | — | (orphan) | Résidu — peut être nettoyé |
| `localai_*` (legacy) | — | — | Volumes orphelins d'une ancienne stack (cleanup candidate) |
| `535fc1c1a86f…` (anonymous) | — | — | Anonymous volume orphelin |

> ⚠️ Volumes Neo4j et supabase-db-data n'apparaissent pas dans la liste `docker volume ls` — vérifier s'ils sont bind-mountés depuis le host ou créés en named volumes par les overrides.

**Inspection depuis le host :**
```bash
docker volume inspect --format '{{.Mountpoint}}' local-ai-packaged_caddy-data
docker volume inspect --format '{{.Mountpoint}}' local-ai-packaged_qdrant_storage
```

---

## 4. Bare Metal / Systemd Services

| Service | Type | Port | Access URL | Status | Notes |
|---|---|---|---|---|---|
| **Palanthai API** | `nohup uvicorn` (start_api.sh) | **8765** (HTTP) | `http://31.97.67.145:8765` | ✅ Running (PID 776) | `--reload` activé ; systemd `palanthai-sync.service` est `disabled` |
| **HERMES Dashboard** | Python venv | **9119** | `http://100.78.110.61:9119` | ✅ Running (PID 968) | Bindé sur IP interne Tailscale uniquement |
| **HERMES Agent** | Python venv | — | — | ✅ Running | `/home/phil/.hermes/` |
| **Fail2ban** | systemd | — | — | ✅ active | SSH brute-force protection |
| **Tailscale** | systemd | — | — | ✅ active | VPN mesh (IP 100.78.110.61) |
| **Syncthing** | systemd | 8384 | `http://localhost:8384` | ❌ **inactive** | sendonly → Mac, service non démarré |

### Palanthai API Details
- **Binaire :** `python3 -m uvicorn palanthai_api:app --host 0.0.0.0 --port 8765 --reload`
- **Version :** **1.0.0** (Title: `Palanthai Local API`, 49 routes)
- **Venv :** `/home/phil/venv/` (Python 3.12)
- **Config :** `/home/phil/palanthai/config/.env` (20 clés)
- **Logs :** `/home/phil/palanthai/api.log` (PAS `palanthai/logs/api.log`)
- **PID file :** `/home/phil/palanthai/api.pid` (PAS `/home/phil/api.pid`)
- **Endpoints :** 49 routes — voir [[VPS_ACCESS_REFERENCE#🚀-Services-Bare-Metal-hors-Docker]]
- **⚠️ Security :** Hardcoded PG password + command injection in `sync_service.py` (cf. security audit)
- **⚠️ Runtime error :** `ModuleNotFoundError: No module named 'analytics'` au hit de `/seo/sync-subjects`

### HERMES Agent Details
- **Install :** `/home/phil/.hermes/` (Python venv, pas Docker)
- **Dashboard port :** 9119, bindé sur `100.78.110.61` (Tailscale)
- **Replaces :** OpenClaw

---

## 5. Exposed Ports Summary

### Internet-Accessible (VPS Firewall)
| Port | Service | URL | Auth |
|---|---|---|---|
| 22 | SSH | `ssh phil@31.97.67.145` | SSH key only |
| 80 | Caddy HTTP | `http://31.97.67.145` | redirige vers 443 |
| 443 | Caddy HTTPS | `https://*.recall-agency.com` | TLS (Let's Encrypt) |
| 5432 | PostgreSQL (pooler) | `psql` direct | ⚠️ exposed sans restriction IP |
| 5678 | n8n | `http://31.97.67.145:5678` | bypass Caddy possible |
| 6333 | Qdrant REST | `http://31.97.67.145:6333` | ⚠️ sans auth |
| 6334 | Qdrant gRPC | `http://31.97.67.145:6334` | ⚠️ sans auth |
| 7473 | Neo4j (HTTPS) | `https://31.97.67.145:7473` | ⚠️ exposed |
| 7474 | Neo4j Browser | `https://neo4j.recall-agency.com` (Caddy) ou direct | ⚠️ |
| 7687 | Neo4j Bolt | `bolt://31.97.67.145:7687` | ⚠️ |
| 8000 | Kong HTTP | `http://31.97.67.145:8000` | via Caddy aussi |
| 8081 | SearXNG | `http://31.97.67.145:8081` | exposé sans auth (à fermer) |
| 8443 | Kong HTTPS | `https://31.97.67.145:8443` | via Caddy aussi |
| 8765 | Palanthai API | `http://31.97.67.145:8765` | sans auth, direct |
| 9119 | HERMES Dashboard | `http://100.78.110.61:9119` (Tailscale only) | Tailscale ACL |
| 11434 | Ollama | `http://31.97.67.145:11434` | ⚠️ exposé (devrait être internal) |

### Tailscale (VPN interne)
| Port | Service | URL |
|---|---|---|
| 9119 | HERMES Dashboard | `http://100.78.110.61:9119` |

### Shared Hosting (92.113.28.34)
| Port | Service | URL | Auth |
|---|---|---|---|
| 65002 | WordPress | `https://reflexion.asia` | LiteSpeed |
| 65002 | WordPress | `https://recall-agency.com` | LiteSpeed |
| — | patrimonasia.com | — | ❌ Not built |

---

## 6. Syncthing Configuration

**Status :** ❌ service `syncthing@phil.service` est **inactive** (au 2026-06-01)
**Config file (à réactiver) :** `~/.config/syncthing/config.xml`

### Synced Folders (configurés, sendonly — VPS → Mac)
| VPS Folder | Mac Destination | Rescan Interval | Status |
|---|---|---|---|
| `/home/phil/palanthai` | TBC on Mac | 3600s (1h) | sendonly (config) |
| `/home/phil/obsidian-leon` | TBC on Mac | 3600s (1h) | sendonly (config) |

**Mode :** `sendonly` — changes on Mac are NOT synced back to VPS.

---

## 7. Caddy Proxy Routing

**File :** `/home/phil/local-ai-packaged/Caddyfile`

### ✅ Proxied (HTTPS via Caddy)
```
N8N_HOSTNAME      → n8n:5678       (https://n8n.recall-agency.com)
SUPABASE_HOSTNAME → kong:8000      (https://supabase.recall-agency.com)
NEO4J_HOSTNAME    → neo4j:7474     (https://neo4j.recall-agency.com)  ← actif
```

### ❌ NOT Proxied
- **Palanthai API** (port 8765) — HTTP, no Caddy involvement
- **WordPress sites** — separate server (92.113.28.34), LiteSpeed direct
- **HERMES Dashboard** (port 9119) — bound to internal Tailscale IP 100.78.110.61
- **Ollama** (port 11434) — exposé directement sur host, pas via Caddy
- **SearXNG** (port 8081) — exposé directement sur host, pas via Caddy

---

## 8. WordPress Sites (Shared Hosting)

**Server :** 92.113.28.34 (separate from VPS — LiteSpeed + PHP)

| Site | URL | Theme | SEO | Status |
|---|---|---|---|---|
| reflexion.asia | https://reflexion.asia | Houzez | RankMath | ✅ Production |
| recall-agency.com | https://recall-agency.com | Astra child | RankMath + Polylang | ✅ Production (FR/EN) |
| patrimonasia.com | https://patrimonasia.com | — | — | ❌ Not built |

**Cache :** LiteSpeed cache + LiteSpeed DOCREF active on recall-agency.com

---

## 9. Service Health Matrix

| Service | Container/Binary | Health | Auto-Restart |
|---|---|---|---|
| Caddy | Docker | ✅ Up 25h | docker compose |
| n8n | Docker | ✅ Up 25h | docker compose |
| Qdrant | Docker | ✅ Up 25h, status green | docker compose |
| Neo4j | Docker | ✅ Up 25h | docker compose |
| Supabase (11 containers) | Docker | ✅ Up 25h | docker compose |
| MinIO | Docker | ✅ Up 25h, healthy | docker compose |
| Valkey | Docker | ✅ Up 25h, healthy | docker compose |
| SearXNG | Docker | ✅ Up 25h | docker compose |
| Ollama | Docker | ✅ Up 25h | docker compose |
| ~~OpenWebUI~~ | ~~Docker~~ | ❌ retiré | n/a |
| Palanthai API | nohup uvicorn | ✅ PID 776 (19h+) | via `start_api.sh` ; **systemd disabled** |
| HERMES Dashboard | Python venv | ✅ PID 968 | ? |
| Fail2ban | systemd | ✅ active | auto |
| Tailscale | systemd | ✅ active | auto |
| Syncthing | systemd | ❌ **inactive** | à réactiver |

---

## 10. Palanthai Phase Pipeline — Service Mapping

```mermaid
flowchart TD
    subgraph P1["Phase 1 — Scraping (VPS /home/phil/palanthai/phase1_extraction)"]
        LP["LivePhuket.com"]
        SC["source_crawler.py"]
        WF["wf_extract/*.py"]
        FR["fullrun/fullrun.py"]
        LD["RUN_LOCKDOWN/"]
    end

    subgraph P2["Phase 2 — Sync (phase2_sync)"]
        SEQ["sequencer_v2.py"]
        UE["unit_extractor_v2.py"]
        DB["db_ingestor_units.py"]
    end

    subgraph P3["Phase 3 — Embedding (phase3_embedding_graph)"]
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

## 11. Données au 2026-06-01

| Source | Volume | Notes |
|---|---|---|
| PostgreSQL | 2 527 MB / 145 tables | Supabase `supabase-db` |
| `replica_unit` | **53 301** rows | table principale unités |
| `replica_projects_live` | **6 646** rows | projets |
| `unit_features` | 245 865 rows | features unités |
| Qdrant `units` | **45 039** vectors (768 dims) | status green, Cosine, HNSW m=16 |
| Qdrant `units_v3` | 200 vectors (1024 dims) | sparse + dense |
| Qdrant `projects_v3` | active | |
| Qdrant `palanthai_knowledge` | active | KB Reflexion |
| Qdrant `palanthai_memory` | active | |
| Qdrant `mem0migrations` | active | meta |

---

*Dernière mise à jour : 2026-06-01 | Source : `docker ps`, `docker volume ls`, `docker network ls`, `ps aux`, `ss -tlnp`, `/openapi.json`, `pg_database_size`, `pg_tables`*
*Voir : [[VPS_ARCHITECTURE_DIAGRAM]], [[VPS_BACKUP_INFRASTRUCTURE]], [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_ACCESS_REFERENCE]]*
