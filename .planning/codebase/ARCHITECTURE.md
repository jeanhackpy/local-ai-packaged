# Architecture

**Analysis Date:** 2026-04-13

## Pattern Overview

**Overall:** Multi-Project Agent Orchestration Hub with AI-First Data Platform

SystemMac serves as the central orchestration hub for Thai real estate intelligence operations. It coordinates three interconnected projects (Recall Agency, Reflexion Asia/Palanthai, Patrimonasia) through AI agents (Claude Code, Gemini CLI, Antigravity) while managing infrastructure (VPS Hostinger, Shared Hosting) and housing technical knowledge.

**Key Characteristics:**
- **Agent-First Architecture**: All agents (Gemini CLI, Claude Code, Antigravity IDE) operate through the Obsidian vault as shared context window
- **PARA 2.0 Organization**: Projects, Areas, Resources, Archives structure adapted for multi-project management
- **Context-First Protocol**: Agents must read `40_Context_Hub/CURRENT_CONTEXT.md` before any task execution
- **Hybrid Infrastructure**: VPS Hostinger (Docker containers) + Shared Hosting (WordPress/PHP/MySQL) + Local macOS

## Layers

**Agent Orchestration (SystemMac):**
- Purpose: Coordinate AI agents and human operators across all projects
- Location: `40_Context_Hub/` - Context window for all agents
- Contains: `AGENT_INSTRUCTIONS.md`, `CURRENT_CONTEXT.md`, `AGENT_CROSS_COMMUNICATION.md`, `SESSION_LOGS/`
- Depends on: MCP servers, Skills registry, project dashboards
- Used by: Gemini CLI, Claude Code, Antigravity IDE

**Intelligence Platform (Palanthai):**
- Purpose: AI-powered Thai real estate data extraction, storage, and RAG-based search
- Location: `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/`
- Contains: SIAM (crawler), CHANG (Supabase/Qdrant/Neo4j), NAGA (graph), GARUDA (RAG), KINNAREE (reports), LANNA (frontend)
- Depends on: Crawl4AI, Supabase, Qdrant, Neo4j, Ollama
- Used by: Reflexion Asia website, Recall Agency services

**Web Properties (Recall Agency):**
- Purpose: B2B tech-first real estate scraping services
- Location: `20_Projects/Active/websites redesign/recall-agency.com/code/`
- Contains: Next.js application with Stitch MCP UI generation
- Depends on: Hostinger Node.js VPS, Cloudflare
- Used by: End clients seeking Thai property data

**Infrastructure Management:**
- Purpose: VPS and hosting management documentation
- Location: `10_Infrastructure/`
- Contains: `VPS_Hostinger/` (Docker, n8n, Qdrant, Neo4j), `Shared_Hosting/Hostinger/` (WordPress sites)
- Depends on: Hostinger MCP server
- Used by: All projects requiring deployment or hosting

## Data Flow

**Palanthai Data Pipeline:**

```
SIAM (Crawl4AI Extractors)
    │
    ├── phase1_project_extractor.py ──► CHANG (Supabase: project table)
    │                                    │
    │                                    ├──► Qdrant (projects collection) ──► GARUDA RAG
    │                                    └──► Neo4j (Project nodes) ──► NAGA Graph
    │
    ├── phase1_developer_extractor.py ──► CHANG (Supabase: developer table)
    │                                    └──► Neo4j (Developer nodes)
    │
    ├── phase1_faq_extractor.py ────────► CHANG (Supabase: faq_article table)
    │                                    └──► Qdrant (faq_knowledge) ──► GARUDA RAG
    │
    └── phase1_financial_extractor.py ──► CHANG (Supabase: market_data table)
                                         └──► Neo4j (MarketSector nodes)
```

**Agent Communication Flow:**

```
Human Operator
    │
    ├──► Claude Code ──► Obsidian Vault ──► AGENT_INSTRUCTIONS.md
    │                   (Current Context)
    │
    ├──► Gemini CLI ────► .planning/context ──► CURRENT_CONTEXT.md
    │                   (Session State)
    │
    └──► Antigravity ───► /jules endpoint ──► Jules Server MCP
                         (Async code review)
```

