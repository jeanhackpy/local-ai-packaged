---
type: infrastructure_reference
tags: [vps, ssh, n8n, docker, infrastructure, supabase, security, palanthai, scraper, rls]
updated: 2026-06-01
status: active
---

# 🖥️ VPS Hostinger — Infrastructure Complete Reference

> **Note Agent IA** : Lire ce fichier pour avoir le contexte complet VPS avant toute task. Connexion SSH via `ssh phil@31.97.67.145`.

> **🔐 SECURITY ALERT (2026-05-01)** : Security audit completed. 6 CRITICAL findings including hardcoded credentials. See [[VPS_Security_Audit_2026-05-01]] for full details. **Rotate all exposed credentials immediately.**

---

## 🏠 VPS Home Structure (au 2026-06-01)

```
/home/phil/
├── palanthai/                    # AI property intelligence platform (PRIMARY)
├── local-ai-packaged/            # Docker stack (n8n, Supabase, Qdrant, Ollama, Neo4j, etc.)
├── obsidian-leon/                # Leon's research & automation vault
├── venv/                         # Python 3.12 venv (site-packages: crawl4ai, psycopg2, etc.)
├── skills/                       # Claude Code skills installation
├── Cline/                        # Claude CLI workspace
├── Sync/                         # Sync scripts
├── .hermes/                      # HERMES agent (Python venv, dashboard :9119)
├── .claude/                      # Claude config (CLI session logs)
├── .codex/                       # Codex CLI data
├── .gemini/                      # Gemini CLI data
├── .bun/                         # Bun runtime
├── .antigravity-*/               # Antigravity IDE workspace
├── api.pid → /home/phil/palanthai/api.pid  (NB: pid file is in palanthai/, not /home/)
├── palanthai-sync.service        # systemd unit (DISABLED, ne démarre pas l'API)
│
│ ── legacy / cleanup candidates ──────────────────────────────────
├── vps-cleanup.sh                # Cleanup cron
├── vps-monitor/                  # Monitoring scripts
├── cleanup-cron.log              # Cron log
└── CHECK-CLEANUP-WEEK.log        # Weekly check log
```

---

## 🔑 Accès SSH

```bash
ssh phil@31.97.67.145
ssh -i ~/.ssh/id_ed25519 phil@31.97.67.145
ssh phil@srv857744.hstgr.cloud
```

| Paramètre | Valeur |
|---|---|
| IP principale | 31.97.67.145 |
| IP Tailscale | 100.78.110.61 |
| Hostname | srv857744.hstgr.cloud |
| User | phil |
| SSH Key | ~/.ssh/id_ed25519 (ed25519) |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Kernel | 6.8.0-117-generic |
| Plan | KVM 2 — 2 vCPU / 7.8 GB RAM / 96 GB SSD |
| Disk | 84 GB used / 13 GB free (87%) |
| Provider | Hostinger VPS (VM ID: 857744) |

---

## 🌐 URLs Publiques

| Service | URL | Notes |
|---|---|---|
| **n8n** | https://n8n.recall-agency.com | via Caddy |
| **Supabase** | https://supabase.recall-agency.com | via Caddy → Kong:8000 |
| **Neo4j Browser** | https://neo4j.recall-agency.com | via Caddy → neo4j:7474 |
| Paperclip | https://paperclip.recall-agency.com | déclaré dans `.env` |
| Palanthai API | http://31.97.67.145:8765 | **HTTP direct, port 8765** |
| Qdrant REST | http://31.97.67.145:6333 | sans auth ⚠️ |
| HERMES Dashboard | http://100.78.110.61:9119 | bind interne Tailscale |

---

## 📁 PALANTHAI — Property Intelligence Platform

**Répertoire :** `/home/phil/palanthai/`
**Version API :** 1.0.0 (Title: `Palanthai Local API`, 49 routes)
**Démarrage :** `nohup` via `start_api.sh` ; systemd `palanthai-sync.service` est **disabled**

