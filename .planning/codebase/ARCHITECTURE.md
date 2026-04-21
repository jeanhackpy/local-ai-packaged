# Architecture

**Analysis Date:** 2026-04-21

## Pattern Overview

**Overall:** LLM-maintained knowledge wiki with 3-layer architecture (raw sources → processed wiki → cross-domain synthesis)

**Key Characteristics:**
- Immutable source layer (raw/) read-only by LLM
- Structured wiki layer (concepts/, entities/, sources/) maintained by LLM agents
- Cross-domain synthesis layer (synthesis/) for multi-source analyses
- Schema-driven content management (WIKI_SCHEMA.md as guide)

## Layers

**Raw Sources Layer:**
- Purpose: Immutable source documents for AI/ML research on Thai real estate
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/raw/`
- Contains: 65 source files (papers, articles, documentation, blueprints)
- Depends on: Nothing (root layer)
- Used by: LLM for ingestion and reference

**Wiki Processing Layer:**
- Purpose: Structured knowledge extracted from raw sources
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/`
- Contains: `concepts/`, `entities/`, `sources/`
- Depends on: Raw sources
- Used by: Query workflow, cross-domain synthesis

**Synthesis Layer:**
- Purpose: Cross-domain analyses connecting multiple sources
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/synthesis/`
- Contains: 2 synthesis documents (ai-factory-for-real-estate, thailand-property-intelligence)
- Depends on: Wiki processing layer
- Used by: Research queries, planning

## Data Flow

**Ingest Workflow:**
1. Raw source file placed in `raw/`
2. LLM reads source, creates `sources/[slug].md` summary
3. LLM identifies entities → updates `entities/[entity].md`
4. LLM identifies concepts → creates/updates `concepts/[concept].md`
5. LLM updates `index.md` catalogue
6. LLM appends entry to `log.md`

**Query Workflow:**
1. Read `index.md` to identify relevant pages
2. Read concerned pages
3. Synthesize response with `[[page]]` citations
4. If response is valuable → create new synthesis page

**Lint Workflow (weekly):**
- Check contradictions between pages
- Check outdated claims vs new sources
- Find orphan pages (no incoming links)
- Identify concepts without dedicated pages
- Find missing connections

## Key Abstractions

**Concept Page:**
- Purpose: Represents a research topic (RAG, data flywheel, property valuation)
- Examples: `concepts/rag.md`, `concepts/data-pipeline.md`, `concepts/agentic-ai.md`
- Pattern: Frontmatter (created, updated, tags, sources) + structured content with connections

**Entity Page:**
- Purpose: Represents an organization, tool, or platform
- Examples: `entities/nvidia.md`, `entities/fazwaz.md`
- Pattern: Company/platform overview with related concepts

**Source Summary:**
- Purpose: Structured summary of raw source document
- Examples: `sources/rag-reranker-setup.md`, `sources/nvidia-omniverse-dsx-blueprint.md`
- Pattern: 2-3 sentence summary + key points + connections

**Synthesis Document:**
- Purpose: Cross-domain analysis connecting multiple sources
- Examples: `synthesis/ai-factory-for-real-estate.md`, `synthesis/thailand-property-intelligence.md`
- Pattern: Thesis statement + evidence table + implications + conclusion

## Entry Points

**Wiki Index:**
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/index.md`
- Triggers: Query workflow starts here
- Responsibilities: Catalog all wiki content, link to concepts/entities/sources

**Wiki Schema:**
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/WIKI_SCHEMA.md`
- Triggers: Ingest workflow, LLM behavior guidance
- Responsibilities: Define file organization, naming conventions, workflow patterns

**Overview:**
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/overview.md`
- Triggers: High-level orientation
- Responsibilities: Thesis statement, 5 research axes, last updated timestamp

**Log:**
- Location: `/Users/phil/Documents/Vaults/SystemMac/WIKI/log.md`
- Triggers: Append-only after any wiki change
- Responsibilities: Chronological history of all ingests, restructures, queries

## Error Handling

**Strategy:** Append-only log with explicit action tracking

**Patterns:**
- Each ingest logs: source file, entities found, concepts identified, actions taken
- Each restructure logs: actions taken, stats (file counts per category)
- Log enables audit trail for contradictions detection in lint workflow

## Cross-Cutting Concerns

**Logging:** Chronological log.md append-only history
**Validation:** Frontmatter required on all wiki pages (created, updated, tags, sources)
**Linking:** Obsidian `[[wiki/file-name]]` format for cross-references
**Naming:** kebab-case for all files (`real-estate-valuation.md`, `ai-factory-for-real-estate.md`)

---

*Architecture analysis: 2026-04-21*