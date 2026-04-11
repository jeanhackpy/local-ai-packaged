# 🏰 LANNA — Frontend PRD Summary
> Full documents live in: `~/Documents/main_scraper/lanna-frontend/`

---

## Files for Claude Code

| File | Purpose | Location |
|---|---|---|
| `PLANNING.md` | Full architecture, tech stack, DB schema, component tree, design system | `lanna-frontend/PLANNING.md` |
| `TASK.md` | Sprint tasks (S1–S4), backlog, progress tracking | `lanna-frontend/TASK.md` |
| `CLAUDE.md` | Global rules for Claude Code (Supabase, Mapbox, TypeScript, testing) | `lanna-frontend/CLAUDE.md` |

---

## How to Use with Claude Code

1. **Open Claude Code** in the `lanna-frontend/` directory
2. **First message in every session**: _"Read PLANNING.md and TASK.md first."_
3. **Pick one task** from Sprint 1 in TASK.md
4. **Use the First Prompt Template** at the bottom of CLAUDE.md
5. **After each task**: update TASK.md (Claude Code should do this automatically per CLAUDE.md rules)

---

## Sprint Overview

| Sprint | Focus | Est. Time |
|---|---|---|
| S1 | Foundation: scaffold, types, landing page, project grid + detail | 1–2 weeks |
| S2 | Interactive Mapbox map with markers, clustering, filters | 1 week |
| S3 | AI Chat agent (Claude API + Qdrant RAG) | 1 week |
| S4 | Market intelligence dashboard (charts, developer pages) | 1 week |

---

## Key Context from Google Drive

- **[Full AI Coding Workflow Guide](https://docs.google.com/document/d/1NVBuHCLVJXilxdgJ1AB5qTg-bcJ-Sljw6r7VoauhjU4)** — Golden rules incorporated into CLAUDE.md
- **Reflection.Asia PropTech folder** (`1thj_rFSZBF5uDZotg-YKT_8xRtz-L0py`) — Business strategy context
- **AI Infrastructure SOP** (`1E6JYLgNWSzfDCOJ_LC_uoyGPY7VHcgWsdiwj3tR5vGk`) — Deployment & infra guide

---

## Tech Decisions (final)

- **Next.js 14** (App Router) — not Vite/CRA
- **Mapbox GL JS** — not Leaflet, not Google Maps (3D buildings, WebGL performance)
- **Supabase JS v2** — typed client, RLS, realtime
- **Zustand** — not Redux, not Context (filter state, map state)
- **TanStack Query** — not SWR, not raw useEffect
- **Vercel** — deployment (zero-config Next.js)