### Structure Réelle (au 2026-06-01)

```
palanthai/
├── CLAUDE.md                     ← Project definition (pour agents IA)
├── README.md / SESSION_NOTES.md
├── palanthai_api.py              ← Main FastAPI (49 routes)
├── start_api.sh                  ← nohup uvicorn (port 8765, --reload)
├── api.log / api.pid             ← Logs + PID à la racine
│
├── config/
│   ├── .env                      ← 20 clés (GA4, GSC, Neo4j, Qdrant, Ollama, WordPress…)
│   └── api.pid / google_service_account.json
│
├── phase1_extraction/            ← ⚠️ rename: ancien "phase1-project-directory"
│   ├── CLAUDE.md
│   ├── README_PHASE1.md
│   ├── PALANTHAI_OPERATIONS.md / PIPELINE_STATE.md / SANDBOX_MAPPING.md
│   ├── source_crawler.py / sync_count_ping.py
│   ├── project_extractor.py / crawling_extractor.py
│   ├── ingestor_v5.py / sync_service.py   ← ⚠️ security issues
│   ├── RUN_LOCKDOWN/             ← nouveau (lockdown workflow)
│   ├── LAB_TEST_SCRIPTS/         ← unit tests
│   ├── crawl4ai/ / crawl4ai_skills/ / venv/
│   └── backups/ / .planning/ / .env.local
│
├── phase2_sync/                  ← ⚠️ rename: ancien "phase2/"
│   ├── wf_proto.py (24K) / extract_one.py / db_io.py
│   ├── AUTOMATION.md / WORKFLOWS.md
│   ├── data/ / _archive/ / __pycache__/
│
├── phase3_embedding_graph/       ← ⚠️ rename: ancien "phase3-embedding&graph"
│   ├── ingestor_v5.py / sync_service.py / crawling_extractor.py
│   ├── project_extractor.py / source_crawler.py
│   ├── models_parsers_00.py / db_helpers_00.py / schemas.py
│   ├── kaggle_bge_m3.ipynb / massive_embedding*.ipynb
│   ├── audit-report-full.md / agent.md / phase3_goal.md
│   ├── n8n/ / n8n_workflow_*.json
│   ├── database/ / pipeline/ / logs/ / outputs/ / colab_export/
│   ├── supabase-edge-functions/
│   └── wf_extract/               ← 12 city-specific workflow scripts
│
├── phase4_vision/                ← image classification
├── phase5_mapping/               ← (renommé)
├── phase6_intelligence/          ← (renommé)
├── phase7_agents/                ← (renommé)
│
├── content_flywheels/            ← ⚠️ NEW vs old doc
├── knowledge_base/               ← ⚠️ NEW (reflexion_kb_clean.json, kb_reflexion*)
├── legacy_phase2_data/           ← ⚠️ NEW (anciennes données)
├── audits/                       ← ⚠️ NEW
├── docs/                         ← PALANTHAI_TUTORIAL.md, WF_PROTO_SYNC.md
├── scripts/                      ← ⚠️ NEW
├── sql/                          ← SQL scripts
└── logs/                         ← bulk_embed.log, verify_run_*.log, etc.
```

### LivePhuket Scraper Regions
```python
_ACTIVE_REGIONS = ["bangkok", "phuket", "surat-thani", "chiang-mai", "chon-buri", "prachuap-kiri-khan"]
```

### Palanthai API — Endpoints (49 routes, source : `/openapi.json`)

