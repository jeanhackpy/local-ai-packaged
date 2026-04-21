# Wiki Log

> Historique chronologique du wiki. Append-only.

```bash
# Dernières 5 entrées
grep "^## \[" wiki/log.md | tail -5

# Stats
grep -c "^## \[" wiki/log.md
```

---

## [2026-04-05] setup | Initialisation du wiki

**Type** : setup

**Actions** :
- Structure créée : raw/, wiki/, wiki/concepts/, wiki/entities/, wiki/sources/, wiki/synthesis/
- 51 fichiers déplacés vers raw/
- WIKI_SCHEMA.md créé
- wiki/index.md + wiki/log.md créés

---

## [2026-04-05] ingest-batch-1 | 3 sources initiales

**Sources** : NVIDIA DSX, Deloitte, FazWaz

---

## [2026-04-05] ingest-batch-2 | 17 sources

**Sources NVIDIA** : Virtual assistant, Healthcare agents, Retail blueprints, Voice agent, Security, Streaming RAG, Catalog enrichment

**Sources RAG** : Cyborg, RAG+Reranker, AI observability, AI orchestration, Transcripts

**Sources Thailand** : DealSniper, Extracteur, Ontologie, Palanthai, Sansiri, YC SPITCH, Trust

---

## [2026-04-05] ingest-batch-3 | 15 sources

**Research** : Multi-modal, GCN, ViT, Satellite Thailand, Building condition, Price forecasting, Rotterdam, Ensemble

**Divers** : Architecture of Trust, Service quality, Data pipeline, Neuro-symbolic, Digital twins, Custom instructions

---

## [2026-04-05] concepts | 6 concepts créés

- agentic-ai, rag, data-flywheel, digital-twins
- property-valuation, computer-vision, immobilier-thailand, trust

---

## [2026-04-21] merge-consolidation | Merged Clippings + WIKI, restructured, created syntheses

**Type** : restructure

**Actions** :
- Restructured WIKI/ to match Clippings WIKI_SCHEMA.md
- Created WIKI/raw/ (65 raw sources moved from WIKI/sources/)
- Created WIKI/synthesis/ with 2 cross-source analyses
- Created WIKI/WIKI_SCHEMA.md (copied from Clippings/)
- Created WIKI/overview.md (thesis and research axes)
- Added 6 new concepts: voice-ai, security, urban-analysis, vlm, knowledge-extraction, data-pipeline
- Updated WIKI/index.md with full catalogue

**Stats post-merge** :
- **raw/** : 65 sources
- **sources/** : 0 summaries (in progress)
- **concepts/** : 14 (8 original + 6 new)
- **entities/** : 2
- **synthesis/** : 2 (ai-factory-for-real-estate, thailand-property-intelligence)

---

## [2026-04-21] ingest-full | 55 sources summaries ingested

**Type** : ingest

**Actions** :
- 22 NVIDIA blueprint source summaries created in sources/
- 33 Thailand/AI-ML/Research source summaries created in sources/

**Stats**:
- **Sources ingérées** : 55/65
- **Concepts** : 8
- **Entities** : 2
