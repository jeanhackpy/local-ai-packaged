---
created: 2026-04-21
updated: 2026-04-21
tags: [concept, data-pipeline, ETL, streaming, batch, real-estate]
sources: [raw/data-pipeline-unit-recommendations.md, raw/data-processing.md, raw/dataflow-architecture.md]
---

## Data Pipeline

The infrastructure that moves property data from source systems through transformation into AI-ready formats. Combines streaming (real-time) and batch (periodic) patterns.

### Architecture

**Core stack**: Supabase (structured DB + PostgreSQL) + Qdrant (vector store) + Neo4j (knowledge graph)

| Component | Role |
|-----------|------|
| Supabase | Structured property data, user data, feedback signals |
| Qdrant | Vector embeddings of listing text, images, floor plans |
| Neo4j | Property relationships: project → building → unit, location graph |

### Pipeline Patterns

1. **Batch ETL** — nightly crawl → extract → normalize → embed → index
2. **Incremental** — sitemap monitoring with lastmod + SHA-1 hash for change detection
3. **Streaming** — live price updates, new listings, viewing bookings via webhooks
4. **Feedback loop** — user clicks → store signal → retrain embeddings weekly

### Crawl Architecture (per rag-reranker-setup)

```
Sitemap monitor (n8n) → Crawl workers (Crawl4AI) → Pydantic-AI (PropertyDoc) →
Postgres (BM25) + Qdrant (HNSW) → Hybrid search → LLM → Answer + listings
```

## Sources

- [[sources/data-pipeline-unit-recommendations]]
- [[sources/data-processing]]
- [[sources/dataflow-architecture]]

## Connexions

- [[concepts/data-flywheel]] — pipeline feeds continuous model improvement
- [[concepts/rag]] — pipeline output feeds retrieval
- [[concepts/knowledge-extraction]] — extraction from raw crawl data