| Groupe | Endpoints |
|---|---|
| Health | `GET /health`, `GET /services/health`, `GET /system/resources` |
| Workflows | `POST /wf_proto/extract`, `POST /wf_proto/refresh_prices`, `POST /wf_proto/ping`, `POST /wf_proto/new_units` |
| Scraper | `POST /scraper/run` |
| Lockdown sync | `GET /lockdown/sync/ping-one`, `POST /lockdown/sync/projects-count`, `POST /lockdown/sync/projects-extract-new`, `POST /lockdown/sync/units-new`, `POST /lockdown/sync/units-update`, `GET /lockdown/sync_v2/daily_summary`, `POST /lockdown/sync_v2/new_project`, `POST /lockdown/sync_v2/new_unit`, `POST /lockdown/sync_v2/updated_unit` |
| Sync | `GET /sync/check-counts`, `POST /sync/count`, `POST /sync/projects/delta`, `POST /sync/projects/extract`, `POST /sync/run-all`, `POST /sync/units/extract`, `POST /sync/units/price-refresh` |
| Queue | `POST /queue/check-duplicate`, `POST /queue/insert`, `GET /queue/next` |
| Units | `POST /units/embed`, `POST /units/mark-synced`, `GET /units/next-unsynced`, `POST /units/price-update`, `POST /units/upsert` |
| Subjects | `GET /subjects`, `POST /subjects` |
| Memory | `POST /memory/add`, `DELETE /memory/delete`, `GET /memory/list`, `POST /memory/search` |
| Content | `POST /content/atomize`, `POST /content/embed`, `POST /content/enrich-facts`, `POST /content/generate`, `POST /content/inject-links`, `POST /content/update-faq-hub` |
| SEO | `GET /seo/content-performance`, `GET /seo/gsc-pages`, `GET /seo/keywords`, `GET /seo/pages`, `POST /seo/request-indexing`, `POST /seo/sync-subjects` |

> ⚠️ Les anciens endpoints `/api/v1/source/projects`, `/api/v1/sync`, `/api/v1/sync/neo4j/*` mentionnés dans l'ancienne doc **n'existent plus** — ce sont des paths legacy.

### Quality Thresholds
- **Project extraction**: quality_score ≥ 60
- **Unit embedding**: quality_score ≥ 75/100 (governance gate)

---

## 🐳 LOCAL-AI-PACKAGED — Docker Stack

**Répertoire :** `/home/phil/local-ai-packaged/`
**Network :** `localai_default` (172.18.0.0/16)
**Containers actifs :** 19 (tous `Up 25 hours` au 2026-06-01)

### Structure Complete

```
local-ai-packaged/
├── docker-compose.yml                       ← Main compose
├── docker-compose.override.public.yml
├── docker-compose.override.private.yml
├── docker-compose.override.public.supabase.yml
├── Caddyfile                                ← Reverse proxy (TLS) — 3 routes actives
│
├── .env                                     ← ⚠️ CRITICAL: 40 hardcoded secrets
│                                              (N8N_ENCRYPTION_KEY, POSTGRES_PASSWORD,
│                                               ANON_KEY, SERVICE_ROLE_KEY, JWT_SECRET,
│                                               OPENROUTER_API_KEY, GROQ_API_KEY,
│                                               TELEGRAM_BOT_TOKEN, ELEVENLABS_API_KEY,
│                                               OLLAMA_CLOUD_URL, NVIDIA_API_KEY,
│                                               SERPER_API_KEY, INDEXNOW_KEY, etc.)
│
├── start_services.py                        ← ⚠️ HIGH: command injection risk
├── config-guard.sh                          ← Config backup script
│
├── n8n/                                     ← n8n workflows (1 actif : Local_RAG_AI_Agent)
│   └── workflows/Local_RAG_AI_Agent_n8n_Workflow.json
├── supabase/ / neo4j/ / searxng/ / scripts/ / docs/ / logs/ / assets/ / shared/ / caddy-addon/
├── ARCHITECTURE_LOG.md / Caddyfile (et .bak multiples) / .env.example / .env.bak.20260326
├── .git/ / .gitignore / .gitattributes / .github/ / LICENSE / README.md
├── __pycache__/ / .stfolder/ / .golden/ / .jules/
```

### Docker Services (au 2026-06-01)

