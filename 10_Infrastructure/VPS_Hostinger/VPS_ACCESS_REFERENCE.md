---
type: infrastructure_reference
tags: [vps, ssh, n8n, docker, infrastructure, supabase, security, rls]
updated: 2026-05-01
status: active
---

# 🖥️ VPS Hostinger — Accès & Services

> **Note Agent IA** : Lire ce fichier en début de session pour avoir accès au VPS et connaître l'état des services. Pour la structure complète et la sécurité, voir [[VPS_INFRASTRUCTURE_REFERENCE]].

> **🔐 SECURITY ALERT (2026-05-01)**: 6 CRITICAL findings — hardcoded credentials in multiple scripts. See [[VPS_Security_Audit_2026-05-01]] and [[VPS_INFRASTRUCTURE_REFERENCE]] for full details. **Rotate all exposed credentials immediately.**

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

---

## 🐳 Services Docker Actifs

Répertoire : `/home/phil/local-ai-packaged/`

| Container | Image | Ports | Rôle | Status |
|---|---|---|---|---|
| caddy | caddy:2-alpine | 80, 443 | Reverse proxy / TLS | ✅ Running |
| qdrant | qdrant/qdrant | 6333-6334 | Vector DB | ✅ Running |
| n8n | ad20607cdd24 | 5678 → https://n8n.recall-agency.com | Automation | ✅ Running |
| minio | minio/minio | 9000-9001 | Object storage | ✅ Running |
| redis | valkey/valkey:8-alpine | 6379 | Cache / Queue | ✅ Running |
| searxng | searxng/searxng:latest | 8081 | Moteur recherche | ✅ Running |
| supabase-kong | kong:2.8.1 | 8000, 8443 | API Gateway | ✅ Running |
| supabase-db | supabase/postgres:15.8.1.085 | 5432 | Base de données | ✅ Running |
| supabase-auth | supabase/gotrue:v2.184.0 | — | Auth | ✅ Running |
| supabase-rest | postgrest/postgrest:v14.1 | 3000 | REST API | ✅ Running |
| supabase-studio | supabase/studio:2025.12.17 | 3000 | Dashboard | ✅ Running |
| supabase-storage | supabase/storage-api:v1.33.0 | 5000 | Storage | ✅ Running |
| supabase-pooler | supabase/supavisor:2.7.4 | 5432 | Pooler | ✅ Running |
| supabase-imgproxy | darthsim/imgproxy:v3.8.0 | — | Image proxy | ✅ Running |
| supabase-edge-functions | supabase/edge-runtime:v1.69.28 | — | Edge Functions | ✅ Running |
| realtime | supabase/realtime:v2.68.0 | — | Realtime | ✅ Running |
| **ollama** | ollama/ollama:latest | 11434 | LLM local | ⚠️ **Exited** |
| **open-webui** | ghcr.io/open-webui/open-webui:main | — | WebUI Ollama | ⚠️ **Exited** |
| **neo4j** | neo4j:latest | 7474, 7687 | Graph DB | ❌ **INACTIVE** |

---

## 🔗 URLs Internes Docker (n8n workflows)

```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
OLLAMA_HOST=http://ollama:11434   # ⚠️ Ollama stopped
REDIS_HOST=redis:6379             # Valkey (Redis-compatible)
NEO4J_URL=bolt://neo4j:7687      # ⚠️ Neo4j inactive
```

---

## 🚀 Services Non-Docker

| Service | Type | Port | Status |
|---|---|---|---|
| **Palanthai API** | systemd (`palanthai-sync.service`) | 8500 | ✅ Running |
| **Qdrant** | Docker | 6333 | ✅ Running |
| **n8n** | Docker | 5678 | ✅ Running |
| **PostgreSQL** | Docker (supabase-db) | 5432 | ✅ Running |

**Palanthai API** (`sync_service:app`):
- Version: 2.0.0
- Service: `palanthai-sync.service` (systemd)
- Port: 8500
- Endpoints: `/api/v1/source/projects`, `/api/v1/sync`, `/api/v1/sync/neo4j/*`
- Logs: `/home/phil/palanthai/logs/api.log`

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

## 🔐 Security Summary

> Full audit: [[VPS_Security_Audit_2026-05-01]] | Full infra reference: [[VPS_INFRASTRUCTURE_REFERENCE]]

**CRITICAL credentials exposed and needing rotation:**
- VPS PostgreSQL: `xpKe3z1z8q5d1QKjx1ZZzRRgFtQlUe3K` (in `migrate_cloud_to_vps.py`, `setup_vps_neo4j.py`)
- Neo4j: `9PXofEGxRCw2O119HC3RnRUK` (in `setup_vps_neo4j.py`)
- Supabase anon key: project `owmucbudvleotyilotoq` (in `migrate_cloud_to_vps.py`)
- 15+ secrets in `local-ai-packaged/.env`

**Command injection vulnerabilities:**
- `palanthai/phase1-project-directory/sync_service.py` — `subprocess.run(shell=True)`
- `local-ai-packaged/start_services.py` — `subprocess.run(shell=True)`

---

*Dernière mise à jour : 2026-05-01 | Supercedes old access ref — see [[VPS_INFRASTRUCTURE_REFERENCE]] for complete VPS mapping*