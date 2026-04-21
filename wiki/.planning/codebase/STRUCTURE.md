# Codebase Structure

**Analysis Date:** 2026-04-21

## Directory Layout

```
SystemMac/WIKI/
├── WIKI_SCHEMA.md       # Schema for LLM agent behavior
├── overview.md          # Thesis and research axes
├── index.md            # Catalogue of all wiki content
├── log.md              # Append-only chronological history
├── raw/                # Immutable source documents (65 files)
├── concepts/           # 14 concept pages (kebab-case .md files)
├── entities/           # 2 entity pages (nvidia.md, fazwaz.md)
├── sources/            # 59 source summaries (slug-based naming)
└── synthesis/          # 2 cross-domain analyses
```

## Directory Purposes

**Root (WIKI/):**
- Purpose: Wiki entry point and schema
- Contains: Schema, overview, index, log (all .md)
- Key files: `index.md` (catalogue), `WIKI_SCHEMA.md` (LLM guide)

**raw/:**
- Purpose: Immutable source documents
- Contains: Papers, articles, blueprints, documentation
- Key files: 65 raw markdown files (nvidia blueprints, research papers, market docs)

**concepts/:**
- Purpose: Research topic pages
- Contains: 14 concept pages (agentic-ai, rag, data-flywheel, data-pipeline, etc.)
- Key files: `index.md` (concept listing), individual concept files

**entities/:**
- Purpose: Organization/platform pages
- Contains: 2 entities (nvidia, fazwaz)
- Key files: `nvidia.md`, `fazwaz.md`

**sources/:**
- Purpose: Structured summaries of raw sources
- Contains: 59 source summary documents
- Key files: slug-based naming (e.g., `rag-reranker-setup.md`, `nvidia-omniverse-dsx-blueprint.md`)

**synthesis/:**
- Purpose: Cross-domain multi-source analyses
- Contains: 2 synthesis documents
- Key files: `ai-factory-for-real-estate.md`, `thailand-property-intelligence.md`

## Key File Locations

**Entry Points:**
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/index.md` — Primary catalogue, start of query workflow
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/WIKI_SCHEMA.md` — LLM agent schema and workflows

**Configuration:**
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/WIKI_SCHEMA.md` — Schema defining 3-layer architecture and conventions

**Core Logic:**
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/overview.md` — Thesis and 5 research axes
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/log.md` — Append-only action history

**Content:**
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/concepts/*.md` — 14 concept pages
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/entities/*.md` — 2 entity pages
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/sources/*.md` — 59 source summaries
- `/Users/phil/Documents/Vaults/SystemMac/WIKI/synthesis/*.md` — 2 synthesis analyses

## Naming Conventions

**Files:**
- All files: kebab-case (e.g., `real-estate-valuation.md`, `ai-factory-for-real-estate.md`)
- Source summaries: slug from source filename (e.g., `rag-reranker-setup.md` from `rag-reranker-setup.md` in raw)

**Directories:**
- All directories: lowercase, hyphenated (concepts, entities, sources, synthesis, raw)

**Wiki Links:**
- Obsidian `[[wiki/file-name]]` format (e.g., `[[concepts/rag]]`, `[[entities/nvidia]]`)

**Frontmatter (required on all wiki pages):**
```yaml
---
created: YYYY-MM-DD
updated: YYYY-MM-DD
tags: [concept, AI, Thailand]
sources: [raw/filename.md]
---
```

## Where to Add New Code

**Note:** This is a markdown knowledge wiki, not a code project. There is no implementation code.

**New Source Document:**
- Primary: `raw/` directory
- Summary: `sources/[slug].md`

**New Concept Page:**
- Implementation: `concepts/[concept-name].md`
- Must include frontmatter and connections to existing concepts/entities

**New Entity Page:**
- Implementation: `entities/[entity-name].md`

**New Synthesis:**
- Implementation: `synthesis/[synthesis-name].md`
- Triggered when query response is valuable enough to persist

## Special Directories

**raw/:**
- Purpose: Immutable source documents
- Generated: No (user-managed)
- Committed: Yes (version controlled in git)

**sources/:**
- Purpose: LLM-generated summaries of raw sources
- Generated: Yes (by LLM during ingest)
- Committed: Yes

**synthesis/:**
- Purpose: Cross-domain analyses
- Generated: Yes (by LLM during valuable query responses)
- Committed: Yes

---

*Structure analysis: 2026-04-21*