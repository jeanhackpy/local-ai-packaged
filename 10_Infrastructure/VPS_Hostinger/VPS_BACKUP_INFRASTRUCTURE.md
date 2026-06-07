---
type: infrastructure_documentation
tags: [vps, backup, postgresql, b2, backblaze, n8n, supabase, rclone, critical, migration]
updated: 2026-06-01
status: active
---

# 💾 VPS Backup Infrastructure — État Réel

> **État vérifié au 2026-06-01** : la situation est meilleure que la doc d'origine ne le disait — un backup DB quotidien tourne depuis fin mai 2026 vers Backblaze B2. Reste des gaps (Qdrant / Neo4j / MinIO / TLS).
> See also : [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_SERVICE_MAP]]

---

## ✅ Ce qui EST sauvegardé (au 2026-06-01)

### 1. PostgreSQL (DB complète) — **FONCTIONNEL**

| Élément | Valeur |
|---|---|
| Cron | `0 3 * * * /home/phil/palanthai/scripts/backup_db.sh daily` |
| Fréquence | Quotidien, 03:00 UTC (= 10:00 Bangkok) |
| Méthode | `docker exec supabase-db pg_dump -Fc --no-owner --no-privileges` |
| Destination locale | `/home/phil/palanthai/phase1_extraction/backups/db/` (~5 GB cumulés, rotation 30j) |
| Destination schema | `/home/phil/palanthai/phase1_extraction/backups/schema/` (rotation 90j) |
| **Offsite** | **Backblaze B2** `b2-palanthai:palanthai-backups/` (PERMANENT) |
| Outil offsite | rclone (`/usr/bin/rclone`) |
| Compte B2 | `c8c977ff7e38` (config dans `~/.config/rclone/rclone.conf`, chmod 600) |
| Taille dump | ~323 MB compressé (-Fc) |
| Taille schema | ~464 KB plain SQL |
| Dernier run | **2026-06-01 03:01 UTC** ✅ — `palanthai_20260531_200001.dump` (323 MiB, 41.9s upload) |
| Logs | `/home/phil/palanthai/phase1_extraction/backups/logs/backup.log` |
| Restore | `rclone copy b2-palanthai:palanthai-backups/db/palanthai_YYYYMMDD_HHMMSS.dump ./` puis `docker exec -i supabase-db pg_restore -U postgres -d postgres --clean --if-exists < dump` |

> **Note importante :** n8n stocke ses workflows + credentials dans **cette même base PostgreSQL** (variable `DB_TYPE=postgresdb`, `DB_POSTGRESDB_DATABASE=postgres`). Donc le pg_dump quotidien couvre **aussi n8n**. La clé de chiffrement n8n (`N8N_ENCRYPTION_KEY`) doit être préservée séparément (cf. § secrets).

### 2. Code + configs (Git) — **FONCTIONNEL**

| Repo | Couverture |
|---|---|
| `jeanhackpy/palanthai` (VPS) | code, scripts, schemas SQL, `phase1_extraction/backups/schema/` |
| `jeanhackpy/local-ai-packaged` (VPS) | docker-compose + overrides, Caddyfile, n8n/workflows/ (1 actif), shared/pipelines, neo4j/config, searxng |
| `jeanhackpy/obsidian-leon` (VPS) | KB, scripts, n8n workflow docs |
| `jeanhackpy/obsidian-systemmac` (Mac) | ce vault Obsidian (auto-backup cron) |

### 3. Backups de workflows n8n (export JSON) — **PARTIELLEMENT**

| Localisation | Contenu | Statut |
|---|---|---|
| `/home/phil/local-ai-packaged/n8n/workflows/` | `Local_RAG_AI_Agent_n8n_Workflow.json` (1 actif, **tracké dans git**) | ✅ git |
| `/home/phil/local-ai-packaged/n8n/backup/` | WF-002/003/004/006.json (exports ponctuels Mars 2026) | ⚠️ gitignored (`.bak`) |
| `/home/phil/local-ai-packaged/n8n/backup/workflows/` | V1/V2/V3_RAG, SEO_Article, palanthai/WF-002..009 | ⚠️ gitignored |
| **n8n container `/home/node/.n8n/`** | `all_workflows.json` (186K), `chk_*.json`, `n8nEventLog-*.log` | ✅ couvert par pg_dump (n8n DB = PostgreSQL) |
| `obsidian-leon/n8n/` | docs markdown des workflows (WF-002..009) | ✅ git |