| Container | Image | Ports (Host) | Status |
|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443, 443/udp, 2019 | ✅ Running |
| qdrant | qdrant/qdrant:latest | 6333-6334 | ✅ Running |
| n8n | n8nio/n8n:latest | 5678 | ✅ Running |
| minio | minio/minio:latest | 9000-9001 (interne) | ✅ Running (healthy) |
| redis (valkey) | valkey/valkey:8-alpine | 6379 | ✅ Running (healthy) |
| searxng | searxng/searxng:latest | 8081→8080 | ✅ Running |
| supabase-kong | kong:2.8.1 | 8000, 8443 | ✅ Running (healthy) |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 (interne) | ✅ Running (healthy) |
| supabase-auth | supabase/gotrue:v2.184.0 | — | ✅ Running (healthy) |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 (interne) | ✅ Running |
| supabase-studio | supabase/studio:2025.12.17-sha-43f4f7f | 3000 (interne) | ✅ Running (healthy) |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 (interne) | ✅ Running (healthy) |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432, 6543 | ✅ Running (healthy) |
| supabase-meta | supabase/postgres-meta:v0.95.1 | 8080 (interne) | ✅ Running (healthy) |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | 8080 (interne) | ✅ Running (healthy) |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | ✅ Running |
| realtime | supabase/realtime:v2.68.0 | — | ✅ Running (healthy) |
| **ollama** | ollama/ollama:latest | 11434 | ✅ **Running** (10.6 GB image) |
| **neo4j** | neo4j:latest | 7473, 7474, 7687 | ✅ **Running** |

> ❌ **open-webui** — plus présent dans la stack.

---

## 📁 OBSIDIAN-LEON — Research & Automation Vault

**Répertoire :** `/home/phil/obsidian-leon/`

### Structure Complete

```
obsidian-leon/
├── HOME.md / README.md / WIKI.md / WIKI_SCHEMA.md / LOG.md
├── 00_SYSTEM/ / Infrastructure/ / Recherches/ / References/ / agent_formation/
├── analysis/ / campagnes/ / database/ / ideas/ / logs/ / meeting_room/
├── n8n/                         ← n8n workflow exports
│   ├── WF-002-GENERATE-FAQ-REFLEXION.md
│   ├── WF-003-REVIEW-HUMAN-REFLEXION.md
│   ├── WF-005-GDRIVE-CONTENT-FEEDER.md
│   ├── WF-006-MONITOR-HEALTH-ALL.md
│   ├── WF-008-SYNC-NEW-LISTINGS.md
│   ├── WF-009-PRICE-UPDATE.md
│   ├── WORKFLOWS-A-RETROUVER.md
│   └── LOCAL-RAG-EVOLUTION.md
│
├── "extractor data v1"/         ← ⚠️ NEW (ancien "PIPELINE_data_extraction/")
├── sites-immobiliers/           ← ⚠️ NEW
│
├── scripts/                     ← ⚠️ CRITICAL: migrate_cloud_to_vps.py + setup_vps_neo4j.py
│   ├── migrate_cloud_to_vps.py   ← ⚠️ Live DB creds + Supabase anon key hardcoded
│   ├── setup_vps_neo4j.py        ← ⚠️ Live Neo4j + DB passwords hardcoded
│   ├── setup_vps_qdrant.py / openclaw_ts_proxy.py / bulk_index_kb.py
│   ├── clean_kb_v2.py / deep_clean_kb.py / scrape_forum_full.py
│   ├── sync-obsidian-leon.sh / watch-meeting-room.py
│   ├── weekly_update.sh / cleanup-vps.sh / seo/
│
├── projects/ / systems/ / veille/ / ontology/ / wiki/
├── skills-openclaw.md / Leon-Skills-OpenClaw.md / Leon-Rapport-Scraping.md
├── PROJETS-ACTIFS.md / THAILAND_NEWS_FEEDS.md
```

---

## 🔗 URLs Internes Docker (n8n workflows)

```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434        # ✅ réactivé
REDIS_HOST=redis:6379                  # Valkey
NEO4J_URL=bolt://neo4j:7687            # ✅ réactivé
SEARXNG_URL=http://searxng:8080        # container port 8080
```

---

