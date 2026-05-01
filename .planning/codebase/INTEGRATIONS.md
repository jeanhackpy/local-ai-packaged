# External Integrations

**Analysis Date:** 2026-05-01

---

## Infrastructure

### VPS (Hostinger)
| Service | Access | Purpose |
|---------|--------|---------|
| SSH | `ssh phil@31.97.67.145` | Main server access |
| SSH Key | `~/.ssh/id_ed25519` | Authentication |

### Shared Hosting
| Service | URL | Purpose |
|---------|-----|---------|
| WordPress | 92.113.28.34:65002 | reflexion.asia, recall-agency.com, patrimonasia.com |

---

## Database Services

### PostgreSQL (Supabase)
- **Internal:** `postgres://postgres@supabase-db:5432`
- **Public URL:** Via Kong gateway `http://kong:8000`
- **Driver:** psycopg2, SQLModel
- **Purpose:** Property listings, constructors, residences

### Qdrant (Vector Store)
- **URL:** `http://qdrant:6333` (internal), `http://31.97.67.145:6333` (external)
- **Port:** 6333 (REST), 6334 (gRPC)
- **Collection:** `units` (45,039 points, 768 dims, Cosine)
- **Purpose:** Semantic search, RAG embeddings

### Neo4j (Graph Database)
- **URL:** `bolt://neo4j:7687`
- **Status:** Container running (previously had connection issues)
- **Purpose:** Knowledge graph for properties/projects
- **Credentials:** Hardcoded in scripts (SECURITY RISK)

### Valkey (Redis)
- **URL:** `redis://redis:6379`
- **Purpose:** Cache and queue operations

---

## AI/LLM Services

### OpenRouter
- **Purpose:** Free model routing for Phase 3 embeddings
- **Usage:** `embed_to_qdrant.py`, `model_config.py`
- **Config:** Uses `:free` suffix for model selection

### Groq
- **API:** `GROQ_API_KEY` in Docker `.env`
- **Purpose:** Fast LLM inference

### Ollama
- **URL:** `http://ollama:11434`
- **Status:** Container **exited** (not running)
- **Purpose:** Local LLM inference (bypassed due to exit)

### ElevenLabs
- **API:** `ELEVENLABS_API_KEY` in Docker `.env`
- **Purpose:** Text-to-speech

---

## Automation & Workflows

### n8n
- **URL:** https://n8n.recall-agency.com
- **Internal:** `http://n8n:5678`
- **Workflows:**
  - SEO Article Monitoring Generation
  - V1/V2/V3 Local RAG AI Agent
- **Environment:** `N8N_URL`, `N8N_WEBHOOK_URL`, `N8N_ENCRYPTION_KEY`

### Telegram
- **Bot Token:** `TELEGRAM_BOT_TOKEN` in Docker `.env`
- **Purpose:** Notifications and alerts

---

## Web Scraping

### LivePhuket.com
- **Purpose:** Source for Thai property listings
- **Auth:** Playwright-based login
- **Regions:** bangkok, phuket, surat-thani, chiang-mai, chon-buri, prachuap-kiri-khan
- **Scripts:** `source_crawler.py`, `livephuket_login.py`, `wf_extract/*.py`

### Crawl4AI
- **Environment:** `~/PythonTools/.venv`
- **Version:** 0.7.x (async)
- **Usage:** Large-scale web scraping with markdown output

---

## External APIs (Stored in .env.local)

| Service | Key Variable | Purpose |
|---------|-------------|---------|
| Stitch | `STITCH_API_KEY` | UI integration |
| Hostinger | `HOSTINGER_API_KEY` | VPS management |
| Cloudflare | `CLOUDFLARE_API_TOKEN`, `CLOUDFLARE_API_TOKEN_2` | DNS, security |
| Hostinger Firewall | `HOSTINGER_FIREWALL_KEY` | Firewall management |

---

## WordPress Sites

| Site | URL | Theme | SEO |
|------|-----|-------|-----|
| reflexion.asia | https://reflexion.asia | Houzez | RankMath |
| recall-agency.com | https://recall-agency.com | Astra child | RankMath + Polylang |
| patrimonasia.com | https://patrimonasia.com | Not built | — |

**Server:** 92.113.28.34 (separate from VPS, LiteSpeed + PHP)

---

## Internal Service URLs

```
n8n.recall-agency.com     → n8n:5678 (via Caddy)
supabase.recall-agency.com → kong:8000 (via Caddy)
Palanthai API             → http://31.97.67.145:8500
Qdrant                    → http://31.97.67.145:6333
```

---

## Authentication Services

### Supabase Auth
- **Provider:** Gotrue (v2.184.0)
- **Config:** `JWT_SECRET`, `ANON_KEY`, `SERVICE_ROLE_KEY`
- **Purpose:** User authentication for applications

---

*Integration audit: 2026-05-01*