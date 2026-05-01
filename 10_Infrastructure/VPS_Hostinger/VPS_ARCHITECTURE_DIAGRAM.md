---
type: infrastructure_documentation
tags: [vps, architecture, mermaid, diagram, infrastructure, docker, n8n, supabase, qdrant, neo4j, palanthai, heremes, wordpress]
updated: 2026-05-01
status: draft
---

# 🔬 VPS Architecture Diagram

> Diagramme Mermaid de l'architecture complète du VPS Hostinger.
> Voir aussi : [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_SERVICE_MAP]]

---

## Vue d'ensemble — Infrastructure Complete

```mermaid
flowchart TB
    subgraph INTERNET["🌐 Internet"]
        USER([👤 User / Agent])
    end

    subgraph VPS["🖥️ VPS Hostinger (31.97.67.145) — Ubuntu 24.04 LTS"]
        subgraph DOCKER["🐳 Docker Stack (/home/phil/local-ai-packaged/)"]
            CADDY["🟡 Caddy<br/>:80, :443<br/>Reverse Proxy + TLS"]
            N8N["⚡ n8n<br/>:5678 → https://n8n.recall-agency.com"]
            SUPABASE["📦 Supabase Stack (10 containers)"]
            SUPABASE_KONG["🔷 Kong API Gateway<br/>:8000, :8443"]
            SUPABASE_DB["🗄️ PostgreSQL<br/>:5432"]
            SUPABASE_AUTH["🔐 Gotrue Auth<br/>:5432"]
            SUPABASE_REST["📋 PostgREST<br/>:3000"]
            SUPABASE_STUDIO["🎨 Supabase Studio<br/>:3000"]
            SUPABASE_STORAGE["📁 Storage API<br/>:5000"]
            QDRANT["🔢 Qdrant<br/>:6333, :6334<br/>45k+ units, 768 dims"]
            NEO4J["🕸️ Neo4j<br/>:7474, :7687<br/>Graph DB"]
            MINIO["🪣 MinIO<br/>:9000, :9001<br/>Object Storage"]
            VALKEY["🔴 Valkey/Redis<br/>:6379<br/>Cache/Queue"]
            SEARXNG["🔍 SearXNG<br/>:8081<br/>Meta-Search"]
            OLLAMA["🤖 Ollama<br/>:11434<br/>⚠️ Exited"]
            OPENWEBUI["🌐 OpenWebUI<br/>⚠️ Exited"]

            CADDY --> N8N
            CADDY --> SUPABASE_KONG
            SUPABASE_KONG --> SUPABASE_AUTH
            SUPABASE_KONG --> SUPABASE_REST
            SUPABASE_KONG --> SUPABASE_STORAGE
            SUPABASE_KONG --> SUPABASE_DB
        end

        subgraph BARE_METAL["⚙️ Bare Metal / Systemd"]
            PALANTHAI_API["🤖 Palanthai API<br/>:8500 (HTTP)<br/>systemd/uvicorn"]
            NEXTJS["📱 Next.js (temp-app)<br/>:3000 (public)<br/>:5173 (localhost)"]
            HERMES["🔮 HERMES Agent<br/>Python venv<br/>Dashboard :9119"]
            SYNCTHING["🔄 Syncthing<br/>:8384<br/>sendonly → Mac"]
            MINIO_BIN["🪣 MinIO (binary)<br/>:9000, :9001"]
            FAIL2BAN["🛡️ Fail2ban<br/>SSH brute-force protection"]
            TAILSCALE["🌊 Tailscale<br/>VPN access"]
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
    USER -->|"HTTPS :8500 (no proxy)"| PALANTHAI_API
    USER -->|"HTTPS :3000"| NEXTJS
    USER -->|HTTPS (direct)| WP_REFLEXION
    USER -->|HTTPS (direct)| WP_RECALL
    USER -->|HTTPS (direct)| WP_PATRIMONASIA

    SYNCTHING ==>|"3600s rescan"| SYNC_PALANTHAI
    SYNCTHING ==>|"3600s rescan"| SYNC_OBSIDIAN
```

---

## Data Pipeline Flow — Scraping to WordPress

