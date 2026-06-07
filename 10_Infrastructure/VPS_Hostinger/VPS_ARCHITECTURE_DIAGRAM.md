---
type: infrastructure_documentation
tags: [vps, architecture, mermaid, diagram, infrastructure, docker, n8n, supabase, qdrant, neo4j, palanthai, heremes, wordpress]
updated: 2026-06-01
status: active
---

# 🔬 VPS Architecture Diagram

> Diagramme Mermaid de l'architecture complète du VPS Hostinger (au 2026-06-01).
> Voir aussi : [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_SERVICE_MAP]], [[VPS_ACCESS_REFERENCE]]

---

## Vue d'ensemble — Infrastructure Complete

```mermaid
flowchart TB
    subgraph INTERNET["🌐 Internet"]
        USER([👤 User / Agent])
    end

    subgraph VPS["🖥️ VPS Hostinger (31.97.67.145) — Ubuntu 24.04.4 LTS"]
        subgraph DOCKER["🐳 Docker Stack (/home/phil/local-ai-packaged/) — 19 containers"]
            CADDY["🟡 Caddy<br/>:80, :443, :2019<br/>Reverse Proxy + TLS"]
            N8N["⚡ n8n<br/>n8nio/n8n:latest<br/>:5678 → https://n8n.recall-agency.com"]
            SUPABASE["📦 Supabase Stack (11 containers)"]
            SUPABASE_KONG["🔷 Kong API Gateway<br/>kong:2.8.1<br/>:8000, :8443"]
            SUPABASE_DB["🗄️ PostgreSQL<br/>15.8.1.085 — 145 tables / 2.5 GB<br/>:5432 (interne)"]
            SUPABASE_AUTH["🔐 Gotrue Auth<br/>gotrue:v2.184.0"]
            SUPABASE_REST["📋 PostgREST<br/>postgrest:v14.1<br/>:3000"]
            SUPABASE_STUDIO["🎨 Supabase Studio<br/>2025.12.17<br/>:3000"]
            SUPABASE_STORAGE["📁 Storage API<br/>v1.33.0 :5000"]
            SUPABASE_META["🧩 pg-meta<br/>v0.95.1 :8080"]
            QDRANT["🔢 Qdrant<br/>qdrant/qdrant:latest<br/>:6333, :6334<br/>units 45 039 (768d) + units_v3 200 (1024d)"]
            NEO4J["🕸️ Neo4j<br/>neo4j:latest<br/>:7473, :7474, :7687<br/>✅ ACTIF"]
            MINIO["🪣 MinIO<br/>minio/minio:latest<br/>:9000, :9001 (interne)"]
            VALKEY["🔴 Valkey/Redis<br/>valkey/valkey:8-alpine<br/>:6379"]
            SEARXNG["🔍 SearXNG<br/>searxng/searxng:latest<br/>:8081→:8080 (interne)"]
            OLLAMA["🤖 Ollama<br/>ollama/ollama:latest<br/>:11434<br/>✅ ACTIF (10.6 GB image)"]

            CADDY --> N8N
            CADDY --> SUPABASE_KONG
            CADDY --> NEO4J
            SUPABASE_KONG --> SUPABASE_AUTH
            SUPABASE_KONG --> SUPABASE_REST
            SUPABASE_KONG --> SUPABASE_STORAGE
            SUPABASE_KONG --> SUPABASE_DB
            SUPABASE_KONG --> SUPABASE_META
        end

        subgraph BARE_METAL["⚙️ Bare Metal / host network"]
            PALANTHAI_API["🤖 Palanthai API v1.0.0<br/>nohup uvicorn :8765 (--reload)<br/>49 routes — systemD disabled<br/>PID 776"]
            NEXTJS["📱 Next.js (temp-app)<br/>:3000 / :5173"]
            HERMES["🔮 HERMES Agent<br/>Python venv<br/>Dashboard :9119 (Tailscale 100.78.110.61)"]
            SYNCTHING["🔄 Syncthing<br/>:8384<br/>❌ INACTIVE"]
            FAIL2BAN["🛡️ Fail2ban<br/>✅ active"]
            TAILSCALE["🌊 Tailscale<br/>✅ active (100.78.110.61)"]
        end
    end

    subgraph WEBHOSTING["🌐 Shared Hosting (92.113.28.34) — LiteSpeed + PHP"]
        WP_REFLEXION["🌴 reflexion.asia<br/>Houzez theme<br/>RankMath SEO<br/>✅ Production"]
        WP_RECALL["🏠 recall-agency.com<br/>Astra child theme<br/>RankMath + Polylang<br/>✅ Production FR/EN"]
        WP_PATRIMONASIA["💎 patrimonasia.com<br/>❌ Not built yet<br/>En attente reflexion+recall stable"]
    end

    subgraph MAC["🍎 Mac (Local)"]
        SYNC_PALANTHAI["📁 /home/phil/palanthai<br/>sendonly ← VPS"]
        SYNC_OBSIDIAN["📁 /home/phil/obsidian-leon<br/>sendonly ← VPS"]
    end

    USER -->|HTTPS| CADDY
    USER -->|"HTTP :8765 (no proxy)"| PALANTHAI_API
    USER -->|"HTTPS :3000"| NEXTJS
    USER -->|HTTPS direct| WP_REFLEXION
    USER -->|HTTPS direct| WP_RECALL
    USER -->|HTTPS direct| WP_PATRIMONASIA
    USER -->|"Tailscale"| HERMES

    SYNCTING -.->|"sendonly (config)"| SYNC_PALANTHAI
    SYNCTING -.->|"sendonly (config)"| SYNC_OBSIDIAN
```