**State Management:**
- **Agent Instructions**: `40_Context_Hub/AGENT_INSTRUCTIONS.md` - global context and rules
- **Current Context**: `40_Context_Hub/CURRENT_CONTEXT.md` - active project state and next actions
- **Cross-Communication**: `40_Context_Hub/AGENT_CROSS_COMMUNICATION.md` - inter-agent status and handover notes
- **Session Logs**: `40_Context_Hub/SESSION_LOGS/` - chronological agent activity logs

## Key Abstractions

**PARA 2.0 Directory Structure:**
- `00_System/` - Local macOS maintenance (not time-bound)
- `10_Infrastructure/` - Infrastructure details (VPS, hosting)
- `20_Projects/` - Time-bound active projects with dashboards
- `30_Knowledge/` - Permanent technical documentation
- `40_Context_Hub/` - Agent context window (instructions, sessions)

**MCP Server Registry:**
- Purpose: Unified tool access for AI agents
- Examples: `00_System/Configs/MCP_SKILLS_INVENTORY.md`
- Pattern: MCP servers provide tools (cloudflare, github, google-analytics, hostinger-api, obsidian, stitch, julesServer, chrome-devtools, context7)

**Skills Registry:**
- Purpose: Workflow agents for complex tasks
- Examples: `30_Knowledge/Agent_Factory/Skills_Registry.md`
- Categories: Superpowers (brainstorming, writing-plans, executing-plans), Development (huggingface-jobs, crawl4ai-skill), Business (deep-research, market-research, content-engine)

**Palanthai Module Mapping (Palantir → Thai):**
- SIAM: Scraping Intelligence & Acquisition Module (crawlers, ETL)
- CHANG: Central Hub for Aggregation, Normalization & Governance (Supabase, Qdrant, Neo4j)
- NAGA: Node-based Architecture for Graph & Analysis (knowledge graph, entity resolution)
- GARUDA: Generative AI-Ready Unified Data Access (LLM integration, RAG, semantic search)
- KINNAREE: Key Insights, Notifications & Automated Reporting Engine (market intel, alerts)
- LANNA: Live Analytics, Notification & Navigation App (frontend: chat, 3D maps, dashboards)

## Entry Points

**Command Center:**
- Location: `00_COMMAND_CENTER.md`
- Triggers: Human or agent startup
- Responsibilities: Strategic axes overview, project dashboards, infrastructure status, agent instructions reference

**Agent Instructions:**
- Location: `40_Context_Hub/AGENT_INSTRUCTIONS.md`
- Triggers: Any agent task execution
- Responsibilities: Identity definition, technical stack, core mandates, vault organization rules

**Current Context:**
- Location: `40_Context_Hub/CURRENT_CONTEXT.md`
- Triggers: Context-first protocol before any task
- Responsibilities: Active project state, recent work completed, next actions, security credentials

## Error Handling

**Strategy:** Context propagation with session logging

**Patterns:**
- Session logs in `40_Context_Hub/SESSION_LOGS/` with YYYY-MM-DD naming
- Cross-communication status table tracking service states (VPS Monitoring, Shared Hosting, n8n Workflows, Supabase Sync)
- Work journals in `10_Infrastructure/VPS_Hostinger/Journal_Travail_*.md`

## Cross-Cutting Concerns

**Logging:** Session logs (`SESSION_LOGS/`), work journals (`Journal_Travail_*.md`), audit files (`00_System/Audits/`)

**Validation:** Pydantic models in scraper scripts, JSON-LD Schema.org extraction (primary strategy), data quality scores

**Authentication:** `.env.local` for local credentials, `00_System/Secrets/` for service accounts, RLS policies in Supabase

**Security:** No API keys in vault (placeholders only), security policies in `00_System/Policies/03_Security.md`, disavow files in `00_System/Audits/`

---

*Architecture analysis: 2026-04-13*
