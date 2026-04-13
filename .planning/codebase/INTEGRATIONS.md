# External Integrations

**Analysis Date:** 2026-04-13

## APIs & External Services

**AI & LLM Providers:**
- **OpenRouter** - API-based LLM calls with free tier routing
  - SDK: `httpx` with custom `model_config.py`
  - Auth: API key stored in VPS `.env`
  - Models: `google/gemini-2.0-flash-exp:free`, `qwen/qwen-2.5-72b-instruct:free`, `deepseek/deepseek-chat-v3-0324:free`, `meta-llama/llama-3.1-8b-instruct:free`
  - Rate limits: 20 req/min, 1000 req/day
  - Location: `/home/phil/palanthai/content/model_config.py`

- **Ollama** - Local LLM runtime (Docker container on VPS)
  - Endpoint: `http://ollama:11434` (internal), accessible via `http://31.97.67.145:11434`
  - Models: llama3.2, nomic-embed-text (for embeddings)
  - Location: Docker container `ollama` in `/home/phil/local-ai-packaged/`

- **Claude API** - Anthropic LLM (mentioned for GARUDA module)
  - Auth: API key in configuration

**Search & Scraping:**
- **Crawl4AI** - Web scraping framework
  - Version: 0.7.x (async)
  - Environment: `~/PythonTools/.venv`
  - Uses Playwright chromium
  - Location: `/home/phil/Documents/Vaults/SystemMac/00_System/Scripts/crawl_test.py`

- **LivePhuket.com** - Primary scraping source
  - Data: Property projects, developers, pricing
  - Extraction: JSON-LD Schema.org data

- **FazWaz.com** - Secondary data source
  - Data: FAQ articles for RAG knowledge base

- **SET Thailand** - Stock exchange data
  - Endpoint: `https://www.set.or.th/en/market/index/set/propcon/prop`
  - Data: Market cap, P/E ratios, dividends for property companies

## Data Storage

**PostgreSQL (Supabase):**
- Type: Relational database (Supabase self-hosted)
- Connection: `postgresql://postgres:[password]@supabase-db:5432/postgres`
- Client: SQLAlchemy, psycopg2
- Port: 5432 (internal Docker)
- Location: Docker container `supabase-db`
- Schema: Tables for `developer`, `project`, `listing`, `faq_article`, `market_data`
- RLS: Row-Level Security enabled on core Palanthai tables

**Qdrant (Vector Database):**
- Type: Vector store for semantic search and RAG
- Connection: `http://qdrant:6333` (internal), `http://31.97.67.145:6333` (external)
- Client: `qdrant-client` Python library
- Collections:
  - `palanthai_knowledge` (768-dim, nomic-embed-text)
  - `projects` (384-dim, all-MiniLM-L6-v2)
  - `faq_knowledge` (384-dim)
- Port: 6333 (REST API), 6334 (gRPC)

**Neo4j (Graph Database):**
- Type: Knowledge graph for entity relationships
- Connection: `bolt://neo4j:7687` (internal)
- Client: `neo4j-driver` Python library
- UI: `http://31.97.67.145:7474` (Browser)
- Nodes: `:Project`, `:Developer`, `:Location`, `:Facility`, `:PropertyType`, `:MarketSector`
- Relationships: `DEVELOPED_BY`, `LOCATED_IN`, `HAS_FACILITY`, `IS_TYPE`, `LISTED_ON`

**Redis/Valkey:**
- Type: Cache and queue
- Connection: `redis:6379` (internal)
- Purpose: n8n queue worker, caching

**MinIO (Object Storage):**
- Type: S3-compatible object storage
- Connection: `minio:9000` (internal)
- Console: `minio:9001`
- Purpose: File storage (Supabase storage backend)

## Authentication & Identity

**Supabase Auth:**
- Type: Supabase Gotrue (self-hosted)
- Container: `supabase-auth`
- Purpose: User authentication for Palanthai applications
- RLS: Row-Level Security policies enforce access control

**SSH Keys:**
- Key type: Ed25519
- Location: `~/.ssh/id_ed25519`
- Usage: VPS access, GitHub, shared hosting

**API Keys (`.env.local`):**
- `STITCH_API_KEY` - Stitch service
- `HOSTINGER_API_KEY` - Hostinger cloud management
- `CLOUDFLARE_API_TOKEN` / `CLOUDFLARE_API_TOKEN_2` - DNS and CDN
- `HOSTINGER_FIREWALL_KEY` - Firewall management

## Monitoring & Observability

**Error Tracking:**
- No dedicated error tracking service detected
- Logs stored in various locations:
  - n8n logs: `docker logs n8n --tail 50`
  - Palanthai logs: `/home/phil/palanthai/phase2/logs/sequencer_v2_*.log`
  - WordPress debug: `wp-content/debug.log`

**System Monitoring:**
- Hostinger hPanel - VPS management dashboard
- Docker stats: `docker ps --format "{{.Names}}: {{.Status}}"`
- Custom monitoring script: `/Users/phil/Documents/AppsData/AgentManager_Cursor/monitor.py`

**Uptime Monitoring:**
- n8n accessible at: https://n8n.recall-agency.com
- Paperclip accessible at: https://paperclip.recall-agency.com

## CI/CD & Deployment

