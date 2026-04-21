# Testing Patterns

**Analysis Date:** 2026-04-21

## Project Type

**This is an Obsidian markdown wiki**, not a traditional codebase. There is:
- No test suite
- No test framework
- No test files (`.test.py`, `.spec.ts`, etc.)
- No coverage requirements

---

## Wiki Quality Assurance

The WIKI_SCHEMA.md defines a **lint workflow** for quality maintenance (not testing per se):

### Lint Workflow (weekly)

Per `WIKI_SCHEMA.md`:
1. Contradictions between pages?
2. Claims outdated by new sources?
3. Orphan pages (no incoming links)?
4. Concepts mentioned without dedicated page?
5. Missing connections?

### Ingest Workflow (verification)

When adding new sources:
1. Read source in `raw/`
2. Create `sources/[slug].md` with structured summary
3. Identify entities → update `entities/[entity].md`
4. Identify concepts → create/update `concepts/[concept].md`
5. Update `index.md`
6. Add entry in `log.md`

### Query Workflow (validation)

When answering queries:
1. Read `index.md` to identify relevant pages
2. Read concerned pages
3. Synthesize response with citations `[[page]]`
4. If response is valuable → create new page in `synthesis/`

---

## Operational Testing (VPS)

Python scripts used on the VPS (in `../Palanthai/`) do have testing patterns documented elsewhere:

- Palanthai project has its own CLAUDE.md with testing guidelines
- Scripts are executed directly on VPS via SSH
- No automated test suite observed in the WIKI itself

---

## Recommendations

If this wiki evolves to include scripts or code:

**For Python scripts:**
- Use `pytest` as test runner
- Place tests in `tests/` directory adjacent to code
- Follow TDD approach (test first, then minimal implementation)
- Target 80% minimum coverage

**For any future testing framework:**
- Config file: `pytest.ini` or `pyproject.toml`
- Run all: `pytest`
- Watch mode: `pytest --watch` (pytest-watch package)
- Coverage: `pytest --cov=src --cov-report=term-missing`

---

## Current Quality Gates

**Manual verification:**
- Frontmatter completeness (created, updated, tags)
- Kebab-case file naming
- Wiki link syntax (`[[page]]` not `[text](url)`)
- Cross-reference validation (orphans check)

**No automated testing in place.**

---

*Testing analysis: 2026-04-21*