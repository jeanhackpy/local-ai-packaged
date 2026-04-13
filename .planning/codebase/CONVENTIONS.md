# Coding Conventions

**Analysis Date:** 2026-04-13

## Naming Patterns

### Files

**Obsidian Vault Files:**
- Markdown files use title case: `Brand Voice Framework.md`, `VPS Management Prompt Template.md`
- Wiki-links use `[[double brackets]]` with exact filenames including extensions: `[[Development/VPS Hostinger & WordPress#SSH Config]]`
- Frontmatter uses YAML with keys like `title:`, `type:`, `source:`, `tags:`, `notion_id:`, `notion_url:`, `published:`, `author:`, `description:`

**Python Scripts:**
- Snake case: `content_flywheel.py`, `rls_security_audit.py`, `phase1_project_extractor.py`
- Descriptive names reflecting purpose: `rls_security_audit.py`, `rls_redundancy_audit.py`

**Shell Scripts:**
- Snake case: `check_env.sh`, `mac_health_check.sh`, `super_clean.sh`, `sync_obsidian_links.sh`

**Directories:**
- PARA 2.0 organization: `00_System/`, `10_Infrastructure/`, `20_Projects/`, `30_Knowledge/`, `40_Context_Hub/`
- Sub-categories use CamelCase or descriptive names: `30_Knowledge/Development/`, `40_Context_Hub/SESSION_LOGS/`, `20_Projects/20_Reflexion_Asia/`

### Variables and Functions

**Python:**
- Snake case: `QDRANT_HOST`, `POSTGRES_HOST`, `EMBED_MODEL`, `EMBED_DIM`
- Class names use CamelCase: `RLSAuditTool`, `RLSRedundancyAudit`
- Type imports from `typing`: `List`, `Dict`, `Tuple`, `Set`, `Optional`, `Any`, `Literal`
- Pydantic models use CamelCase: `BaseModel`, `Field`

**Shell:**
- Uppercase for constants: `ENV_FILE`, `REQUIRED_KEYS`
- Lowercase with underscores for functions: `create_link()`

---

## Code Style

### Python

**Formatting:** PEP 8 conventions observed
- 4-space indentation
- Imports organized: `os`, `re`, `json`, `uuid`, `hashlib`, `logging` (stdlib first), then third-party (`httpx`, `fastapi`, `pydantic`, `dotenv`, `qdrant_client`, `sentence_transformers`, `psycopg2`)

**Type Annotations:**
```python
from typing import List, Dict, Tuple, Optional
# Function signatures include type hints
def connect(self) -> bool: ...
def query(self, sql: str) -> List[Tuple]: ...
```

**Docstrings:**
```python
"""
RLS Security Audit Tool for PostgREST-Exposed Tables
=====================================================

Detects PostgreSQL tables that lack Row-Level Security (RLS) protection
in schemas exposed to the PostgREST API. Produces automated audit reports
and remediation recommendations.

Usage:
    python3 rls_security_audit.py --host 31.97.67.145 --db postgres --user postgres
"""
```

**Class Structure:**
```python
class RLSAuditTool:
    """SQL-based RLS security audit for PostgREST exposure."""

    def __init__(self, host: str = None, database: str = "postgres", user: str = "postgres",
                 password: str = None, port: int = 5432, docker_container: str = None):
        self.host = host
        ...

    def connect(self) -> bool:
        """Establish database connection."""
        ...
```

**Error Handling:**
- Uses `try/except` with specific exceptions
- Prints errors to `sys.stderr`: `print(f"Error: {e}", file=sys.stderr)`
- Returns `False` or empty lists on failure rather than raising

**Environment Variables:**
```python
from dotenv import load_dotenv
load_dotenv("/home/phil/local-ai-packaged/.env")
QDRANT_HOST = os.getenv("QDRANT_HOST", "localhost")
```

### Shell Scripts

**Shebang:** `#!/bin/bash` or `#!/usr/bin/env python3`

**Comments:**
- Header with description and sections: `# ==============================================================================`
- Section dividers: `# ─────────────────────────────────────────────────────────`

