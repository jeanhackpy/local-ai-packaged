# 🐍 Palanthai Scripts Index

> Symlinks to active pipeline scripts in `rato-sequencer-condominium/`

---

## SIAM Module (Extraction)
- [[phase1_project_extractor.py]] — Main project crawler (10 seed URLs, JSON-LD + CSS, **Pydantic validated**, Cloudflare bypass)
- [[phase1_developer_extractor.py]] — Developer directory (1519 devs, 16 pages)
- [[phase1_faq_extractor.py]] — FazWaz FAQ knowledge base

### Pydantic Models (in phase1_project_extractor.py)
- `ProjectRecord` — Canonical output schema, enforces `facilities: List[str]` (full names, never counts)
- `GeoLocation` — Lat/lng validation (range check, both-or-neither)
- `StructuredAddress` — JSON-LD address fields
- `PriceRange` — Min/max with auto-swap if inverted

## CHANG Module (Storage)
- [[v2_pipeline_orchestrator.py]] — Unified DB export (Supabase + Qdrant + Neo4j)

## LANNA Module (Visualization)
- [[v2_dashboard_generator.py]] — Interactive HTML dashboard (Chart.js)

## Config
- `phase1_config.yaml` — Pipeline configuration (all 10 seed URLs)
- `requirements.txt` — Python dependencies

---

## Run Commands

```bash
# Single job (e.g., Phuket condos, limit 10 for testing)
python phase1_project_extractor.py --config phase1_config.yaml --job phuket_condo --limit 10

# All 10 jobs
python phase1_project_extractor.py --config phase1_config.yaml --all

# Developer directory (basic)
python phase1_developer_extractor.py --config phase1_config.yaml

# Developer directory (with detail page enrichment)
python phase1_developer_extractor.py --config phase1_config.yaml --enrich

# FAQ knowledge base
python phase1_faq_extractor.py --config phase1_config.yaml
```