> ⚠️ Les **credentials n8n** (clés API des nodes HTTP, mots de passe, tokens Telegram, etc.) sont **chiffrés au repos** dans la DB PostgreSQL via `N8N_ENCRYPTION_KEY`. Sans cette clé, on peut pas les déchiffrer. **Elle est dans `.env` gitignored** (cf. § secrets).

---

## ❌ Ce qui N'EST PAS sauvegardé (gaps critiques)

| Data store | Volume | Raison | Priorité |
|---|---|---|---|
| **Qdrant** (vecteurs 768d) | 45 039 + 200 vectors | Pas de snapshot, pas de cron | **CRITICAL** — c'est toute la mémoire RAG |
| **Neo4j** (graphe) | inconnu | Bind-mount `/home/phil/local-ai-packaged/neo4j/data/` (gitignored) | HIGH |
| **MinIO** (object storage) | inconnu | Bind-mount `/home/phil/local-ai-packaged/minio_storage` (volume) | MEDIUM (semble peu utilisé) |
| **Caddy TLS certs** | Let's Encrypt | Caddy les regenère auto si DNS/hostname OK | LOW (auto-recover) |
| **Ollama models** (10.6 GB) | Pull manuel | Doit être re-pull sur nouveau VPS (cf. migration) | INFO |
| **Valkey/Redis** | cache/queue | Volatile par design | LOW (pas besoin) |
| **Palanthai venv Python** | 6.2 GB | Re-installable via `requirements.lock.txt` | INFO |
| **Palanthai extracted data** | `phase1_extraction/backups/extracted/{projects,units}/` (221+1176 fichiers) | gitignored localement, **pas envoyé sur B2** | HIGH — c'est la moisson scraper |

---

## 🔐 Secrets critiques à préserver

**TOUT est dans `local-ai-packaged/.env` (gitignored) + `palanthai/config/.env` (gitignored) + `~/.config/rclone/rclone.conf` (chmod 600).**

### Tier 1 — Perte = perte de fonctionnalité

| Secret | Fichier | Valeur exemple (à regenerer) |
|---|---|---|
| `N8N_ENCRYPTION_KEY` | `local-ai-packaged/.env` | `de9fe4df000a46095e53234e82d28b9a10ac54669f017617f5493de44da5b38b` (GARDER — sinon credentials n8n illisibles) |
| `N8N_USER_MANAGEMENT_JWT_SECRET` | `local-ai-packaged/.env` | `449989224edbbe402784d90b1870cd9bb3031174197f5f8fde6a77ec5443f8a1` (GARDER) |
| `POSTGRES_PASSWORD` | `local-ai-packaged/.env` + `supabase/docker/.env` | (GARDER — utilisé par n8n, supabase, palanthai) |
| `SERVICE_ROLE_KEY` | `local-ai-packaged/.env` | (GARDER) |
| `ANON_KEY` | `local-ai-packaged/.env` | (GARDER) |
| `JWT_SECRET` | `local-ai-packaged/.env` | (GARDER) |
| `SECRET_KEY_BASE` | `supabase/docker/.env` | (GARDER) |
| `DASHBOARD_PASSWORD` | `local-ai-packaged/.env` | (GARDER — accès Supabase Studio) |
| `VAULT_ENC_KEY` | `supabase/docker/.env` | (GARDER) |
| `PG_META_CRYPTO_KEY` | `supabase/docker/.env` | (GARDER) |
| `NEO4J_AUTH` | `local-ai-packaged/.env` | (GARDER — neo4j user/pass) |
| `NEO4J_PASSWORD` | `palanthai/config/.env` | (GARDER) |
| `MINIO_ROOT_PASSWORD` | `local-ai-packaged/.env` | (GARDER) |
| `WP_RECALL_PASS`, `WP_REFLEXION_PASS` | `palanthai/config/.env` | (GARDER) |
| `GOOGLE_SERVICE_ACCOUNT` | `palanthai/config/.env` (path) + JSON file | (GARDER) |

### Tier 2 — Clés API externes (peuvent être regenerables)