---

## Data Pipeline Flow — Scraping to WordPress

```mermaid
flowchart LR
    subgraph SCRAPING["Phase 1 — Scraping (/home/phil/palanthai/phase1_extraction)"]
        LP["LivePhuket.com"]
        SC["source_crawler.py<br/>(6 regions)"]
        WF["wf_extract/*.py<br/>(12 city/type combos)"]
        FULLRUN["fullrun/fullrun.py<br/>(JSONL batches)"]
        LD["RUN_LOCKDOWN/<br/>(lockdown workflow)"]
    end

    subgraph INGESTION["Phase 2 — Sync (/home/phil/palanthai/phase2_sync)"]
        WF_PROTO["wf_proto.py<br/>(24K — orchestrateur)"]
        EXTRACT["extract_one.py"]
        DB["db_io.py<br/>(Supabase upsert)"]
    end

    subgraph EXTRACTION_EMBEDDING["Phase 3 — Content & Embedding (phase3_embedding_graph)"]
        CLEAN["data_cleaner.py<br/>(brand → Reflexion)"]
        OLLAMA_EMB["embed_to_qdrant.py<br/>(Ollama → Qdrant)"]
        KAGGLE["kaggle_bge_m3.ipynb<br/>(BGE-large via Kaggle)"]
        QDRANT_COL["🔢 Qdrant units<br/>45 039 pts (768d) + units_v3 200 (1024d)"]
    end

    subgraph RAG_SERVICE["RAG / API"]
        PALANTHAI_API["🤖 Palanthai API v1.0.0<br/>nohup uvicorn :8765<br/>49 routes (/scraper /wf_proto /sync /seo /content /units /memory ...)"]
        HERMES["HERMES Agent<br/>(.hermes Python venv)"]
    end

    subgraph AUTOMATION["n8n Workflows"]
        N8N_WF["n8n :5678<br/>Local_RAG_AI_Agent.json<br/>(1 workflow actif)"]
    end

    subgraph PUBLISHING["Publishing"]
        WP_R["🌴 reflexion.asia"]
        WP_REC["🏠 recall-agency.com"]
    end

    LP --> SC --> WF --> FULLRUN
    FULLRUN --> WF_PROTO --> EXTRACT --> DB
    DB --> CLEAN --> OLLAMA_EMB --> QDRANT_COL
    KAGGLE -.->|alternative| QDRANT_COL
    QDRANT_COL --> PALANTHAI_API --> HERMES
    PALANTHAI_API -->|"RAG queries"| N8N_WF
    N8N_WF -->|"SEO automation"| WP_R
    N8N_WF -->|"content generation"| WP_REC
```

