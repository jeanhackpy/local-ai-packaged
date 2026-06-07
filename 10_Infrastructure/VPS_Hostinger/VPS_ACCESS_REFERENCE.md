---
type: infrastructure_reference
tags: [vps, ssh, n8n, docker, infrastructure, supabase, security, rls]
updated: 2026-06-01
status: active
---

# 🖥️ VPS Hostinger — Accès & Services

> **Note Agent IA** : Lire ce fichier en début de session pour avoir accès au VPS et connaître l'état des services. Pour la structure complète et la sécurité, voir [[VPS_INFRASTRUCTURE_REFERENCE]].

> **🔐 SECURITY ALERT (2026-05-01)** : 6 CRITICAL findings — hardcoded credentials in multiple scripts. See [[VPS_Security_Audit_2026-05-01]] and [[VPS_INFRASTRUCTURE_REFERENCE]] for full details. **Rotate all exposed credentials immediately.**

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
| IP interne (Tailscale) | 100.78.110.61 |
| Hostname | srv857744.hstgr.cloud |
| User | phil |
| SSH Key | ~/.ssh/id_ed25519 (ed25519) |
| OS | Ubuntu 24.04.4 LTS (Noble Numbat) |
| Kernel | 6.8.0-117-generic |
| Plan | KVM 2 — 2 vCPU / 7.8 GB RAM / 96 GB SSD |
| Disk usage | 84 GB used / 13 GB free (87%) |
| Uptime (au 2026-06-01) | ~1 jour, load average 1.4 |
| Provider | Hostinger VPS (VM ID: 857744) |

---

## 🌐 URLs Publiques

| Service | URL | Notes |
|---|---|---|
| **n8n** | https://n8n.recall-agency.com | via Caddy |
| **Supabase** | https://supabase.recall-agency.com | via Caddy → Kong:8000 |
| **Neo4j Browser** | https://neo4j.recall-agency.com | via Caddy → neo4j:7474 (active) |
| Paperclip | https://paperclip.recall-agency.com | déclaré dans `.env` (`PAPERCLIP_HOSTNAME`) |
| Palanthai API | http://31.97.67.145:8765 | **HTTP direct, port 8765** (pas 8500) |
| Qdrant REST | http://31.97.67.145:6333 | sans auth ⚠️ |
| HERMES Dashboard | http://100.78.110.61:9119 | bindé sur IP interne uniquement |

> ⚠️ Ollama (11434) et SearXNG (8081) ne sont **plus exposés** publiquement — internal only.

---

## 🐳 Services Docker Actifs

**Répertoire :** `/home/phil/local-ai-packaged/`
**Stack :** 19 containers — tous `Up 25 hours` (au 2026-06-01)

| Container | Image | Ports (Host) | Rôle | Status |
|---|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443, 443/udp, 2019 | Reverse proxy / TLS | ✅ Running |
| qdrant | qdrant/qdrant:latest | 6333-6334 | Vector DB | ✅ Running |
| n8n | n8nio/n8n:latest | 5678 | Automation | ✅ Running |
| minio | minio/minio:latest | 9000-9001 (interne) | Object storage | ✅ Running (healthy) |
| redis (valkey) | valkey/valkey:8-alpine | 6379 | Cache / Queue | ✅ Running (healthy) |
| searxng | searxng/searxng:latest | 8081→8080 | Moteur recherche | ✅ Running |
| supabase-kong | kong:2.8.1 | 8000, 8443 | API Gateway | ✅ Running (healthy) |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 (interne) | Base de données | ✅ Running (healthy) |
| supabase-auth | supabase/gotrue:v2.184.0 | — | Auth | ✅ Running (healthy) |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 (interne) | REST API | ✅ Running |
| supabase-studio | supabase/studio:2025.12.17-sha-43f4f7f | 3000 (interne) | Dashboard | ✅ Running (healthy) |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 (interne) | Storage | ✅ Running (healthy) |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432, 6543 | Connection pooler | ✅ Running (healthy) |
| supabase-meta | supabase/postgres-meta:v0.95.1 | 8080 (interne) | pg-meta | ✅ Running (healthy) |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | 8080 (interne) | Image proxy | ✅ Running (healthy) |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | Edge Functions | ✅ Running |
| realtime | supabase/realtime:v2.68.0 | — | Realtime | ✅ Running (healthy) |
| **ollama** | ollama/ollama:latest | 11434 | LLM local | ✅ **Running** (10.6 GB image) |
| **neo4j** | neo4j:latest | 7473, 7474, 7687 | Graph DB | ✅ **Running** |

> ❌ **open-webui** — plus présent dans la stack. Le container a été retiré (le volume `local-ai-packaged_open-webui` existe encore comme résidu).

---

## 🔗 URLs Internes Docker (n8n workflows)

```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434          # ✅ réactivé
REDIS_HOST=redis:6379                    # Valkey (Redis-compatible)
NEO4J_URL=bolt://neo4j:7687              # ✅ réactivé
SEARXNG_URL=http://searxng:8081          # internal only
```

---

## 🚀 Services Bare-Metal (hors Docker)