`OPENROUTER_API_KEY`, `GROQ_API_KEY`, `TELEGRAM_BOT_TOKEN`, `ELEVENLABS_API_KEY`, `OLLAMA_CLOUD_URL`, `OLLAMA_API_KEY`, `NVIDIA_API_KEY`, `CODEX_NVIDIA_API_KEY`, `SERPER_API_KEY`, `OPENCLAW_GATEWAY_TOKEN`, `INDEXNOW_KEY`, `QUIC_CLOUD_API_KEY`, `GA4_PROPERTY_*`, `GSC_SITE_*`, `SLACK_API_TOKEN`

### Tier 3 — Backblaze B2 (pour B2 lui-même !)

`~/.config/rclone/rclone.conf` :
```
[b2-palanthai]
type = b2
account = c8c977ff7e38
key = 0035d8a63a2ce193f09f960a36ea91262c35afb787
```
**À BACKUPER aussi** sinon on perd l'accès au B2 depuis le nouveau VPS.

### Tier 4 — Caddy TLS

Certificats Let's Encrypt stockés dans volume `local-ai-packaged_caddy-data`. Si hostname identique → Caddy les regen auto. Si hostname/IP change → manuel via `docker exec caddy caddy reload`.

---

## 📁 Inventaire complet des emplacements de sauvegarde

| Quoi | Où | Git? | B2? |
|---|---|---|---|
| Code palanthai | `/home/phil/palanthai/` | ✅ | ❌ |
| Code local-ai-packaged | `/home/phil/local-ai-packaged/` | ✅ | ❌ |
| Code obsidian-leon | `/home/phil/obsidian-leon/` | ✅ | ❌ |
| Vault SystemMac | `/Users/phil/Documents/FAKTORY/SystemMac/` | ✅ | ❌ |
| **DB dumps quotidiens** | `/home/phil/palanthai/phase1_extraction/backups/db/` | ❌ (gitignored) | ✅ **B2 PERMANENT** |
| **Schemas SQL** | `/home/phil/palanthai/phase1_extraction/backups/schema/` | ✅ trackés | ✅ B2 |
| **Logs backup** | `/home/phil/palanthai/phase1_extraction/backups/logs/backup.log` | ❌ | ❌ |
| Données extraites (projets/units) | `/home/phil/palanthai/phase1_extraction/backups/extracted/{projects,units}/` (221+1176) | ❌ (gitignored) | ❌ **GAP** |
| n8n workflow actif | `local-ai-packaged/n8n/workflows/Local_RAG_AI_Agent_n8n_Workflow.json` | ✅ | ❌ |
| n8n credentials (chiffrés) | DB PostgreSQL (`n8n` schema) | ❌ | ✅ (via pg_dump) |
| n8n encryption key | `local-ai-packaged/.env` | ❌ | ❌ **manuel** |
| Anciens exports n8n (JSON) | `local-ai-packaged/n8n/backup/{,workflows/}` | ❌ (gitignored) | ❌ |
| n8n event logs | container `/home/node/.n8n/n8nEventLog-*.log` | ❌ | ❌ |
| Qdrant (vecteurs) | volume `local-ai-packaged_qdrant_storage` | ❌ | ❌ **GAP** |
| Neo4j (graphe) | bind-mount `local-ai-packaged/neo4j/data/` | ❌ (gitignored) | ❌ **GAP** |
| MinIO data | volume `local-ai-packaged_minio_storage` | ❌ | ❌ **GAP** |
| Caddy TLS certs | volume `local-ai-packaged_caddy-data` | ❌ | ❌ (auto-regen) |
| Ollama models | volume `localai_ollama_storage` | ❌ | ❌ (re-pull) |
| Hermes state | `/home/phil/.hermes/` | ❌ (gitignored) | ❌ |
| rclone config | `/home/phil/.config/rclone/rclone.conf` (chmod 600) | ❌ | ❌ **manuel** |
| Python venv | `/home/phil/venv/` (6.2 GB) | ❌ | ❌ (re-install) |
| Playwright Python venv | `/home/phil/venv-playwright/` (153 MB) | ❌ | ❌ (re-install) |

---

## 🚨 Actions immédiates avant migration (Hostinger → Oracle Cloud)

### À faire MAINTENANT (avant que le VPS meure)

