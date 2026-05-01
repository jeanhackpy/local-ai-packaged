# Technology Stack

**Analysis Date:** 2026-05-01

## Overview

SystemMac is an **Obsidian vault** serving as an agent orchestration hub for Thai real estate intelligence. It is not a traditional codebase - there is no `package.json` or build system. Work is done via direct file editing, SSH to VPS for Python execution, and n8n UI for workflow management.

---

## Languages

**Primary:**
- **Python 3.12** - Main scraping pipeline, Palanthai API, data processing
  - Location: VPS `/home/phil/venv/` (virtual environment)
  - Key packages: crawl4ai, playwright, psycopg2, pydantic, fastapi, uvicorn

**Secondary:**
- **TypeScript/JavaScript** - n8n workflows, Next.js applications
- **Bash** - Shell scripts for VPS management
- **SQL** - PostgreSQL schemas, Supabase queries

---

## Runtime Environments

### macOS (Local)
- **Platform:** Darwin 24.6.0 (macOS)
- **Shell:** zsh
- **Python:** Via virtual environments (`~/.venv`, `~/PythonTools/.venv`)
- **Node.js:** For Next.js applications (v16.0.10 on VPS)

### VPS (Hostinger)
- **OS:** Ubuntu 24.04 LTS
- **Plan:** KVM 2 — 2 vCPU / 8 GB RAM / 100 GB SSD
- **Python:** `/home/phil/venv/` (Python 3.12)
- **Docker:** Docker Compose stack for services

---

## Frameworks & Libraries

### Python Stack (VPS)
| Package | Version | Purpose |
|---------|---------|---------|
| FastAPI | — | Palanthai API server (port 8500) |
| Uvicorn | — | ASGI server (runs Palanthai API) |
| Playwright | — | Web scraping (LivePhuket authentication) |
| Crawl4AI | 0.7.x | Async web scraping |
| Pydantic | — | Data validation models |
| SQLModel | — | ORM for PostgreSQL |
| psycopg2 | — | PostgreSQL driver |
| Ollama | — | Local LLM inference |

### Node.js Stack
| Package | Version | Purpose |
|---------|---------|---------|
| Next.js | 16.0.10 | Temporary app on VPS (port 3000) |
| n8n | latest | Workflow automation |
| supabase | — | JS client for Supabase |

### AI/LLM Tools
| Tool | Purpose |
|------|---------|
| Claude Code | CLI agent orchestration (primary) |
| MiniMax M2.7 | High-performance model for coding |
| Gemini CLI | Research and SEO tasks |
| Ollama | Local LLM inference (currently stopped) |
| OpenRouter | Free model routing (Phase 3 embedding) |
| Groq | API inference |
| Crawl4AI | Async web scraping |

---

## Development Tools

### Local IDEs
| Tool | Purpose |
|------|---------|
| Cursor | Heavy development (TypeScript, React, Python) |
| VS Code (Kilo Code) | VS Code-based AI coding |
| Windsurf | Autonomous "Flows" workflows |
| Antigravity | Browser-based agent, web automation |

### Local CLI Tools
| Tool | Purpose |
|------|---------|
| Claude Code | Terminal orchestration, VPS maintenance |
| Gemini CLI | Research tasks (via `gemini "prompt"`) |
| Superwhisper | Local Whisper dictation |

---

## Infrastructure Services (Docker)

**Location:** `/home/phil/local-ai-packaged/`

| Service | Image | Ports | Status |
|---------|-------|-------|--------|
| Caddy | caddy:2-alpine | 80, 443 | Running |
| Qdrant | qdrant/qdrant | 6333-6334 | Running |
| n8n | ad20607cdd24 | 5678 | Running |
| Neo4j | neo4j:latest | 7474, 7687 | Running |
| Supabase DB | supabase/postgres:15.8.1.085 | 5432 | Running |
| Supabase Kong | kong:2.8.1 | 8000, 8443 | Running |
| Supabase Auth | supabase/gotrue:v2.184.0 | — | Running |
| Supabase REST | postgrest/postgrest:v14.1 | 3000 | Running |
| Supabase Studio | supabase/studio:2025.12.17 | 3000 | Running |
| Supabase Storage | supabase/storage-api:v1.33.0 | 5000 | Running |
| MinIO | minio/minio | 9000-9001 | Running |
| Valkey (Redis) | valkey/valkey:8-alpine | 6379 | Running |
| SearXNG | searxng/searxng:latest | 8081 | Running |
| Ollama | ollama/ollama:latest | 11434 | **Exited** |

---

## Configuration Files

| File | Purpose |
|------|---------|
| `/home/phil/local-ai-packaged/docker-compose.yml` | Main Docker compose |
| `/home/phil/local-ai-packaged/Caddyfile` | Reverse proxy + TLS config |
| `/home/phil/local-ai-packaged/.env` | Docker environment variables (15+ API keys) |
| `/home/phil/palanthai/config/.env` | Palanthai API config |
| `/Users/phil/Documents/Vaults/SystemMac/.env.local` | Local vault config (Stitch, Hostinger, Cloudflare API keys) |

---

## Key File Locations

**Palanthai Pipeline (VPS):**
- `/home/phil/palanthai/phase1-project-directory/` — Scraping (source_crawler.py, fullrun/)
- `/home/phil/palanthai/phase2/` — Extraction (sequencer_v2.py, unit_extractor_v2.py)
- `/home/phil/palanthai/phase3-embedding&graph/` — Embedding (embed_to_qdrant.py)
- `/home/phil/palanthai/palanthai_api.py` — FastAPI server (v2.0.0, port 8500)

**Obsidian Vaults:**
- `/Users/phil/Documents/Vaults/SystemMac/` — This vault (agent orchestration hub)
- `/Users/phil/Documents/Vaults/Palanthai/` — Palanthai project definition
- `/Users/phil/Documents/Vaults/obsidian-leon/` — Leon's research vault

---

*Stack analysis: 2026-05-01*