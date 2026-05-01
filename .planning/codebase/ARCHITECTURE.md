# Architecture

**Analysis Date:** 2026-05-01

## Pattern Overview

**Overall:** Multi-project orchestration hub with distributed microservices

**Key Characteristics:**
- Obsidian vault as central nervous system (not traditional codebase)
- PARA 2.0 organizational structure across three projects
- Hybrid infrastructure: local macOS + VPS Hostinger + Shared Hosting
- AI agent orchestration via multiple CLI tools (Claude Code, Gemini CLI, Antigravity)
- Data pipeline from scraping to WordPress publishing

## Layers

**Obsidian Vault (SystemMac):**
- Purpose: Central coordination, documentation, agent instructions
- Location: `/Users/phil/Documents/Vaults/SystemMac`
- Contains: Project dashboards, infrastructure docs, agent instructions, session logs
- Depends on: Nothing (it's the root context)
- Used by: All agents and human operator

**Infrastructure Layer (VPS Hostinger 31.97.67.145):**
- Purpose: Docker-based microservices for data processing and automation
- Location: `/home/phil/local-ai-packaged/` and `/home/phil/palanthai/`
- Contains: Supabase, Qdrant, Neo4j, n8n, Ollama, Palanthai API
- Depends on: Docker, systemd
- Used by: Scraping pipeline, RAG queries, workflow automation

**Data Pipeline (Palanthai):**
- Purpose: Scrape real estate data, extract, embed, and publish
- Location: `/home/phil/palanthai/` (phase1, phase2, phase3)
- Contains: Python scrapers, Pydantic models, embedding scripts
- Depends on: LivePhuket.com, FazWaz.com
- Used by: n8n workflows, Palanthai API

**Web Layer (Shared Hosting 92.113.28.34):**
- Purpose: Production WordPress sites
- Location: LiteSpeed + PHP on shared hosting
- Contains: reflexion.asia, recall-agency.com, patrimonasia.com
- Depends on: n8n workflows for content automation
- Used by: End users

## Data Flow

**Primary Flow (Property Intelligence):**

```
LivePhuket.com (Scraping)
    ↓
phase1/source_crawler.py → URL discovery (6 regions)
    ↓
phase1/wf_extract/*.py → Project extraction (12 city/type combos)
    ↓
phase1/fullrun/fullrun.py → Orchestrator (JSONL batches to disk)
    ↓
phase1/ingestor_v5.py → Multi-DB ingest (Supabase)
    ↓
phase2/sequencer_v2.py → Unit extraction + quality check
    ↓
db_ingestor_units.py → Supabase upsert
    ↓
phase3/content/data_cleaner.py → Brand replacement (source → "Reflexion")
    ↓
phase3/content/embed_to_qdrant.py → OpenRouter embeddings → Qdrant
    ↓ (quality >= 75 gate)
Qdrant (45,039 units, 768 dims, Cosine)
    ↓
Palanthai API (FastAPI, port 8500)
    ↓
n8n workflows (SEO automation, content generation)
    ↓
WordPress (reflexion.asia, recall-agency.com)
```

**Secondary Flows:**

```
User → Chat Agent → Palanthai API → Qdrant (RAG)
    ↓
HERMES Agent (Python venv, dashboard :9119)
    ↓
SearXNG (meta-search, port 8081)

n8n.recall-agency.com → Workflows → Supabase + Qdrant
    ↓
WordPress sites (92.113.28.34)
```

## Key Abstractions

**Palanthai Module Architecture (Palantir-inspired):**

| Module | Thai Name | Purpose |
|--------|-----------|---------|
| SIAM | สยาม | Scraping Intelligence & Acquisition — Crawlers, extractors, ETL |
| CHANG | ช้าง | Central Hub for Aggregation, Normalization & Governance — Supabase, Qdrant, Neo4j |
| NAGA | นาค | Node-based Architecture for Graph & Analysis — Knowledge graph (INACTIVE) |
| GARUDA | ครุฑ | Generative AI-Ready Unified Data Access — LLM integration, RAG, semantic search |
| KINNAREE | กินรี | Key Insights, Notifications & Automated Reporting — Market intel, due diligence |
| LANNA | ล้านนา | Live Analytics, Notification & Navigation App — Frontend: chat, 3D maps, dashboards |

**Project Architecture:**

Three projects under PARA 2.0, each with Identity/Technical/Knowledge/Tasks structure:

- **Recall Agency** (10_Recall_Agency/) — B2B tech-first, Next.js rebranding, scraping automation
- **Reflexion Asia** (20_Reflexion_Asia/) — Palantir of real estate, RAG, 3D discovery (Palanthai core)
- **Patrimonasia** (30_Patrimonasia/) — European partner network, wealth management (NOT BUILT YET)

## Entry Points

**SystemMac Command Center:**
- Location: `00_COMMAND_CENTER.md`
- Triggers: Agent startup, project switching
- Responsibilities: Strategic axes, project dashboards, infrastructure overview

**Agent Instructions:**
- Location: `40_Context_Hub/AGENT_INSTRUCTIONS.md`
- Triggers: Every new agent session
- Responsibilities: Identity, stack, rules, vault organization

**Current Context:**
- Location: `40_Context_Hub/CURRENT_CONTEXT.md`
- Triggers: Task start
- Responsibilities: Active task state, work log, Google credentials

## Error Handling

**Strategy:** Human-in-the-loop governance

**Patterns:**
- Quality gates: Only embed units with quality score >= 75/100
- Agent propose, human approve: No autonomous external actions
- Brand replacement: External source names → "Reflexion" in outputs
- Free models only: OpenRouter calls must use `:free` suffix

## Cross-Cutting Concerns

**Logging:** Session logs in `40_Context_Hub/SESSION_LOGS/`, VPS logs in `/home/phil/palanthai/logs/`

**Validation:** Pydantic models for all data schemas (unit_schema.py, models_parsers_00.py)

**Security:** Security audit documented in `10_Infrastructure/VPS_Hostinger/VPS_Security_Audit_2026-05-01.md` — 6 CRITICAL findings including hardcoded credentials

**Authentication:** Supabase Gotrue for auth, JWT tokens, RLS policies on all tables

---

*Architecture analysis: 2026-05-01*