```mermaid
flowchart LR
    subgraph SCRAPING["Phase 1 — Scraping"]
        LP["LivePhuket.com"]
        SC["source_crawler.py<br/>(6 regions)"]
        WF["wf_extract/*.py<br/>(12 city/type combos)"]
        FULLRUN["fullrun/fullrun.py<br/>(JSONL batches)"]
    end

    subgraph INGESTION["Phase 2 — Ingestion"]
        INGEST["ingestor_v5.py<br/>(multi-DB)"]
        SEQUENCER["phase2/sequencer_v2.py"]
        DB["db_ingestor_units.py<br/>(Supabase upsert)"]
    end

    subgraph EXTRACTION_EMBEDDING["Phase 3 — Content & Embedding"]
        CLEAN["data_cleaner.py<br/>(brand → Reflexion)"]
        OLLAMA_EMB["embed_to_qdrant.py<br/>(Ollama → Qdrant)"]
        QDRANT_COL["🔢 Qdrant units<br/>(768 dims, ≥75 quality)"]
    end

    subgraph RAG_SERVICE["Phase 3+ — RAG"]
        PALANTHAI_API["Palanthai API<br/>:8500"]
        HERMES["HERMES Agent"]
    end

    subgraph AUTOMATION["n8n Workflows"]
        N8N_WF["n8n workflows<br/>(SEO, content, sync)"]
    end

    subgraph PUBLISHING["Phase 3+ — Publishing"]
        WP_R["🌴 reflexion.asia"]
        WP_REC["🏠 recall-agency.com"]
    end

    LP --> SC --> WF --> FULLRUN
    FULLRUN --> INGEST --> SEQUENCER --> DB
    DB --> CLEAN --> OLLAMA_EMB --> QDRANT_COL
    QDRANT_COL --> PALANTHAI_API --> HERMES
    PALANTHAI_API -->|"RAG queries"| N8N_WF
    N8N_WF -->|"SEO automation"| WP_R
    N8N_WF -->|"content generation"| WP_REC
```

---

## Docker Network — Internal Connections

```mermaid
flowchart LR
    subgraph DOCKER_NETWORK["Docker Internal Network (172.18.0.x)"]
        subgraph SUPABASE_CLUSTER["Supabase Cluster"]
            KONG["Kong :8000<br/>API Gateway"]
            DB["PostgreSQL :5432"]
            AUTH["Gotrue :5432"]
            REST["PostgREST :3000"]
            STUDIO["Studio :3000"]
            STORAGE["Storage :5000"]
            POOLER["Supavisor :5432"]
        end

        subgraph SERVICES["Services"]
            N8N["n8n :5678"]
            QDRANT["Qdrant :6333"]
            NEO4J["Neo4j :7687"]
            VALKEY["Valkey :6379"]
            MINIO["MinIO :9000"]
            SEARXNG["SearXNG :8081"]
        end

        subgraph OLLAMA_CLUSTER["Ollama (Exited)"]
            OLLAMA["Ollama :11434"]
            OPENWEBUI["OpenWebUI :8080"]
        end
    end

    KONG --> DB
    KONG --> AUTH
    KONG --> REST
    KONG --> STORAGE
    REST --> DB
    STORAGE --> DB
    N8N --> QDRANT
    N8N --> VALKEY
    N8N --> KONG
    HERMES -.->|"Python venv"| OLLAMA
```

---

## Caddy Proxy Routing

```mermaid
flowchart TB
    CADDY_FILE["📋 Caddyfile<br/>/home/phil/local-ai-packaged/Caddyfile"]

    subgraph EXPOSED["✅ Exposed via Caddy (HTTPS)"]
        N8N_ROUTE["n8n.recall-agency.com<br/>→ n8n:5678"]
        SUPABASE_ROUTE["supabase.recall-agency.com<br/>→ kong:8000"]
    end

    subgraph INTERNAL_ONLY["⚠️ Internal Only (no Caddy proxy)"]
        NEO4J_ROUTE["Neo4j Browser :7474<br/>COMMENTED OUT"]
        OLLAMA_ROUTE["Ollama :11434<br/>DISABLED"]
        SEARXNG_ROUTE["SearXNG :8081<br/>DISABLED"]
    end

    subgraph NOT_PROXIED["❌ Not via Caddy (separate infrastructure)"]
        PALANTHAI["Palanthai API :8500<br/>HTTP, no proxy"]
        WORDPRESS["WordPress sites<br/>92.113.28.34:65002<br/>Direct LiteSpeed"]
        NEXTJS_VPS["Next.js :3000<br/>Direct (internet)"]
        HERMES_DASH["HERMES Dashboard :9119<br/>Bound to 100.78.110.61"]
    end

    CADDY_FILE --> N8N_ROUTE
    CADDY_FILE --> SUPABASE_ROUTE
    CADDY_FILE -.commented.-> NEO4J_ROUTE
    CADDY_FILE -.disabled.-> OLLAMA_ROUTE
    CADDY_FILE -.disabled.-> SEARXNG_ROUTE
```

