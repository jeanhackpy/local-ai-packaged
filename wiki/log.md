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

## Stats

- **Sources ingérées** : 35/51
- **Concepts** : 8
- **Entities** : 2