---

## Docker Network — Internal Connections

```mermaid
flowchart LR
    subgraph DOCKER_NETWORK["localai_default (172.18.0.0/16)"]
        subgraph SUPABASE_CLUSTER["Supabase Cluster (11)"]
            KONG["Kong :8000<br/>API Gateway"]
            DB["PostgreSQL :5432<br/>145 tables / 2.5 GB"]
            AUTH["Gotrue :9999"]
            REST["PostgREST :3000"]
            STUDIO["Studio :3000"]
            STORAGE["Storage :5000"]
            POOLER["Supavisor :5432 / :6543"]
            META["pg-meta :8080"]
        end

        subgraph SERVICES["Services"]
            N8N["n8n :5678"]
            QDRANT["Qdrant :6333-34"]
            NEO4J["Neo4j :7474 / :7687<br/>✅ ACTIF"]
            VALKEY["Valkey :6379"]
            MINIO["MinIO :9000-9001"]
            SEARXNG["SearXNG :8080 (interne)"]
        end

        subgraph OLLAMA_CLUSTER["Ollama (✅ ACTIF)"]
            OLLAMA["Ollama :11434<br/>10.6 GB image"]
        end
    end

    KONG --> DB
    KONG --> AUTH
    KONG --> REST
    KONG --> STORAGE
    KONG --> META
    REST --> DB
    STORAGE --> DB
    N8N --> QDRANT
    N8N --> VALKEY
    N8N --> KONG
    HERMES[".hermes Python venv"] -.->|"bolt"| NEO4J
    HERMES -.->|"http"| OLLAMA
    HERMES -.->|"http"| QDRANT
```

---

## Caddy Proxy Routing

```mermaid
flowchart TB
    CADDY_FILE["📋 Caddyfile<br/>/home/phil/local-ai-packaged/Caddyfile"]

    subgraph EXPOSED["✅ Exposed via Caddy (HTTPS)"]
        N8N_ROUTE["n8n.recall-agency.com<br/>→ n8n:5678"]
        SUPABASE_ROUTE["supabase.recall-agency.com<br/>→ kong:8000"]
        NEO4J_ROUTE["neo4j.recall-agency.com<br/>→ neo4j:7474<br/>✅ ACTIF"]
    end

    subgraph INTERNAL_ONLY["🚫 NOT via Caddy (exposed on host, no auth)"]
        OLLAMA_HOST["Ollama :11434<br/>host port direct"]
        SEARXNG_HOST["SearXNG :8081<br/>host port direct"]
        QDRANT_HOST["Qdrant :6333 / :6334"]
        NEO4J_HOST["Neo4j :7473 / :7474 / :7687<br/>host port direct"]
        PG_HOST["PostgreSQL :5432 (pooler)"]
    end

    subgraph NOT_PROXIED["❌ Not via Caddy (separate)"]
        PALANTHAI["Palanthai API :8765<br/>HTTP, no proxy, no auth"]
        WORDPRESS["WordPress sites<br/>92.113.28.34:65002<br/>Direct LiteSpeed"]
        HERMES_DASH["HERMES Dashboard :9119<br/>Bound to 100.78.110.61 (Tailscale)"]
    end

    CADDY_FILE --> N8N_ROUTE
    CADDY_FILE --> SUPABASE_ROUTE
    CADDY_FILE --> NEO4J_ROUTE
```

---

## Service Health Status (au 2026-06-01)