| Service | Type | Port | Status | Notes |
|---|---|---|---|---|
| **Palanthai API** | `nohup uvicorn` (start_api.sh) | **8765** | ✅ Running (PID 776, 19h+) | **PAS systemd** — `palanthai-sync.service` est `disabled` |
| **HERMES Dashboard** | Python venv (`/home/phil/.hermes/`) | 9119 (bind 100.78.110.61) | ✅ Running | |
| **Fail2ban** | systemd | — | ✅ active | protection SSH |
| **Tailscale** | systemd | — | ✅ active | VPN mesh |
| **Syncthing** | systemd | 8384 | ❌ **inactive** | service down, dossier config présent |

### Palanthai API — Détails
- **Binaire :** `/home/phil/venv/bin/uvicorn palanthai_api:app --host 0.0.0.0 --port 8765 --reload`
- **Version :** **1.0.0** (Title: `Palanthai Local API`, 49 routes)
- **Démarrage :** `nohup …start_api.sh` (auto-restart sur modif via `--reload`)
- **Logs :** `/home/phil/palanthai/api.log` (⚠️ PAS `palanthai/logs/api.log`)
- **PID file :** `/home/phil/palanthai/api.pid` (⚠️ PAS `/home/phil/api.pid`)
- **Config :** `/home/phil/palanthai/config/.env` (20 clés : GA4, GSC, Neo4j, Qdrant, Ollama, WordPress, etc.)
- **Erreur courante observée :** `ModuleNotFoundError: No module named 'analytics'` (palanthai_api.py:539 → `seo_sync_subjects`)

### Endpoints API (49 routes, d'après `/openapi.json`)
- `/health`, `/services/health`, `/system/resources`
- `/scraper/run`, `/wf_proto/extract`, `/wf_proto/refresh_prices`, `/wf_proto/ping`, `/wf_proto/new_units`
- `/lockdown/sync/*` (6 routes), `/lockdown/sync_v2/*` (3 routes)
- `/sync/*` (6 routes), `/queue/*` (3 routes), `/units/*` (5 routes)
- `/subjects` (GET/POST), `/memory/*` (4 routes)
- `/content/*` (6 routes : atomize, embed, enrich-facts, generate, inject-links, update-faq-hub)
- `/seo/*` (5 routes : gsc-pages, keywords, pages, content-performance, sync-subjects, request-indexing)

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

# Test API health
curl -s http://31.97.67.145:8765/health

# Qdrant collections
curl -s http://31.97.67.145:6333/collections

# Fullrun progress
ssh phil@31.97.67.145 'cat /home/phil/palanthai/phase1_extraction/PIPELINE_STATE.md 2>/dev/null || ls /home/phil/palanthai/phase1_extraction/'
```

---

## 📊 État des Données (au 2026-06-01)

| Source | Volume | Notes |
|---|---|---|
| **PostgreSQL** | 2 527 MB / 145 tables public | Supabase `supabase-db` container |
| `replica_unit` | **53 301** rows | table principale des unités |
| `replica_projects_live` | **6 646** rows | projets |
| `unit_features` | 245 865 rows | features unités |
| **Qdrant `units`** | **45 039** vectors (768 dims) | status `green`, Cosine, HNSW m=16 |
| **Qdrant `units_v3`** | 200 vectors (1024 dims) | nouvelle collection, sparse + dense |
| Qdrant `projects_v3` | (collection active) | |
| Qdrant `palanthai_knowledge` | (collection active) | KB Reflexion |
| Qdrant `palanthai_memory` | (collection active) | |
| Qdrant `mem0migrations` | (collection active) | meta |

---

## 🔐 Security Summary

> Full audit: [[VPS_Security_Audit_2026-05-01]] | Full infra reference: [[VPS_INFRASTRUCTURE_REFERENCE]]

**CRITICAL credentials exposed and needing rotation:**
- VPS PostgreSQL: `xpKe3z1z8q5d1QKjx1ZZzRRgFtQlUe3K` (in `migrate_cloud_to_vps.py`, `setup_vps_neo4j.py`)
- Neo4j: `9PXofEGxRCw2O119HC3RnRUK` (in `setup_vps_neo4j.py`)
- Supabase anon key: project `owmucbudvleotyilotoq` (in `migrate_cloud_to_vps.py`)
- 15+ secrets in `local-ai-packaged/.env` (40 clés au total — N8N, Supabase, OpenRouter, Groq, Telegram, ElevenLabs, Ollama, NVIDIA, Serper, OpenClaw, INDEXNOW, QuicCloud, GA4/GSC, etc.)

**Command injection vulnerabilities:**
- `palanthai/phase1_extraction/sync_service.py` — `subprocess.run(shell=True)`
- `local-ai-packaged/start_services.py` — `subprocess.run(shell=True)`

---

*Dernière mise à jour : 2026-06-01 | Mise à jour basée sur `docker ps`, `/openapi.json`, `ps aux`, `ss -tlnp` et inspection filesystem. Supercedes old access ref — see [[VPS_INFRASTRUCTURE_REFERENCE]] for complete VPS mapping*
