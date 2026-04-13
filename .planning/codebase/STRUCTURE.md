# Codebase Structure

**Analysis Date:** 2026-04-13

## Directory Layout

```
SystemMac/
├── 00_COMMAND_CENTER.md      # Main entry point (strategic axes, dashboards)
├── 00_System/                # macOS local maintenance
├── 10_Infrastructure/        # VPS Hostinger, Shared Hosting
├── 20_Projects/              # Active projects with dashboards
├── 30_Knowledge/             # Technical documentation, AI orchestration
├── 40_Context_Hub/           # Agent context window (instructions, sessions)
├── Clippings/                # Curated research (LLM wiki pattern)
├── WIKI/                     # Additional wiki content
├── Excalidraw/               # Excalidraw diagram files
├── entities/                 # Entity files
├── .env.local                # API keys and credentials (never commit)
├── .gitignore                # Git ignore patterns
└── .obsidian/                # Obsidian app data
```

## Directory Purposes

**00_System/:**
- Purpose: Local macOS system maintenance, OS specs, cleaning scripts, policies
- Contains:
  - `Configs/MCP_SKILLS_INVENTORY.md` - inventory of MCP servers
  - `Configs/Architecture/MCP_SKILLS_SCHEMA.md` - MCP schema definitions
  - `Policies/` - Policy framework (01_BaseSetup, 02_DevEnv, 03_Security, 04_Workflow, 05_Maintenance)
  - `Maintenance/` - Cleaning and health check scripts
  - `Scripts/` - Operational scripts (crawl_test.py, sync_obsidian_links.sh)
  - `Secrets/` - Service account JSON files (google_credentials.json, etc.)
  - `Audits/` - Site audit files (reflexion.asia.md, recall-agency.com.md, disavow files)
  - `System_Mapping.md` - System inventory

**10_Infrastructure/:**
- Purpose: VPS Hostinger and Shared Hosting documentation
- Contains:
  - `VPS_Hostinger/` - Docker-based services (n8n, Qdrant, Neo4j, Ollama, Caddy)
    - `Pipeline_Dashboard.md` - Pipeline monitoring
    - `Plan_Action_Monitoring.md` - Action plan tracking
    - `Journal_Travail_*.md` - Work journals
    - `Kanban_Travail.md` - Kanban board
    - `RLS_HARDENING_*.md` - Security hardening plans
    - `SUPABASE_RLS_AUDIT_*.md` - RLS audit documents
    - SQL and Python audit scripts
  - `Shared_Hosting/Hostinger/` - WordPress sites on Hostinger
    - `Access/` - SSH and FTP credentials
    - `Details/` - Plan documentation
  - `Data_Architecture.md` - Data architecture overview (Supabase, Qdrant, Neo4j schemas)

**20_Projects/:**
- Purpose: Active time-bound projects with dashboards
- Contains:
  - `20_Reflexion_Asia/` - Palanthai real estate intelligence platform
    - `02_Technical/Palanthai_Core/` - Core platform documentation
      - `00_README.md` - Module architecture (SIAM, CHANG, NAGA, GARUDA, KINNAREE, LANNA)
      - `01_Database_Architecture.md` - Full schema (Supabase, Qdrant, Neo4j)
      - `02_Pipeline_Status.md` - SIAM extractor status tracker
      - `03_Data_Sources.md` - Data sources documentation
      - `04_GDrive_Resources.md` - Google Drive resources
      - `05_LANNA_Frontend_PRD.md` - Frontend specification
  - `Active/Pipeline_Main_Scraper.md` - Main scraper pipeline status
  - `Active/websites redesign/recall-agency.com/code/` - Next.js application
    - `src/app/` - Next.js app directory
    - `package.json` - Dependencies
    - `tsconfig.json` - TypeScript configuration
    - `eslint.config.mjs` - ESLint configuration
  - `10_Recall_Agency/` - (referenced in command center)
  - `30_Patrimonasia/` - (referenced in command center)

**30_Knowledge/:**
- Purpose: Permanent technical documentation and AI orchestration guides
- Contains:
  - `AI_Orchestration/` - Agent CLI documentation
    - `ClaudeCode CLI.md` - Claude Code setup and usage
    - `Gemini CLI.md` - Gemini CLI setup and usage
    - `Antigravity IDE.md` - Antigravity IDE documentation
    - `Crawl4AI Datascraper.md` - Crawl4AI agent documentation
    - `Ollama.md` - Ollama local LLM
    - `Cursor.md`, `VsCode.md`, `OpenCode CLI.md` - IDE integrations
    - `Superwhisper TTS.md` - TTS documentation
  - `Tooling/` - Tool integrations
    - `hostinger-mcp-server.md` - Hostinger MCP server
    - `obsidian-mcp-bridge.md` - Obsidian MCP bridge
    - `linear-mcp-server.md` - Linear MCP server
    - `Everything-Claude-Code-Installation.md` - Installation guide
  - `Development/` - Development documentation
    - `docs.crawl4ai.com/` - Crawl4AI documentation (full mirror)
    - `VPS Hostinger & WordPress.md` - VPS documentation
    - `IDE & Skills.md` - Development environment
    - `Script.py/00_INDEX.md` - Python scripts index
  - `Agent_Factory/Skills_Registry.md` - Skills inventory
  - `Visuals/saas-ui-inspiration.md` - UI inspiration
  - `Business/strategic-business-concepts.md` - Business concepts