```mermaid
flowchart LR
    subgraph RUNNING["✅ Running / Active (Up 25 hours)"]
        CADDY_R["Caddy"]
        N8N_R["n8n"]
        QDRANT_R["Qdrant<br/>45 039 vectors"]
        NEO4J_R["Neo4j<br/>✅ réactivé"]
        SUPABASE_ALL["Supabase (11 containers)"]
        MINIO_R["MinIO"]
        VALKEY_R["Valkey"]
        SEARXNG_R["SearXNG"]
        OLLAMA_R["Ollama<br/>✅ réactivé"]
        PALANTHAI_R["Palanthai API v1.0.0<br/>PID 776 (19h+)"]
        HERMES_R["HERMES<br/>PID 968"]
        FAIL2BAN_R["Fail2ban"]
        TAILSCALE_R["Tailscale"]
    end

    subgraph STOPPED["❌ Stopped / Retiré"]
        OPENWEBUI_S["OpenWebUI<br/>container retiré de la stack"]
        SYNCTHING_S["Syncthing<br/>inactive"]
    end

    subgraph BACKUP_GAP["📦 Backup Gap — toujours critique"]
        PG_BACKUP["PostgreSQL 2.5 GB<br/>⚠️ Pas de pg_dump cron"]
        QDRANT_BACKUP["Qdrant 45k vecteurs<br/>⚠️ Pas de backup"]
        NEO4J_BACKUP["Neo4j<br/>⚠️ Pas de backup"]
        MINIO_BACKUP["MinIO<br/>⚠️ Pas de backup"]
    end
```

---

## Décision Ollama → Résolu (✅)

```mermaid
flowchart TD
    OLLAMA_NOW["Ollama Docker Container<br/>✅ Running (Up 25h, 10.6 GB)"]

    OLLAMA_NOW -->|Utilisation| OLLAMA_USE["✓ Embeddings locaux<br/>(Ollama API sur 11434)<br/>✓ n8n RAG queries<br/>✓ HERMES queries"]
    OLLAMA_NOW -->|Alternative| OPENROUTER["☁️ OpenRouter :free<br/>(utilisé par phase3 pour BGE-large)"]
    OLLAMA_NOW -->|Alternative| KAGGLE["📓 Kaggle BGE-M3<br/>(massif_embedding*.ipynb)"]
```

---

## Backup Gap Analysis (inchangé depuis 2026-05-01)

```mermaid
flowchart TB
    subgraph DATASTORES["Data Stores (Production, juin 2026)"]
        PG["🗄️ PostgreSQL<br/>(Supabase, 53 301 units + 6 646 projects)<br/>2.5 GB — Docker volume"]
        QDRANT_VOL["🔢 Qdrant<br/>(45 039 embeddings 768d + 200 v3)<br/>Docker volume"]
        NEO4J_VOL["🕸️ Neo4j<br/>(Graph data)<br/>Docker volume"]
        MINIO_VOL["🪣 MinIO<br/>(Object storage)<br/>Docker volume"]
        VALKEY_VOL["🔴 Valkey<br/>(Cache/Queue)<br/>Docker volume"]
    end

    subgraph BACKUP_STATUS["📦 Backup Status — toujours ZERO"]
        PG_NOBACKUP["❌ No pg_dump cron<br/>No offsite copy"]
        QDRANT_NOBACKUP["❌ No backup<br/>No offsite copy"]
        NEO4J_NOBACKUP["❌ No backup<br/>No offsite copy"]
        MINIO_NOBACKUP["❌ No backup<br/>No offsite copy"]
        VALKEY_NOBACKUP["⚠️ Volatile (cache)<br/>Low priority backup"]
    end

    subgraph RECOMMENDED["💡 Recommended Solution"]
        REC_PGDUMP["pg_dump cron → MinIO<br/>(local-ai-packaged)"]
        REC_RESTIC["restic to S3/MinIO<br/>(Qdrant, Neo4j volumes)"]
        REC_MINIO_BACKUP["MinIO lifecycle<br/>→ S3 or external"]
    end

    PG --> PG_NOBACKUP
    QDRANT_VOL --> QDRANT_NOBACKUP
    NEO4J_VOL --> NEO4J_NOBACKUP
    MINIO_VOL --> MINIO_NOBACKUP

    PG_NOBACKUP --> REC_PGDUMP
    QDRANT_NOBACKUP --> REC_RESTIC
    NEO4J_NOBACKUP --> REC_RESTIC
    MINIO_NOBACKUP --> REC_MINIO_BACKUP
```

---

*Dernière mise à jour : 2026-06-01 | Refresh sur base inspection live VPS*
*Voir : [[VPS_SERVICE_MAP]], [[VPS_BACKUP_INFRASTRUCTURE]], [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_ACCESS_REFERENCE]], [[Network_Architecture]]*