1. **Sauvegarder le `.env` complet** dans un endroit sûr (1Password, B2 privé, vault chiffré) :
   ```bash
   mkdir -p ~/migration-2026-06-01 && cd ~/migration-2026-06-01
   scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env ./local-ai.env
   scp phil@31.97.67.145:/home/phil/palanthai/config/.env ./palanthai.env
   scp phil@31.97.67.145:/home/phil/.config/rclone/rclone.conf ./rclone.conf
   scp phil@31.97.67.145:/home/phil/palanthai/config/google_service_account.json ./
   scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env.example ./
   ```

2. **⏭️ Qdrant + Neo4j** — **PAS de backup** (rebuild from scratch sur nouveau VPS avec meilleur pipeline)

3. **Palanthai extracted data** (221+1176 fichiers JSON) — **À GARDER** (le scraping prend du temps) :
   ```bash
   rsync -avz --progress phil@31.97.67.145:/home/phil/palanthai/phase1_extraction/backups/extracted/ \
     ~/migration-2026-06-01/extracted/
   ```

4. **MinIO data** : à évaluer (probablement peu utilisé — `mc ls local/` pour vérifier)

5. **Forcer un dernier backup DB** avant la migration :
   ```bash
   ssh phil@31.97.67.145 'bash /home/phil/palanthai/scripts/backup_db.sh daily'
   ssh phil@31.97.67.145 'tail -5 /home/phil/palanthai/phase1_extraction/backups/logs/backup.log'
   ```

6. **Puller un dump B2 frais en local** (backup de sécurité) :
   ```bash
   brew install rclone  # sur Mac, si pas déjà fait
   rclone lsd b2-palanthai:palanthai-backups/
   rclone copy b2-palanthai:palanthai-backups/db/ ~/migration-2026-06-01/db-dumps/ --progress
   ```

---

## 📊 Backup Verification Checklist

- [x] pg_dump crée un fichier SQL valide (testé quotidien)
- [x] pg_dump upload B2 sans erreur (testé quotidien)
- [x] Schema tracké dans git
- [x] Cron job tourne à l'heure prévue (03:00 UTC)
- [ ] **`.env` complet transféré de manière sécurisée** ← À FAIRE
- [ ] **rclone config transféré** ← À FAIRE
- [ ] **Palanthai extracted data sauvegardé** ← À FAIRE
- [ ] **MinIO data exporté** (si utilisé) ← À vérifier
- [ ] **Dump B2 frais en local** ← À FAIRE
- [ ] ~~Qdrant snapshots créés~~ ← **SKIP** (rebuild from scratch)
- [ ] ~~Neo4j dump créé~~ ← **SKIP** (rebuild from scratch)
- [ ] Alert Telegram en cas d'échec backup (optionnel, à ajouter sur nouveau VPS)

---

## 🆕 Stratégie de reconstruction post-migration (Qdrant + Neo4j)

Une fois sur le nouveau VPS Oracle Cloud Singapore, Phil va reconstruire :

### Qdrant — Nouvel embedding
- **Modèles candidats** : BGE-M3 (1024d, multilingue), E5-large-v2, ou un modèle custom via Ollama
- **Source** : `replica_unit` (53 301) + `replica_projects_live` (6 646) + `unit_features` (245 865)
- **Pipeline cible** : crawl4ai (Docker) → Playwright (Docker) → extraction → embed → Qdrant
- **Avantages 24 GB RAM** : possibilité de charger des modèles plus gros en parallèle
- **Coût estimé** : 30-90 min de calcul pour re-embed toutes les units

### Neo4j — Nouveau graph
- **Schéma cible** : à redéfinir (Phil a noté "meilleur résultat" — probablement restructurer les nodes/relationships)
- **Source** : même base PG (units + projects + features + métadonnées géographiques)
- **Outils** : même stack (langchain, ou driver Neo4j direct via API Python)
- **Avantage migration** : repartir d'un graph propre sans dette technique

### Ordre recommandé sur le nouveau VPS
1. PostgreSQL restauré depuis B2 ✅
2. Qdrant démarré (vide)
3. Neo4j démarré (vide)
4. Pipeline extraction/scraping : crawl4ai + Playwright
5. Pipeline embedding → Qdrant
6. Pipeline graph → Neo4j
7. Validation (counts, sanity checks, RAG test)

---

*Dernière mise à jour : 2026-06-01 | Doc réécrite après découverte de backup_db.sh + rclone B2 déjà en place depuis le 22 mai 2026.*
*Voir : [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_SERVICE_MAP]], [[MIGRATION_RUNBOOK_2026-06-01]]*