**Hosting:**
- **VPS**: Hostinger KVM 2 at 31.97.67.145 (Docker-based deployment)
- **Shared Hosting**: Hostinger shared plans at 92.113.28.34:65002
- **WordPress Sites**: reflexion.asia, recall-agency.com, patrimonasia.com

**Docker Compose:**
- Main stack: `/home/phil/local-ai-packaged/docker-compose.yml`
- Override files: `docker-compose.override.public.yml`, `docker-compose.override.private.yml`

**Version Control:**
- Git repositories in:
  - `/Users/phil/Documents/Vaults/SystemMac/` (this vault)
  - `/Users/phil/Documents/Vaults/Palanthai/` (Palanthai platform)
  - Palanthai on VPS: `/home/phil/palanthai/`

## Workflow Automation (n8n)

**n8n Instance:**
- URL: https://n8n.recall-agency.com
- Container: `n8n` in Docker stack
- Worker: `n8n-worker` for queue processing
- Workflows directory: `/home/phil/local-ai-packaged/n8n/workflows/`

**Active Workflows:**
| Workflow | Function |
|----------|----------|
| `SEO_Article_Monitoring_Generation.json` | SEO automation: GSC + GA4 → Ollama → WordPress (reflexion.asia + recall-agency.com) |
| `V1_Local_RAG_AI_Agent.json` | RAG with local Ollama + Qdrant |
| `V2_Local_Supabase_RAG_AI_Agent.json` | RAG with Supabase backend |
| `V3_Local_Agentic_RAG_AI_Agent.json` | Agentic RAG workflow |

**Backup Workflows:** WF-002, WF-003, WF-004, WF-006

**Internal URLs for n8n workflows:**
```
N8N_URL=http://n8n:5678
N8N_WEBHOOK_URL=https://n8n.recall-agency.com
SUPABASE_URL=http://kong:8000
QDRANT_URL=http://qdrant:6333
NEO4J_URL=bolt://neo4j:7687
OLLAMA_HOST=http://ollama:11434
CRAWL4AI_URL=http://crawl4ai:11235
REDIS_HOST=redis:6379
```

## WordPress Integration

**Sites:**
| Site | URL | WordPress Path | SEO Plugin | Languages |
|------|-----|----------------|------------|-----------|
| reflexion.asia | https://reflexion.asia | `/home/u965287345/domains/reflexion.asia/public_html` | RankMath | Polylang (FR/EN) |
| recall-agency.com | https://recall-agency.com | `/home/u965287345/domains/recall-agency.com/public_html` | RankMath | Polylang (FR/EN) |
| patrimonasia.com | Not yet built | - | - | - |

**RankMath Schema Fields:**
- `rank_math_title` - Meta title
- `rank_math_description` - Meta description
- `rank_math_focus_keyword` - Focus keyword
- `rank_math_schema` - JSON-LD schema

**WP-CLI Usage:**
```bash
wp plugin list --path=/home/u965287345/domains/reflexion.asia/public_html
wp core update --path=/home/u965287345/domains/reflexion.asia/public_html
```

## Reverse Proxy & TLS (Caddy)

**Caddy Server:**
- Container: `caddy:2-alpine`
- Purpose: Reverse proxy and automatic TLS
- Ports: 80, 443
- Config: `/home/phil/local-ai-packaged/Caddyfile`
- Manages SSL certificates for all subdomains

## MCP Servers & Extensions

**Hostinger MCP Server:**
- Purpose: VPS management via MCP protocol
- Access: From Cursor/Antigravity IDE
- Capabilities: VM status, snapshots, backups, firewall management
- Location: `30_Knowledge/Tooling/hostinger-mcp-server.md`

**Obsidian MCP Bridge:**
- Purpose: Connect Obsidian vault to external tools
- Location: `30_Knowledge/Tooling/obsidian-mcp-bridge.md`

**Linear MCP Server:**
- Purpose: Project management integration
- Location: `30_Knowledge/Tooling/linear-mcp-server.md`

## Additional Services

**Google Workspace:**
- Google Docs - Documentation
- Google Drive - File storage
- Integration via GCP for some services

**GitHub:**
- Repository: `sickn33/antigravity-awesome-skills` (skills catalog)
- SSH keys configured for Git operations

**HuggingFace:**
- Transformers library for embeddings
- Datasets: Real estate data processing

**Mapbox:**
- Map service for LANNA frontend
- Alternative: MapLibre GL (open-source)

**Bitwarden:**
- Password management for credentials

**Stats:**
- System monitoring for macOS

## Environment Configuration Summary

**Required environment variables on VPS:**
```
# Supabase
POSTGRES_PASSWORD=...
DATABASE_URL=postgresql://...

# Qdrant
QDRANT_API_KEY=...

# Neo4j
NEO4J_AUTH=...

# Ollama
OLLAMA_HOST=http://ollama:11434

# OpenRouter
OPENROUTER_API_KEY=...

# n8n
N8N_HOSTNAME=n8n.recall-agency.com
N8N_ENCRYPTION_KEY=...
```

**Required environment variables on Mac:**
```
STITCH_API_KEY=...
HOSTINGER_API_KEY=...
CLOUDFLARE_API_TOKEN=...
HOSTINGER_FIREWALL_KEY=...
```

---

*Integration audit: 2026-04-13*
