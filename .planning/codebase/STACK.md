# Technology Stack

**Analysis Date:** 2026-04-13

## Languages

**Primary:**
- Python 3.12.7 - Main development language for Palanthai data pipeline, scraping, embeddings
- TypeScript/JavaScript - n8n workflows, web development (Next.js mentioned for recall-agency)
- Bash - Shell scripts, automation, VPS management
- SQL - PostgreSQL queries, database operations
- Cypher - Neo4j graph queries

**Secondary:**
- HTML/CSS - WordPress themes, static content
- YAML - Configuration files (phase1_config.yaml)
- JSON - Data exchange format (JSONL for crawl outputs)

## Runtime

**Environment:**
- macOS Darwin 24.6.0 (SystemMac host) - Primary development workstation
- Ubuntu 24.04 LTS (VPS srv857744.hstgr.cloud 31.97.67.145) - Production server

**Package Managers:**
- Homebrew - macOS package management
- pyenv 2.6.17 - Python version management
- uv 0.9.21 - Fast Python virtual environments
- pipx 1.8.0 - Isolated CLI tools
- npm - Node.js package management

## Frameworks & Libraries

**Core Web & API:**
- FastAPI - Palanthai API (`palanthai_api.py`)
- Next.js - Website redesign (recall-agency-v3-redesign)
- WordPress/PHP - Shared hosting for reflexion.asia, recall-agency.com, patrimonasia.com

**Data Processing:**
- Pydantic - Data validation (unit_schema.py, data_cleaner.py)
- Pandas - Data manipulation
- SQLAlchemy - Database ORM
- LangChain - LLM orchestration and RAG

**Web Scraping:**
- Crawl4AI 0.7.x (async) - Primary web scraper
- Playwright - Browser automation for Crawl4AI
- lxml - XML/HTML parsing

**AI & ML:**
- Ollama - Local LLM runtime (llama3.2)
- Qdrant Client - Vector database client
- neo4j-driver - Neo4j graph database driver
- HuggingFace Transformers - Embeddings (all-MiniLM-L6-v2)

**Workflow Automation:**
- n8n - Workflow automation platform (VPS Docker container)

**UI & Visualization:**
- Mapbox GL JS - Interactive maps (recommended for LANNA frontend)
- MapLibre GL - Open-source map fallback
- Apache Superset - Dashboarding

## Infrastructure

**VPS (Hostinger KVM 2):**
- Location: Indonesia - Jakarta
- IP: 31.97.67.145
- Hostname: srv857744.hstgr.cloud
- Specs: 2 vCPU / 8 GB RAM / 100 GB SSD
- OS: Ubuntu 24.04 LTS
- Provider: Hostinger VPS

**Docker Stack (VPS):**
Directory: `/home/phil/local-ai-packaged/`

| Container | Image | Ports | Purpose |
|-----------|-------|-------|---------|
| n8n | n8nio/n8n:latest | 5678 | Workflow automation |
| n8n-worker | n8nio/n8n:latest | internal | Queue worker |
| caddy | caddy:2-alpine | 80, 443 | Reverse proxy/TLS |
| qdrant | qdrant/qdrant | 6333-6334 | Vector database |
| neo4j | neo4j:latest | 7474, 7687 | Graph database |
| ollama | ollama/ollama:latest | 11434 | Local LLM |
| minio | minio/minio | 9000-9001 | Object storage |
| redis | valkey/valkey | 6379 | Cache/Queue |
| searxng | searxng/searxng | 8081 | Search engine |
| supabase-kong | kong:2.8.1 | 8000, 8443 | API Gateway |
| supabase-db | supabase/postgres | 5432 | PostgreSQL database |
| supabase-auth | supabase/gotrue | - | Authentication |
| supabase-rest | postgrest | 3000 | REST API |
| supabase-studio | supabase/studio | 3000 | Dashboard |
| supabase-storage | supabase/storage-api | 5000 | File storage |
| supabase-realtime | supabase/realtime | - | Realtime subscriptions |

**Shared Hosting (WordPress):**
- Host: 92.113.28.34 port 65002
- Sites: reflexion.asia, recall-agency.com, patrimonasia.com

## Development Tools

**IDEs:**
- Cursor - Primary agentic coding assistant (`~/.cursor/`)
- VS Code - General development
- Antigravity - Google agentic IDE (`~/.gemini/antigravity/`)
- OpenCode - Alternative AI IDE
- Claude Code - Anthropic agentic CLI

**AI Agents:**
- Claude Code CLI - Anthropic agentic coding
- Gemini CLI - Google agentic CLI
- Antigravity - Google agentic IDE with skills

**CLI Tools:**
- Raycast - Primary launcher (macOS)
- Warp - Terminal with voice input
- SSH - Remote access
- WP-CLI - WordPress command line

## Configuration Files

**Local Environment:**
- `/Users/phil/Documents/Vaults/SystemMac/.env.local` - API keys (Stitch, Hostinger, Cloudflare)

**VPS Environment:**
- `/home/phil/palanthai/config/.env` - Database connections (PG, Qdrant, Neo4j, Ollama)
- `/home/phil/local-ai-packaged/.env` - OpenRouter, Telegram, n8n, Supabase URLs

**Project Configuration:**
- `Palanthai/phase1_config.yaml` - Pipeline configuration
- `Palanthai/requirements.txt` - Python dependencies

## Key Dependencies (Python)

**Scraping:**
- crawl4ai>=0.7.0
- playwright
- lxml

**Data:**
- pydantic
- pandas
- sqlalchemy
- python-dotenv

**AI/RAG:**
- qdrant-client
- neo4j
- langchain
- langchain-community
- httpx

**Embedding:**
- sentence-transformers (all-MiniLM-L6-v2)
- nomic-embed-text (Ollama)

## Platform Requirements

**Development:**
- macOS (Darwin) with Homebrew
- Python 3.12+ via pyenv
- Node.js/npm for n8n extensions
- SSH key authentication configured

**Production (VPS):**
- Ubuntu 24.04 LTS
- Docker and Docker Compose
- 8GB RAM minimum
- SSH access with key-based auth

---

*Stack analysis: 2026-04-13*
