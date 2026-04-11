---
type: infrastructure_reference
tags: [vps, ssh, n8n, docker, infrastructure, supabase, security, rls]
updated: 2026-04-03
status: active
---

# 🖥️ VPS Hostinger — Référence Accès & Services

> **Note Agent IA** : Lire ce fichier en début de session pour avoir accès au VPS et connaître l'état des services. Connexion SSH via `osascript` shell depuis le Mac.

> **🔐 SECURITY UPDATE (2026-04-03)**: Row-Level Security now ENABLED on core Palanthai tables. See [[SUPABASE_RLS_AUDIT_2026-04-03]] for complete audit report.

---

## 🔑 Accès SSH

```bash
# Connexion directe (clé configurée dans ~/.ssh/config)
ssh phil@31.97.67.145

# Commande complète explicite
ssh -i ~/.ssh/id_ed25519 phil@31.97.67.145

# Via hostname
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
| *(Supabase désactivé)* | supabase.recall-agency.com |

---

## 🐳 Services Docker Actifs

Répertoire : `/home/phil/local-ai-packaged/`
Stack base : coleam00/local-ai-packaged

| Container | Image | Ports | Rôle |
|---|---|---|---|
| n8n | n8nio/n8n:latest | 5678 → https://n8n.recall-agency.com | Automation |
| n8n-worker | n8nio/n8n:latest | 5678 (interne) | Worker queue |
| caddy | caddy:2-alpine | 80, 443 | Reverse proxy / TLS |
| qdrant | qdrant/qdrant | 6333-6334 | Vector DB |
| neo4j | neo4j:latest | 7474, 7687 | Graph DB |
| ollama | ollama/ollama:latest | 11434 | LLM local |
| minio | minio/minio | 9000-9001 | Object storage |
| redis | valkey/valkey | 6379 | Cache / Queue |
| searxng | searxng/searxng | 8081 | Moteur recherche |
| supabase-kong | kong:2.8.1 | 8000, 8443 | API Gateway Supabase |
| supabase-db | supabase/postgres | 5432 | Base de données |
| supabase-auth | supabase/gotrue | — | Auth |
| supabase-rest | postgrest | 3000 | REST API |
| supabase-studio | supabase/studio | 3000 | Dashboard Supabase |
| supabase-storage | supabase/storage-api | 5000 | Storage |
| supabase-realtime | supabase/realtime | — | Realtime |

---

## 🔗 URLs Internes Docker (à utiliser dans les workflows n8n)

```env
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
NEO4J_URL=bolt://neo4j:7687
OLLAMA_HOST=http://ollama:11434
CRAWL4AI_URL=http://crawl4ai:11235
REDIS_HOST=redis:6379
```

---

## ⚙️ Workflows n8n Existants

Répertoire : `/home/phil/local-ai-packaged/n8n/`

### 🟢 Actifs / En production
| Fichier | Fonction |
|---|---|
| `SEO_Article_Monitoring_Generation.json` | SEO auto : GSC + GA4 → Ollama → WordPress (reflexion.asia + recall-agency.com) |
| `V1_Local_RAG_AI_Agent.json` | RAG local (Ollama + Qdrant) |
| `V2_Local_Supabase_RAG_AI_Agent.json` | RAG avec Supabase |
| `V3_Local_Agentic_RAG_AI_Agent.json` | RAG agentique |

### 📦 Backup
WF-002, WF-003, WF-004, WF-006

### 🔜 À créer
- **Social Media Workflow** — Multi-brand (REcall, REflexion, PatrimoinAsia, JP) avec Airtable comme hub

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

# Editer .env
ssh phil@31.97.67.145 'nano /home/phil/local-ai-packaged/.env'
```

---

## 📁 Structure Fichiers VPS

```
/home/phil/local-ai-packaged/
├── docker-compose.yml
├── docker-compose.override.public.yml
├── docker-compose.override.private.yml
├── .env                    ← Variables d'env (N8N_HOSTNAME, SECRETS...)
├── Caddyfile               ← Config reverse proxy
├── n8n/
│   ├── workflows/          ← Workflows actifs
│   ├── backup/             ← Backups WF-002..006
│   └── SEO_Workflow_Setup.md
├── supabase/
├── neo4j/
└── scripts/
```

---

*Dernière mise à jour : 2026-03-30 | Par : Claude (session Cowork)*
