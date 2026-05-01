# Testing Patterns

**Analysis Date:** 2026-05-01

## Project Type

**No testing infrastructure detected in this vault.** This is primarily an Obsidian markdown vault with sub-projects containing code assets (TypeScript/React, Python) that lack test suites.

---

## Test Files

**None detected.** Searched for:
- `*.test.ts`, `*.test.tsx`, `*.spec.ts`, `*.spec.tsx`
- `*_test.py`, `test_*.py`, `conftest.py`
- `jest.config.*`, `vitest.config.*`, `pytest.ini`

---

## Next.js Projects

**Location:** `20_Projects/Active/websites redesign/{recall-agency.com,patrimonasia.com}/code/`

These are Next.js 16 + React 19 projects but have **no test files or testing configuration**.

**Available scripts:**
```bash
npm run dev      # Development server
npm run build    # Production build
npm run start    # Production server
npm run lint     # ESLint check
```

**No test runner configured.** If testing were added, Playwright is recommended for E2E testing per the user's TypeScript rules.

---

## Python Scripts

**Locations:**
- `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/content_flywheel.py` (1228 lines)
- `10_Infrastructure/VPS_Hostinger/rls_redundancy_audit.py` (414 lines)
- `10_Infrastructure/VPS_Hostinger/rls_security_audit.py` (348 lines)
- Various scripts in `00_System/Scripts/`

**No pytest configuration detected.** Scripts are executed directly on VPS via SSH, not via a test runner.

---

## Wiki Quality Assurance

The wiki uses a **lint workflow** (defined in WIKI_SCHEMA.md) for content quality:

**Weekly checks:**
1. Contradictions between pages?
2. Claims outdated by new sources?
3. Orphan pages (no incoming links)?
4. Concepts mentioned without dedicated page?
5. Missing connections?

**Ingest workflow:**
1. Read source in `raw/`
2. Create `sources/[slug].md` with structured summary
3. Identify entities update `entities/[entity].md`
4. Identify concepts create/update `concepts/[concept].md`
5. Update `index.md`
6. Add entry in `log.md`

**Query workflow:**
1. Read `index.md` to identify relevant pages
2. Read concerned pages
3. Synthesize response with citations `[[page]]`
4. If response is valuable create new page in `synthesis/`

---

## If Testing Were Added

Per user rules (common/testing.md), the recommended approach:

**TypeScript/React:**
- Framework: Playwright for E2E
- Unit tests: Vitest or Jest
- Coverage target: 80%+

**Python:**
- Framework: pytest
- Coverage target: 80%+
- Test organization: `tests/` directory adjacent to code

---

## Current Quality Gates

**Manual verification (wiki):**
- Frontmatter completeness (created, updated, tags)
- Kebab-case file naming
- Wiki link syntax (`[[page]]` not `[text](url)`)
- Cross-reference validation (orphans check)

**No automated testing in place.**

---

## Related Sub-Projects

Palanthai (`../Palanthai/`) may have its own testing patterns documented in its CLAUDE.md.

---

*Testing analysis: 2026-05-01*