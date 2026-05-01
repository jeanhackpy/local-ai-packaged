---
type: infrastructure_reference
tags: [vps, ssh, n8n, docker, infrastructure, supabase, security, palanthai, scraper, rls]
updated: 2026-05-01
status: active
---

# 🖥️ VPS Hostinger — Infrastructure Complete Reference

> **Note Agent IA** : Lire ce fichier pour avoir le contexte complet VPS avant toute task. Connexion SSH via `ssh phil@31.97.67.145`.

> **🔐 SECURITY ALERT (2026-05-01)** : Security audit completed. 6 CRITICAL findings including hardcoded credentials. See [[VPS_Security_Audit_2026-05-01]] for full details. **Rotate all exposed credentials immediately.**

---

## 🏠 VPS Home Structure

```
/home/phil/
├── palanthai/                    # AI property intelligence platform (PRIMARY)
├── local-ai-packaged/            # Docker stack (n8n, Supabase, Qdrant, Ollama, etc.)
├── obsidian-leon/                # Leon's research & automation vault
├── venv/                         # Python 3.12 venv (site-packages: crawl4ai, psycopg2, etc.)
├── skills/                       # Claude Code skills installation
├── Cline/                        # Claude CLI workspace
├── Sync/                         # Sync scripts
├── global.yml                    # Ansible/scheduler config
├── kernel-metadata.json          # Kernel configs
├── vps-cleanup.sh               # Cleanup cron job
├── vps-monitor/                 # Monitoring scripts
├── cleanup-cron.log             # Cron log
├── CHECK-CLEANUP-WEEK.log        # Weekly check log
├── api.pid                       # Palanthai API PID file
├── palanthai-sync.service        # systemd service definition
└── skills-lock.json             # Skills lock file
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
| IP | 31.97.67.145 |
| Hostname | srv857744.hstgr.cloud |
| User | phil |
| SSH Key | ~/.ssh/id_ed25519 (ed25519) |
| OS | Ubuntu 24.04 LTS |
| Plan | KVM 2 — 2 vCPU / 8 GB RAM / 100 GB SSD |
| Provider | Hostinger VPS (VM ID: 857744) |

---

## 🌐 URLs Publiques

| Service | URL |
|---|---|
| **n8n** | https://n8n.recall-agency.com |
| Paperclip | https://paperclip.recall-agency.com |
| Palanthai API | http://31.97.67.145:8500 |
| Qdrant (ext) | http://31.97.67.145:6333 |
| Supabase DB | Port 5432 (internal only) |

---

## 📁 PALANTHAI — Property Intelligence Platform

**Répertoire:** `/home/phil/palanthai/`

### Structure Complete

```
palanthai/
├── CLAUDE.md                     ← Project definition (pour agents IA)
├── README.md
├── palanthai_api.py              ← Main FastAPI (Qdrant, Neo4j, Supabase integration)
├── palanthai_api.py.bak_20260328
├── start_api.sh                  ← API startup script
├── api.log                       ← API logs
├── api.pid                       ← PID file
│
├── config/
│   └── .env                      ← DB connections (PG, Qdrant, Neo4j, Ollama)
│
├── phase1-project-directory/     ← Scrapping pipeline (LIVE)
│   ├── CLAUDE.md                 ← Phase 1 instructions
│   ├── source_crawler.py         ← Discovers project/unit URLs from livephuket.com
│   ├── livephuket_login.py        ← Playwright auth for LivePhuket
│   ├── project_extractor.py      ← Playwright extraction of project details
│   ├── crawling_extractor.py     ← Unit extraction (Phase 5 adapter)
│   ├── unit_extractor_v2.py      ← Phase 5 unit extractor
│   ├── db_ingestor_units.py      ← Unit DB ingestor
│   ├── ingestor_v5.py            ← Phase 5 multi-DB ingestor (⚠️ CRITICAL: hardcoded PG fallback)
│   ├── sync_service.py           ← FastAPI sync service (⚠️ CRITICAL: hardcoded PG + command injection)
│   ├── models_parsers_00.py      ← Pydantic models + parsers
│   │
│   ├── fullrun/                  ← Full pipeline orchestrator
│   │   ├── fullrun.py            ← discover → projects → units pipeline
│   │   ├── setup_schema.py       ← Creates fullrun_* tables
│   │   └── data/                 ← JSONL batches + progress.json
│   │
│   ├── wf_extract/               ← 12 city-specific workflow scripts
│   │   ├── WF-extract-bangkok-condo.py
│   │   ├── WF-extract-bangkok-villa.py
│   │   ├── WF-extract-chiang-mai-condo.py
│   │   ├── WF-extract-chiang-mai-villa.py
│   │   ├── WF-extract-chon-buri-condo.py
│   │   ├── WF-extract-chon-buri-villa.py
│   │   ├── WF-extract-phuket-condo.py      ← Has pagination loop (other cities don't)
│   │   ├── WF-extract-phuket-villa.py
│   │   ├── WF-extract-prachuap-kiri-khan-condo.py
│   │   ├── WF-extract-prachuap-kiri-khan-villa.py
│   │   ├── WF-extract-surat-thani-condo.py
│   │   └── WF-extract-surat-thani-villa.py
│   │
│   └── lab_test_SCRIPTS/         ← Unit test scripts (not yet audited)
│       ├── TEST_api_db.py
│       ├── TEST_crawl4ai.py
│       └── TEST_source_crawler.py
│
├── phase2/                       ← Extraction pipeline (RUNNING)
│   ├── sequencer_v2.py           ← Batch orchestrator
│   ├── unit_extractor_v2.py
│   ├── unit_schema.py            ← Pydantic UnitRecord (33 fields)
│   ├── quality_checker.py
│   ├── db_ingestor_units.py
│   ├── data/
│   │   ├── master_queue.json
│   │   ├── progress.json         ← checkpoint
│   │   └── batches/batch_NNN/
│   │       ├── units.jsonl
│   │       ├── metrics.json
│   │       ├── quality_report.json
│   │       └── db_result.json
│   └── logs/sequencer_v2_*.log
│
├── phase3-embedding&graph/       ← Content pipeline
│   ├── content/
│   │   ├── data_cleaner.py       ← Pydantic: replaces source brands → Reflexion
│   │   ├── embed_to_qdrant.py     ← Ollama embedding → Qdrant
│   │   └── model_config.py        ← OpenRouter FREE model routing + chat()
│   └── kb_reflexion-leon/         ← Knowledge base (154 files)
│
├── phase4-image-classification/  ← (not audited)
├── phase5-mapping/               ← (not audited)
├── phase5-sync&update/           ← (not audited)
├── phase6-intelligence signal/   ← (not audited)
├── phase7-agentic-langraph/      ← (not audited)
│
├── content/
│   ├── reflexion/                ← Brand context files (TO CREATE)
│   ├── recall/
│   └── patrimonasia/
│
├── analytics/                    ← GA4/GSC scripts
├── data/                         ← Extracted data batches
├── docs/                         ← Documentation
├── DATABASE_schemas/             ← Schema definitions
├── Knowledge/                    ← Knowledge base
├── ORCHESTRATION_content_creation-flywheels/
├── SESSION_NOTES.md
├── sql/                          ← SQL scripts
├── archive/                      ← Old versions
└── logs/                         ← Operational logs
```

### LivePhuket Scraper Regions
```python
_ACTIVE_REGIONS = ["bangkok", "phuket", "surat-thani", "chiang-mai", "chon-buri", "prachuap-kiri-khan"]
```

### Palanthai API Endpoints
- `GET /api/v1/source/projects` — List source projects
- `POST /api/v1/sync` — Trigger sync
- `POST /api/v1/sync/neo4j/*` — Neo4j sync endpoints

### Quality Thresholds
- **Project extraction**: quality_score ≥ 60
- **Unit embedding**: quality_score ≥ 75/100 (governance gate)

---

## 🐳 LOCAL-AI-PACKAGED — Docker Stack

**Répertoire:** `/home/phil/local-ai-packaged/`

### Structure Complete

```
local-ai-packaged/
├── docker-compose.yml            ← Main compose (Supabase, Qdrant, Ollama, n8n, Caddy)
├── docker-compose.override.public.yml
├── docker-compose.override.private.yml
├── docker-compose.override.public.supabase.yml
├── Caddyfile                     ← Reverse proxy config (TLS)
├── Caddyfile.backup / .bak
│
├── .env                          ← ⚠️ CRITICAL: 15+ hardcoded secrets
│                                  ← N8N_ENCRYPTION_KEY, POSTGRES_PASSWORD, ANON_KEY,
│                                  ← SERVICE_ROLE_KEY, JWT_SECRET, OPENROUTER_API_KEY,
│                                  ← GROQ_API_KEY, TELEGRAM_BOT_TOKEN, ELEVENLABS_API_KEY
│
├── start_services.py             ← ⚠️ HIGH: command injection risk (subprocess.run shell=True)
│
├── config-guard.sh              ← Config backup script
│
├── supabase/                    ← Supabase Docker config
├── neo4j/                       ← Neo4j config
├── openclaw/                    ← OpenClaw gateway
├── n8n_pipe.py                  ← n8n webhook pipe
├── router_pipe.py               ← Router pipe
├── caddy-addon/                 ← Caddy plugins
├── scripts/                     ← Utility scripts
├── searxng/                     ←SearXNG meta-search engine
├── docs/                        ← Documentation
├── logs/                        ← Container logs
├── assets/                      ← Static assets
├── shared/                      ← Shared data
│
└── n8n/                         ← n8n workflows
    ├── workflows/               ← Active workflows
    │   ├── SEO_Article_Monitoring_Generation.json
    │   ├── V1_Local_RAG_AI_Agent.json
    │   ├── V2_Local_Supabase_RAG_AI_Agent.json
    │   └── V3_Local_Agentic_RAG_AI_Agent.json
    └── backup/                  ← WF-002 to WF-006 backups
```

### Docker Services

| Container | Image | Ports | Status |
|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443 | ✅ Running |
| qdrant | qdrant/qdrant | 6333-6334 | ✅ Running |
| n8n | ad20607cdd24 | 5678 | ✅ Running |
| minio | minio/minio | 9000-9001 | ✅ Running (healthy) |
| redis (valkey) | valkey/valkey:8-alpine | 6379 | ✅ Running |
| searxng | searxng/searxng:latest | 8081 | ✅ Running |
| supabase-kong | kong:2.8.1 | 8000, 8443 | ✅ Running |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 | ✅ Running |
| supabase-auth | supabase/gotrue:v2.184.0 | — | ✅ Running |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 | ✅ Running |
| supabase-studio | supabase/studio:2025.12.17 | 3000 | ✅ Running |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 | ✅ Running |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432 | ✅ Running |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | — | ✅ Running |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | ✅ Running |
| realtime | supabase/realtime:v2.68.0 | — | ✅ Running |
| **ollama** | ollama/ollama:latest | 11434 | ⚠️ Exited (0) |
| **open-webui** | ghcr.io/open-webui/open-webui:main | — | ⚠️ Exited (137) |
| **neo4j** | neo4j:latest | 7474, 7687 | ❌ INACTIVE |

---

## 📁 OBSIDIAN-LEON — Research & Automation Vault

**Répertoire:** `/home/phil/obsidian-leon/`

### Structure Complete

```
obsidian-leon/
├── HOME.md
├── README.md
├── WIKI.md / WIKI_SCHEMA.md
├── LOG.md / log.md
│
├── Infrastructure/              ← VPS/infrastructure docs
├── Recherches/                  ← 47 research documents
├── References/                   ← Ontology, real-estate math, Palantir strategy
├── agent_formation/             ← Agent training materials
├── analysis/                    ← Analysis docs
├── campaigns/                   ← UAE → Thailand campaign (Phase 1 complete)
│
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
├── PIPELINE_data_extraction/    ← Fazwaz scraper + data v1
│   ├── condo-price-pred/
│   └── repos/
│
├── scripts/                     ← ⚠️ CRITICAL: migrate_cloud_to_vps.py + setup_vps_neo4j.py
│   ├── migrate_cloud_to_vps.py   ← ⚠️ Live DB creds + Supabase anon key hardcoded
│   ├── setup_vps_neo4j.py        ← ⚠️ Live Neo4j + DB passwords hardcoded
│   ├── setup_vps_qdrant.py       ← (not yet audited)
│   ├── openclaw_ts_proxy.py
│   ├── bulk_index_kb.py
│   ├── clean_kb_v2.py
│   ├── deep_clean_kb.py
│   ├── scrape_forum_full.py
│   ├── sync-obsidian-leon.sh
│   ├── watch-meeting-room.py
│   ├── weekly_update.sh
│   ├── cleanup-vps.sh
│   └── seo/
│
├── meeting_room/                ← Meeting notes, debriefs
├── projects/                    ← Project-specific docs
├── systems/                     ← System docs
├── veille/                      ← Monitoring/tracking
├── ontology/                    ← Ontology files
├── ideas/                       ← Ideas
├── database/                    ← DB docs
├── wiki/                        ← Wiki
├── skills-openclaw.md / Leon-Skills-OpenClaw.md
├── Leon-Rapport-Scraping.md
├── PROJETS-ACTIFS.md
├── THAILAND_NEWS_FEEDS.md
└── 00_SYSTEM/                   ← System config
```

---

## 🔗 URLs Internes Docker (n8n workflows)

```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434   # ⚠️ Ollama container stopped
REDIS_HOST=redis:6379             # Valkey (Redis-compatible)
NEO4J_URL=bolt://neo4j:7687      # ⚠️ Neo4j inactive
```

---

## 🔐 SECURITY FINDINGS SUMMARY

> Full report: [[VPS_Security_Audit_2026-05-01]]

### CRITICAL — Rotate Immediately
1. **`local-ai-packaged/.env`** — 15+ live API keys (n8n, Supabase, OpenRouter, Groq, Telegram, ElevenLabs)
2. **`palanthai/phase1-project-directory/ingestor_v5.py`** — Hardcoded Postgres fallback password
3. **`palanthai/phase1-project-directory/sync_service.py`** — Hardcoded Postgres + command injection
4. **`obsidian-leon/scripts/migrate_cloud_to_vps.py`** — Live DB password + Supabase anon key
5. **`obsidian-leon/scripts/setup_vps_neo4j.py`** — Live Neo4j + DB passwords

### HIGH — Fix Before Next Deployment
1. **`local-ai-packaged/start_services.py`** — `subprocess.run(cmd, shell=True)` command injection
2. **12 × `wf_extract/WF-extract-*.py`** — No auth on LivePhuket calls, no retry logic
3. **`fullrun/fullrun.py`** — Memory pause could hang indefinitely (< 800 MiB wait)

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

---

## 🚀 Services Non-Docker

| Service | Type | Port | Status |
|---|---|---|---|
| **Palanthai API** | systemd (`palanthai-sync.service`) | 8500 | ✅ Running |
| **Qdrant** | Docker | 6333 | ✅ Running |
| **n8n** | Docker | 5678 | ✅ Running |
| **PostgreSQL** | Docker (supabase-db) | 5432 | ✅ Running |

---

## 🛠️ Commandes Utiles

```bash
# Statut des containers
ssh phil@31.97.67.145 'docker ps --format "{{.Names}}: {{.Status}}"'

# Logs n8n
ssh phil@31.97.67.145 'docker logs n8n --tail 50'

# Restart n8n
ssh phil@31.97.67.145 'cd /home/phil/local-ai-packaged && docker compose restart n8n n8n-worker'

# Redémarrage stack complète
ssh phil@31.97.67.145 'cd /home/phil/local-ai-packaged && docker compose up -d'

# Palanthai API logs
ssh phil@31.97.67.145 'tail -f /home/phil/palanthai/logs/api.log'

# Fullrun progress
ssh phil@31.97.67.145 'cat /home/phil/palanthai/phase1-project-directory/fullrun/data/progress.json'
```

---

## 📊 WordPress Integration

| Site | URL | Status |
|---|---|---|
| reflexion.asia | 92.113.28.34:65002 | ✅ Ready (RankMath, Polylang) |
| recall-agency.com | 92.113.28.34:65002 | ✅ Ready (RankMath, Polylang) |
| patrimonasia.com | — | ❌ NOT BUILT YET |

---

*Dernière mise à jour : 2026-05-01 | Security audit + full VPS structure mapping*