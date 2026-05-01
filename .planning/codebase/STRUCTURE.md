# Codebase Structure

**Analysis Date:** 2026-05-01

## Directory Layout

```
SystemMac/
├── 00_COMMAND_CENTER.md      # Strategic entry point
├── CLAUDE.md                 # Project instructions
├── README.md
├── 00_System/                # macOS maintenance
├── 10_Infrastructure/        # VPS Hostinger, Shared Hosting
├── 20_Projects/              # Active projects with dates
├── 30_Knowledge/            # Permanent technical knowledge base
├── 40_Context_Hub/           # Agent instructions and sessions
├── Clippings/                # Curated research
├── WIKI/                     # Obsidian wiki (concepts, entities, synthesis)
├── Excalidraw/               # Diagrams
├── entities/                 # Entity files
└── .env.local               # API keys (NEVER commit)
```

## Directory Purposes

**00_System/ (macOS Maintenance):**
- Purpose: Local machine configuration, audits, policies
- Contains:
  - `Architecture/` — System mapping files
  - `Audits/` — Technical audits
  - `Configs/` — MCP skills inventory, git/ssh/zsh configs
  - `Links/` — External service links
  - `Maintenance/` — macOS maintenance scripts
  - `Policies/` — Operating policies
  - `Scripts/` — Utility scripts
  - `Secrets/` — Credential references (not values)
  - `spatial_building_match.js` — Spatial matching tool

**10_Infrastructure/ (VPS & Hosting):**
- Purpose: Technical infrastructure documentation
- Contains:
  - `VPS_Hostinger/` — 31.97.67.145 full documentation (31 files)
  - `Shared_Hosting/` — WordPress hosting (92.113.28.34)
  - `Data_Architecture.md` — Complete data pipeline schema
  - `VPS_Security_Audit_2026-05-01.md` — Security findings

**20_Projects/ (Active Work):**
- Purpose: Projects with end dates (PARA 2.0)
- Contains:
  - `10_Recall_Agency/` — Identity, Technical, Knowledge, Tasks
  - `20_Reflexion_Asia/` — Identity, Technical, Knowledge, Tasks
  - `30_Patrimonasia/` — Identity, Technical, Knowledge, Tasks (NOT BUILT)
  - `Active/` — Active sub-projects (websites redesign, recall-agency-v3-redesign)
  - `Archive/` — Completed projects
  - `Reflexion-Asia/` — Secondary reference

**30_Knowledge/ (Permanent KB):**
- Purpose: Technical documentation, tutorials, tooling docs
- Contains:
  - `AI_Orchestration/` — IDE capabilities, Gemini CLI, Claude Code, Ollama, Antigravity
  - `Agent_Factory/` — Skills registry, superpowers skills
  - `API_Specs/` — API specifications
  - `Business/` — Business knowledge
  - `Development/` — Development docs (Script.py, crawl4ai, github inventory)
  - `Tooling/` — Tool documentation
  - `Vector_DB/` — Vector database docs
  - `Visuals/` — Visual assets/documents

**40_Context_Hub/ (Agent Window):**
- Purpose: AI agent context and instructions
- Contains:
  - `AGENT_INSTRUCTIONS.md` — Global agent instructions
  - `CURRENT_CONTEXT.md` — Active task state
  - `BIRD_EYE_VIEW.md` — System overview
  - `AGENT_CROSS_COMMUNICATION.md` — Agent coordination
  - `RE/` — Requirements/epics
  - `SESSION_LOGS/` — Agent session logs

**WIKI/ (Obsidian Wiki):**
- Purpose: Structured knowledge organization
- Contains:
  - `concepts/` — Concept definitions
  - `entities/` — Entity files
  - `raw/` — Raw source materials
  - `sources/` — Source references
  - `synthesis/` — Synthesized knowledge
  - `index.md`, `log.md`, `overview.md`

**Clippings/ (Curated Research):**
- Purpose: Collected research materials

## Key File Locations

**Entry Points:**
- `00_COMMAND_CENTER.md` — Strategic command center
- `40_Context_Hub/AGENT_INSTRUCTIONS.md` — Agent identity and rules
- `40_Context_Hub/CURRENT_CONTEXT.md` — Current task context

**Configuration:**
- `.env.local` — API keys and credentials (for reference only, not committed)
- `00_System/Configs/MCP_SKILLS_INVENTORY.md` — MCP server and skill inventory
- `.gitignore` — Git ignore rules

**Infrastructure:**
- `10_Infrastructure/VPS_Hostinger/VPS_INFRASTRUCTURE_REFERENCE.md` — VPS complete reference
- `10_Infrastructure/VPS_Hostinger/VPS_ARCHITECTURE_DIAGRAM.md` — Architecture diagrams
- `10_Infrastructure/Data_Architecture.md` — Data pipeline schema

**Project Dashboards:**
- `20_Projects/10_Recall_Agency/00_Dashboard.md`
- `20_Projects/20_Reflexion_Asia/00_Dashboard.md`
- `20_Projects/30_Patrimonasia/00_Dashboard.md`

**Palanthai Core (on VPS):**
- `/home/phil/palanthai/palanthai_api.py` — Main FastAPI
- `/home/phil/palanthai/phase1-project-directory/` — Scraping pipeline
- `/home/phil/palanthai/phase2/` — Extraction pipeline
- `/home/phil/palanthai/phase3-embedding&graph/` — Content pipeline

## Naming Conventions

**Files:**
- Markdown files: `UPPER_SNAKE_CASE.md` or `descriptive-name.md`
- Project folders: `NN_Name/` (numbered prefix for ordering)
- Documentation: `*.md` with frontmatter tags

**Directories:**
- PARA 2.0: `00_System/`, `10_Infrastructure/`, `20_Projects/`, `30_Knowledge/`, `40_Context_Hub/`
- Project subdirs: `01_Identity/`, `02_Technical/`, `03_Knowledge/`, `04_Tasks/`

## Where to Add New Code

**New Project:**
- Primary: `20_Projects/XX_ProjectName/`
- Structure: `01_Identity/`, `02_Technical/`, `03_Knowledge/`, `04_Tasks/`

**New Infrastructure Doc:**
- Primary: `10_Infrastructure/VPS_Hostinger/` or `Shared_Hosting/`

**New Knowledge:**
- Primary: `30_Knowledge/` appropriate subdirectory
- Consider WIKI/concepts/ for structured concepts

**New Agent Instruction:**
- Primary: `40_Context_Hub/`
- Session logs: `40_Context_Hub/SESSION_LOGS/`

**VPS Scripts (execute via SSH):**
- Palanthai scripts: `/home/phil/palanthai/phase1-project-directory/`
- Docker/infra: `/home/phil/local-ai-packaged/`

## Special Directories

**.planning/ (Generated):**
- Purpose: GSD planning outputs
- Generated: Yes
- Committed: Yes (architectural documentation)

**.claude/ (Claude Code):**
- Purpose: Claude Code project settings
- Generated: Yes
- Committed: No (.gitignore)

**.smart-env/ (Smart Environment):**
- Purpose: Environment configuration
- Generated: Yes
- Committed: No

**.obsidian/ (Obsidian):**
- Purpose: Obsidian vault configuration
- Generated: Yes
- Committed: No

---

*Structure analysis: 2026-05-01*