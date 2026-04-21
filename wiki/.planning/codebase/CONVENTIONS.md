# Coding Conventions

**Analysis Date:** 2026-04-21

## Project Type

**This is an Obsidian markdown wiki**, not a traditional codebase. There are:
- No Python, TypeScript, or JavaScript files
- No package.json, requirements.txt, or build system
- No test suite or CI/CD pipeline

Conventions documented here apply to the markdown content and operational scripts used on the VPS.

---

## Markdown Conventions

### File Naming

**Pattern:** kebab-case

```
real-estate-valuation.md
nvidia-blueprints.md
ai-orchestration-data-flywheel.md
```

**Not used:** camelCase, PascalCase, snake_case

### Frontmatter Structure

All wiki pages require YAML frontmatter:

```yaml
---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, AI, Thailand]
sources: []
---
```

**Required fields:** `created`, `updated`, `tags`
**Optional fields:** `sources`

### Content Organization

**Sections within a page:**
```markdown
## Résumé

[2-3 phrases max]

## Points clés

- ...

## Connexions

- [[entities/nvidia]]
- [[concepts/rag]]
```

---

## Directory Conventions

**Structure (per WIKI_SCHEMA.md):**
```
WIKI/
├── index.md           # Catalogue of entire wiki
├── log.md             # Chronological history
├── overview.md        # Overview / evolving thesis
├── concepts/          # Concept pages (RAG, data flywheel, agentic AI)
├── entities/          # Entity pages (NVIDIA, FazWaz, Palanthai)
├── sources/           # Source summaries
│   └── [source-slug].md
└── synthesis/         # Cross-cutting analyses
```

**Naming:** kebab-case for directories (concepts, entities, sources)

---

## Obsidian Link Patterns

**Wiki links:** `[[page-name]]`
- Points to another wiki page
- Does not use file extensions

**Examples:**
```markdown
- [[entities/nvidia]]
- [[concepts/rag]]
- [[sources/cyborg-enterprise-rag]]
```

---

## Content Conventions

### Language

- Primary: English with French comments
- French accents preserved (immobilier, thaïlandais)
- Technical terms in English when common

### Section Headers

- Use `##` for main sections
- Use `-` for bullet points (not `*`)
- Avoid numbering (flexibility for future edits)

---

## Operational Scripts (VPS)

Scripts are stored in the parent `SystemMac/` directory, not in this wiki.

**Python scripts exist in:**
- `../Palanthai/` - Property intelligence platform
- `../SystemMac/30_Knowledge/` - Agent orchestration

**Scripts follow Python conventions from:**
- `/Users/phil/Documents/Vaults/SystemMac/CLAUDE.md`
- `/Users/phil/Documents/Vaults/Palanthai/CLAUDE.md`

---

## Error Handling

**Wiki maintenance (from WIKI_SCHEMA.md):**

Lint workflow checks:
- Contradictions between pages
- Outdated claims vs new sources
- Orphan pages (no incoming links)
- Missing concept pages
- Missing connections

---

*Convention analysis: 2026-04-21*