**Output:**
- Emoji prefix for status: `echo "🔍 Vérification..."`, `echo "✅ $key est configuré."`, `echo "❌ Erreur..."`
- Timestamps in logs: `$(date)`

**Functions:**
```bash
create_link() {
    local target="$1"
    local link_name="$2"
    if [ -d "$target" ] || [ -f "$target" ]; then
        ...
    fi
}
```

**Conditional Guards:**
```bash
if [ ! -f "$ENV_FILE" ]; then
    echo "❌ Erreur : Fichier $ENV_FILE introuvable."
    exit 1
fi
```

---

## Import Organization

**Python - Standard Library First:**
```python
import os
import re
import json
import uuid
import hashlib
import logging
from datetime import datetime, timedelta
from typing import Optional, List, Dict, Any, Literal

import httpx
from fastapi import APIRouter, HTTPException, Query, BackgroundTasks
from pydantic import BaseModel, Field
from dotenv import load_dotenv

from qdrant_client import QdrantClient
from qdrant_client.models import (
    PointStruct, Filter, FieldCondition,
    MatchAny, MatchValue, Range,
)
from sentence_transformers import SentenceTransformer

import psycopg2
from psycopg2.extras import RealDictCursor
```

**Python - Pydantic Models Inline:**
```python
# Pydantic models defined in same file for extraction scripts
class ProjectRecord(BaseModel):
    """Canonical output schema, enforces facilities: List[str] (full names, never counts)"""
    name: str
    facilities: List[str]

class GeoLocation(BaseModel):
    """Lat/lng validation (range check, both-or-neither)"""
    lat: Optional[float] = None
    lng: Optional[float] = None
```

---

## Git Workflow Conventions

**Commit Messages:**
- French language used in this vault
- Format: `<description> — <detail>` or `[type] <description>`
- Examples from git log:
  - `Auto-backup Mac 2026-04-11 18:28:27`
  - `auto-sync 2026-03-26 12:26:17 — vault updates, plugin updates, clippings cleanup`
  - `Initial backup: SystemMac vault 2026-03-19`

**Branch Naming:** Not explicitly defined in documentation

**Gitignore Patterns:**
```
# Secrets — never commit
.env
.env.local
.env*.local
00_System/Secrets/

# Node.js projects inside vault
**/node_modules/
**/.next/
**/dist/

# Python
**/__pycache__/
**/*.pyc
**/.venv/
**/venv/

# Obsidian workspace state (machine-specific)
.obsidian/workspace.json
.obsidian/workspace-mobile.json
.obsidian/graph.json
```

---

## Documentation Standards

**Obsidian Frontmatter:**
```yaml
---
type: brand_assets
source: notion
notion_id: 333ebffa-e73e-81ff-98ba-e5a3a125ebe3
notion_url: https://www.notion.so/...
synced: 2026-03-30
tags: [RE, brand-voice, brand-assets, n8n-prompt]
---
```

**Wiki-Links Syntax:**
- Internal files: `[[filename]]` or `[[filename#heading]]`
- External links in same vault: `[[folder/file|Display Text]]`

**Markdown Headings:**
- H1: `# Title`
- H2: `## Section`
- H3: `### Subsection`
- Emoji prefix for visual scanning: `# 🛠️ 01 - Base System Setup`, `# 🔐 03 - Security Configuration`

**Code Blocks:**
- Language specified: ` ```bash`, ` ```python`, ` ```yaml`
- Run commands in code blocks for clarity

---

## Brand Naming Conventions

**Critical: Correct vs Incorrect**

| Correct | Incorrect |
|---------|-----------|
| REcall Agency | Recall Agency, recall agency |
| REflexion Asia | Reflexion Asia, reflexion.asia |
| PatrimoinAsia | Patrimoin Asia, patrimoinasia |
| RE ecosystem | re ecosystem |

**RE Prefix System:**
- RE is always capitalized as prefix
- Full brand names: `REcall Agency`, `REflexion Asia`, `PatrimoinAsia`
- The `RE` prefix represents the Real Estate ecosystem brand

**Color System:**
- Dark Navy `#1B3A5C` — primary brand
- Blue `#2E6DA4` — secondary
- Red `#C0392B` — RE prefix accent