**40_Context_Hub/:**
- Purpose: Agent context window - instructions, sessions, cross-communication
- Contains:
  - `AGENT_INSTRUCTIONS.md` - Global agent context and rules
  - `CURRENT_CONTEXT.md` - Active project state (required read before tasks)
  - `AGENT_CROSS_COMMUNICATION.md` - Inter-agent status table and handover notes
  - `BIRD_EYE_VIEW.md` - Project pulse overview
  - `SESSION_LOGS/YYYY-MM-DD-*.md` - Chronological session logs
  - `RE/` - Brand assets and content calendar

**Clippings/:**
- Purpose: Curated research following LLM Wiki pattern (Karpathy)
- Contains:
  - `raw/` - 51 original sources (articles, papers on Thai real estate, AI/ML)
  - `wiki/` - LLM-generated structured wiki
    - `index.md` - Source catalog
    - `log.md` - Ingestion history
    - `overview.md` - Overview
    - `sources/` - 43 source summaries
    - `concepts/` - 8 concept pages
    - `entities/` - 2 entity pages
    - `synthesis/` - Cross-analysis documents
  - `WIKI_SCHEMA.md` - Schema for LLM ingestion
  - `README.md` - Clippings wiki documentation

**WIKI/:**
- Purpose: Additional wiki content (Obsidian plugin data)
- Contains: Wiki schema and related documentation

**Excalidraw/:**
- Purpose: Excalidraw diagram files
- Contains: Excalidraw format diagrams

**entities/:**
- Purpose: Entity definitions
- Contains: Entity files for Obsidian

**00_COMMAND_CENTER.md:**
- Purpose: Main entry point for human and agent interaction
- Contains: Strategic axes (Recall Agency, Reflexion Asia, Patrimonasia), infrastructure links, agent instructions reference

## Key File Locations

**Entry Points:**
- `00_COMMAND_CENTER.md`: Main entry point - strategic overview, links to project dashboards
- `40_Context_Hub/AGENT_INSTRUCTIONS.md`: Agent identity and rules - must read before any task
- `40_Context_Hub/CURRENT_CONTEXT.md`: Active state - must read before any task

**Configuration:**
- `.env.local`: Local API keys and credentials
- `00_System/Configs/MCP_SKILLS_INVENTORY.md`: MCP server inventory
- `00_System/Policies/`: Policy framework (01-05)

**Core Logic:**
- `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/00_README.md`: Palanthai module architecture
- `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/01_Database_Architecture.md`: Full data architecture
- `10_Infrastructure/Data_Architecture.md`: Simplified data architecture reference

**Testing:**
- `00_System/Scripts/crawl_test.py`: Crawl4AI test script
- `10_Infrastructure/VPS_Hostinger/rls_security_audit.py`: Security audit script

## Naming Conventions

**Files:**
- Markdown files: `Title_Case_With_Underscores.md` or `YY_Dashboard.md`
- Session logs: `YYYY-MM-DD-Descriptive-Name.md`
- Python scripts: `snake_case.py`
- Policy files: `01_BaseSetup.md` (numbered sequence)

**Directories:**
- PARA directories: `NN_Name/` (00-40 numbered sequence)
- Project directories: `NN_Project_Name/`
- Technical directories: `NN_Technical/`

## Where to Add New Code

**New Feature:**
- Palanthai core: `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/`
- Scraping scripts: Symlinked in `20_Projects/Active/main_scraper/` (from `/Users/phil/Documents/The_Lab/Pipeline/main_scraper`)

**New Infrastructure Documentation:**
- VPS: `10_Infrastructure/VPS_Hostinger/`
- Shared Hosting: `10_Infrastructure/Shared_Hosting/Hostinger/`

**New Agent Session:**
- `40_Context_Hub/SESSION_LOGS/YYYY-MM-DD-Descriptive-Name.md`

**New Clipping:**
- Raw source: `Clippings/raw/`
- Wiki page: `Clippings/wiki/sources/` or `concepts/` or `entities/`

**New Technical Knowledge:**
- AI Orchestration: `30_Knowledge/AI_Orchestration/`
- Tooling: `30_Knowledge/Tooling/`
- Development: `30_Knowledge/Development/`

## Special Directories

**00_System/Secrets/:**
- Purpose: Service account JSON files (google_credentials.json, etc.)
- Generated: No (committed to vault)
- Contains: Client secrets for Google APIs

**00_System/Audits/:**
- Purpose: Site audit documents and disavow lists
- Generated: Yes
- Committed: Yes
- Files: reflexion.asia.md, recall-agency.com.md, disavow files

**20_Projects/Active/websites redesign/recall-agency.com/code/:**
- Purpose: Next.js application code (symlinked or copied)
- Generated: No (git repository)
- Committed: Yes
- Contains: Full Next.js project with node_modules

**Clippings/wiki/:**
- Purpose: LLM-generated structured content from raw sources
- Generated: Yes (via LLM ingestion)
- Committed: Yes
- Structure: sources/, concepts/, entities/, synthesis/, index.md, log.md

---

*Structure analysis: 2026-04-13*