---

## Service Health Status

```mermaid
flowchart LR
    subgraph RUNNING["✅ Running / Active"]
        CADDY_R["Caddy"]
        N8N_R["n8n"]
        QDRANT_R["Qdrant"]
        NEO4J_R["Neo4j"]
        SUPABASE_ALL["Supabase (10 containers)"]
        MINIO_R["MinIO"]
        VALKEY_R["Valkey"]
        SEARXNG_R["SearXNG"]
        PALANTHAI_R["Palanthai API"]
        HERMES_R["HERMES"]
        SYNCTHING_R["Syncthing"]
        NEXTJS_R["Next.js"]
    end

    subgraph STOPPED["⚠️ Stopped / Exited"]
        OLLAMA_S["Ollama"]
        OPENWEBUI_S["OpenWebUI"]
    end

    subgraph MISSING["❌ Missing / No Backup"]
        PG_BACKUP["PostgreSQL<br/>⚠️ No pg_dump cron"]
        QDRANT_BACKUP["Qdrant<br/>⚠️ No backup"]
        NEO4J_BACKUP["Neo4j<br/>⚠️ No backup"]
        MINIO_BACKUP["MinIO<br/>⚠️ No backup"]
    end
```

---

## Ollama Decision Map

```mermaid
flowchart TD
    OLLAMA_STATUS["Ollama Docker Container<br/>⚠️ Exited (137)"]

    OLLAMA_STATUS -->|Option A| OLLAMA_RESTART["♻️ Restart Ollama<br/>Local embeddings<br/>No OpenRouter cost"]
    OLLAMA_STATUS -->|Option B| OLLAMA_STAY["☁️ Stay OpenRouter-only<br/>Current: Phase3 uses<br/>OpenRouter :free models"]

    OLLAMA_RESTART -->|" Pros"| OLLAMA_PROS["✓ Local processing<br/>✓ No API cost<br/>✓ Privacy"]
    OLLAMA_STAY -->|" Pros"| STAY_PROS["✓ Already working<br/>✓ No infra management<br/>✓ BGE-large via API"]

    OLLAMA_RESTART -->|" Cons"| OLLAMA_CONS["✗ 8GB RAM VPS<br/>✗ May OOM<br/>✗ Needs maintenance"]
    OLLAMA_STAY -->|" Cons"| STAY_CONS["✗ API costs<br/>✗ External dependency"]
```

---

## Backup Gap Analysis

```mermaid
flowchart TB
    subgraph DATASTORES["Data Stores (Production)"]
        PG["🗄️ PostgreSQL<br/>(Supabase, 45k+ units)<br/>Docker volume"]
        QDRANT_VOL["🔢 Qdrant<br/>(45k+ embeddings)<br/>Docker volume"]
        NEO4J_VOL["🕸️ Neo4j<br/>(Graph data)<br/>Docker volume"]
        MINIO_VOL["🪣 MinIO<br/>(Binary data)<br/>/data directory"]
        VALKEY_VOL["🔴 Valkey<br/>(Cache/Queue)<br/>Docker volume"]
    end

    subgraph BACKUP_STATUS["📦 Backup Status"]
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

*Dernière mise à jour : 2026-05-01*
*Voir : [[VPS_SERVICE_MAP]], [[VPS_BACKUP_INFRASTRUCTURE]], [[VPS_INFRASTRUCTURE_REFERENCE]]*