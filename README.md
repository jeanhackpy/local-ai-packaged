# Palanthai — Local AI Stack

Self-hosted AI infrastructure for Thai real estate intelligence.
Forked from [coleam00/local-ai-packaged](https://github.com/coleam00/local-ai-packaged).

**Last updated:** 2026-03-26

## Active Services

| Service | Container | Port | Purpose |
|---------|-----------|------|---------|
| **Caddy** | caddy | 80, 443 | TLS reverse proxy (Let's Encrypt) |
| **n8n** | n8n | 5678 | Workflow automation |
| **Ollama** | ollama | 11434 | Local LLM inference (CPU) |
| **Qdrant** | qdrant | 6333, 6334 | Vector search |
| **Neo4j** | neo4j | 7474, 7687 | Graph database |
| **Redis** | redis (Valkey) | 6379 | Cache / queue (LRU, no persistence) |
| **MinIO** | minio | 9000, 9001 | S3-compatible object storage |
| **SearXNG** | searxng | 8081 | Meta search engine |
| **Supabase** | supabase-* | 5432, 6543, 8000 | PostgreSQL + Auth + Storage + API |

### External Services (not in Docker)
| Service | Port | Notes |
|---------|------|-------|
| OpenClaw Gateway | 18789 | MCP gateway (loopback only) |
| palanthai_api.py | 8765 | Custom FastAPI (systemd/cron) |
| Langfuse | — | Cloud-hosted at us.cloud.langfuse.com |

### Removed Services
| Service | Date | Reason |
|---------|------|--------|
| OpenWebUI | 2026-03-26 | High RAM (1GB), unused |
| Flowise | — | Never deployed in this fork |

## Commands

```bash
# SSH to VPS
ssh phil@31.97.67.145
cd /home/phil/local-ai-packaged

# ── Stack lifecycle ──────────────────────────────────────

# Stop all services
docker compose -p localai -f docker-compose.yml --profile cpu down

# Pull latest images
docker compose -p localai -f docker-compose.yml --profile cpu pull

# Start all services (Supabase first, then AI stack)
python3 start_services.py --profile cpu

# Start Caddy (scaled to 0 by start_services.py)
docker compose -p localai --profile cpu \
  -f docker-compose.yml \
  -f docker-compose.override.private.yml \
  up -d caddy

# ── Ollama model management ─────────────────────────────
# Auto-pull DISABLED — manage models manually:
docker exec ollama ollama list           # List installed models
docker exec ollama ollama pull <model>   # Download a model
docker exec ollama ollama rm <model>     # Remove a model

# Current models: nomic-embed-text (embeddings)

# ── Monitoring ───────────────────────────────────────────
docker stats --no-stream                 # CPU/RAM per container
docker logs -f <container>               # Follow logs
docker ps -a                             # Container statuses

# ── Caddy ────────────────────────────────────────────────
docker exec caddy caddy reload --config /etc/caddy/Caddyfile
```

## Architecture

### Proxy Chain
```
Internet ─→ Caddy (TLS on 80/443)
               ├─→ n8n.recall-agency.com      → n8n:5678
               ├─→ {SUPABASE_HOSTNAME}        → kong:8000 → Supabase services
               └─→ {NEO4J_HOSTNAME}           → neo4j:7474
```

### Kong (Supabase API Gateway)
Kong routes all Supabase sub-services internally:
```
/rest/v1/*      → PostgREST (supabase-rest:3000)
/auth/v1/*      → GoTrue (supabase-auth:9999)
/storage/v1/*   → Storage (supabase-storage:5000)
/realtime/v1/*  → Realtime (supabase-realtime:4000)
/functions/v1/* → Edge Functions (supabase-edge-functions:9000)
/pg/*           → pg-meta (supabase-meta:8080) [admin only]
/               → Studio (supabase-studio:3000) [basic-auth]
```

### Network
All containers run on the unified `localai_default` Docker bridge network.
Project name: `localai`.

### Memory Allocations
| Service | Limit | Notes |
|---------|-------|-------|
| Ollama | 2.5 GB | CPU capped at 1.5 cores |
| Neo4j | 1 GB | heap 256m + pagecache 64m |
| n8n | 700 MB | |
| Qdrant | 512 MB | |
| Redis | 300 MB | maxmemory 256MB LRU |
| SearXNG | 256 MB | |
| MinIO | 256 MB | |
| Caddy | 128 MB | actual ~16MB |

### DNS / Domains
| Domain | Target |
|--------|--------|
| n8n.recall-agency.com | n8n:5678 via Caddy |

## Configuration Files
```
docker-compose.yml                   # Main service definitions
docker-compose.override.private.yml  # Memory limits, ports, CPU caps
.env                                 # Secrets, domain config
Caddyfile                            # Reverse proxy routes
neo4j/config/neo4j.conf              # Neo4j memory settings
supabase/docker/docker-compose.yml   # Supabase sub-services
supabase/docker/volumes/api/kong.yml # Kong API gateway config
```