## 📊 Données Production (au 2026-06-01)

| Source | Volume | Notes |
|---|---|---|
| PostgreSQL | 2 527 MB / 145 tables public | `supabase-db` |
| `replica_unit` | **53 301** rows | table principale |
| `replica_projects_live` | **6 646** rows | projets |
| `unit_features` | 245 865 rows | features |
| Qdrant `units` | **45 039** vectors (768 dims) | status green, Cosine, HNSW m=16 |
| Qdrant `units_v3` | 200 vectors (1024 dims) | sparse + dense, nouvelle collection |
| Qdrant `projects_v3` | active | |
| Qdrant `palanthai_knowledge` | active | KB Reflexion |
| Qdrant `palanthai_memory` | active | |
| Qdrant `mem0migrations` | active | meta |

### Caddyfile (au 2026-06-01)

```caddy
{$N8N_HOSTNAME}      → n8n:5678       # n8n.recall-agency.com
{$SUPABASE_HOSTNAME} → kong:8000      # supabase.recall-agency.com
{$NEO4J_HOSTNAME}    → neo4j:7474     # neo4j.recall-agency.com (actif)
# Ollama — internal only (commented out)
# SearXNG — internal only (commented out)
```

---

## 🔐 SECURITY FINDINGS SUMMARY

> Full report: [[VPS_Security_Audit_2026-05-01]]

### CRITICAL — Rotate Immediately
1. **`local-ai-packaged/.env`** — **40 hardcoded secrets** (n8n, Supabase, OpenRouter, Groq, Telegram, ElevenLabs, Ollama Cloud, NVIDIA, Serper, OpenClaw, INDEXNOW, QuicCloud, CodeX NVIDIA, etc.)
2. **`palanthai/phase1_extraction/ingestor_v5.py`** — Hardcoded Postgres fallback password
3. **`palanthai/phase1_extraction/sync_service.py`** — Hardcoded Postgres + command injection
4. **`obsidian-leon/scripts/migrate_cloud_to_vps.py`** — Live DB password + Supabase anon key
5. **`obsidian-leon/scripts/setup_vps_neo4j.py`** — Live Neo4j + DB passwords

### HIGH — Fix Before Next Deployment
1. **`local-ai-packaged/start_services.py`** — `subprocess.run(cmd, shell=True)` command injection
2. **12 × `wf_extract/WF-extract-*.py`** — No auth on LivePhuket calls, no retry logic
3. **`fullrun/fullrun.py`** — Memory pause could hang indefinitely (< 800 MiB wait)

### Ports Exposés Sans Auth (à protéger)
- 5432 (PostgreSQL pooler)
- 6333 / 6334 (Qdrant REST + gRPC)
- 7473 / 7474 (Neo4j browser)
- 7687 (Neo4j Bolt)
- 8081 (SearXNG)
- 11434 (Ollama)
- 8765 (Palanthai API, no auth)

### Credentials To Rotate
| Service | Found In | Exposed Value |
|---|---|---|
| VPS PostgreSQL | `migrate_cloud_to_vps.py`, `setup_vps_neo4j.py` | `xpKe3z1z8q5d1QKjx1ZZzRRgFtQlUe3K` |
| Neo4j | `setup_vps_neo4j.py` | `9PXofEGxRCw2O119HC3RnRUK` |
| Supabase anon key | `migrate_cloud_to_vps.py` | `eyJhbGci...` (project `owmucbudvleotyilotoq`) |
| Supabase service role | `local-ai-packaged/.env` | `SERVICE_ROLE_KEY` |
| n8n encryption | `local-ai-packaged/.env` | `N8N_ENCRYPTION_KEY` |
| JWT secret | `local-ai-packaged/.env` | `JWT_SECRET` |
| OpenRouter | `local-ai-packaged/.env` | `OPENROUTER_API_KEY` |
| Groq | `local-ai-packaged/.env` | `GROQ_API_KEY` |
| Telegram | `local-ai-packaged/.env` | `TELEGRAM_BOT_TOKEN` |
| ElevenLabs | `local-ai-packaged/.env` | `ELEVENLABS_API_KEY` |
| Ollama Cloud | `local-ai-packaged/.env` | `OLLAMA_CLOUD_URL`, `OLLAMA_API_KEY` |
| NVIDIA | `local-ai-packaged/.env` | `NVIDIA_API_KEY`, `CODEX_NVIDIA_API_KEY` |
| Serper | `local-ai-packaged/.env` | `SERPER_API_KEY` |
| OpenClaw | `local-ai-packaged/.env` | `OPENCLAW_GATEWAY_TOKEN` |
| INDEXNOW | `local-ai-packaged/.env` | `INDEXNOW_KEY` |
| QuicCloud | `local-ai-packaged/.env` | `QUIC_CLOUD_API_KEY` |