**Taglines:**
- REcall Agency: *Where data meets intelligence. Built for real estate.*
- REflexion Asia: *Thailand real estate intelligence, engineered.* / *L'intelligence immobilière thaïlandaise, à portée de main.*
- PatrimoinAsia: *Le pont patrimonial entre l'Europe et l'Asie.*
- JP Personal: *Designing the intelligence infrastructure where real estate meets AI sovereignty.*

**Brand Voice Principles:**
- Sharp, precise language — no buzzwords
- Data-driven but not academic
- Challenges outdated models
- Outcome-focused, not feature-focused
- Signature phrases: "Engineered for performance", "Built for control", "Intelligence layer"

---

## Script Patterns

**Main Scraper Pipeline (Palanthai):**
```bash
# Single job (e.g., Phuket condos, limit 10 for testing)
python phase1_project_extractor.py --config phase1_config.yaml --job phuket_condo --limit 10

# All 10 jobs
python phase1_project_extractor.py --config phase1_config.yaml --all

# Developer directory (with detail page enrichment)
python phase1_developer_extractor.py --config phase1_config.yaml --enrich
```

**Configuration Files (YAML):**
```yaml
# Pipeline configuration (all 10 seed URLs)
# Requirements files for dependencies
```

**Health Check Pattern:**
```bash
# Output to Obsidian note
HEALTH_NOTE="/Users/phil/Documents/Vaults/SystemMac/00_System/OS_Health_Status.md"
echo "# 🖥️ macOS Health Status" > "$HEALTH_NOTE"
echo "*Dernière mise à jour : $(date '+%Y-%m-%d %H:%M:%S')*" >> "$HEALTH_NOTE"
```

---

## PARA 2.0 Organization

**Directory Purposes:**

| Directory | Purpose |
|-----------|---------|
| `00_System/` | Mac local maintenance, OS specs, scripts |
| `10_Infrastructure/` | Hostinger VPS, shared hosting, data architecture |
| `20_Projects/` | Active projects with end dates |
| `30_Knowledge/` | Permanent technical documentation, tutorials |
| `40_Context_Hub/` | Agent context window, instructions, session logs |

**Sub-Organization Examples:**
- `20_Projects/20_Reflexion_Asia/01_Identity/` — Brand assets
- `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/` — Technical specs
- `20_Projects/20_Reflexion_Asia/03_Knowledge/` — Knowledge base
- `30_Knowledge/Development/` — Development docs
- `30_Knowledge/AI_Orchestration/` — Agent configurations
- `40_Context_Hub/RE/` — Real estate content pipeline

---

## Security Conventions

**API Keys/Secrets:**
- Never hardcode in source files
- Store in `.env.local` at vault root (gitignored)
- Access via environment variables: `os.getenv("API_KEY")`
- Use `load_dotenv()` to load from `.env` files
- Reference secrets via `.env.local` lookup

**SSH Keys:**
- Key-based authentication only (no passwords)
- SSH config in `~/.ssh/config`
- Hostinger access documented in vault

**File Protection:**
- `.env` and `.env.local` always gitignored
- `00_System/Secrets/` directory gitignored
- API keys management documented in `00_System/Secrets/API_KEYS_MANAGEMENT.md`

---

## Obsidian-Specific Conventions

**Plugins Used:**
- obsidian-git — Version control
- obsidian-kanban — Task boards
- obsidian-minimal-settings — Theme settings
- obsidian-smart-links — Link management
- obsidian-checklist-plugin — Checklist tracking
- obsidian-icon-folder — Folder icons
- obsidian-excalidraw-plugin — Diagrams
- obsidian-mind-map — Mind maps
- dataview — Data queries

**Workspace Files (Gitignored):**
- `.obsidian/workspace.json` — Machine-specific
- `.obsidian/workspace-mobile.json` — Mobile-specific
- `.obsidian/graph.json` — Machine-specific

---

*Convention analysis: 2026-04-13*