### Erreur Runtime Observée
- `palanthai_api.py:539` → `ModuleNotFoundError: No module named 'analytics'` (au hit de `/seo/sync-subjects`)
- Source: `api.log` (70 KB, 1.2 MB writeln visible)

---

## 🚀 Services Non-Docker

| Service | Type | Port | Status |
|---|---|---|---|
| **Palanthai API** | `nohup uvicorn` (start_api.sh) | **8765** | ✅ Running (PID 776) |
| **HERMES Dashboard** | Python venv | 9119 (bind 100.78.110.61) | ✅ Running |
| **Fail2ban** | systemd | — | ✅ active |
| **Tailscale** | systemd | — | ✅ active |
| **Syncthing** | systemd | 8384 | ❌ inactive |
| PostgreSQL | Docker (supabase-db) | 5432 (interne) | ✅ Running (healthy) |
| Qdrant | Docker | 6333 | ✅ Running |
| n8n | Docker | 5678 | ✅ Running |

---

## 🛠️ Commandes Utiles

```bash
# Statut des containers
ssh phil@31.97.67.145 'docker ps --format "{{.Names}}: {{.Status}}"'

# Logs n8n
ssh phil@31.97.67.145 'docker logs n8n --tail 50'

# Restart n8n
ssh phil@31.97.67.145 'cd /home/phil/local-ai-packaged && docker compose restart n8n'

# Redémarrage stack complète
ssh phil@31.97.67.145 'cd /home/phil/local-ai-packaged && docker compose up -d'

# Restart Palanthai API
ssh phil@31.97.67.145 'kill $(cat /home/phil/palanthai/api.pid) && nohup /home/phil/palanthai/start_api.sh &'

# Logs Palanthai API
ssh phil@31.97.67.145 'tail -f /home/phil/palanthai/api.log'

# Health check API
curl -s http://31.97.67.145:8765/health

# Qdrant collections
curl -s http://31.97.67.145:6333/collections

# PG sizes
ssh phil@31.97.67.145 'docker exec supabase-db psql -U postgres -d postgres -c "SELECT pg_database_size('\''postgres'\'') / 1024 / 1024 AS size_mb;"'

# Phase1 state
ssh phil@31.97.67.145 'cat /home/phil/palanthai/phase1_extraction/PIPELINE_STATE.md 2>/dev/null || ls /home/phil/palanthai/phase1_extraction/'
```

---

## 📊 WordPress Integration

| Site | URL | Status |
|---|---|---|
| reflexion.asia | 92.113.28.34:65002 | ✅ Ready (RankMath, Polylang) |
| recall-agency.com | 92.113.28.34:65002 | ✅ Ready (RankMath, Polylang) |
| patrimonasia.com | — | ❌ NOT BUILT YET |

---

*Dernière mise à jour : 2026-06-01 | Refresh complet basé sur inspection live du VPS*
*Voir : [[VPS_ACCESS_REFERENCE]], [[VPS_SERVICE_MAP]], [[VPS_ARCHITECTURE_DIAGRAM]], [[Network_Architecture]], [[VPS_BACKUP_INFRASTRUCTURE]]*
