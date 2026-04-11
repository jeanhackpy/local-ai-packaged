---
created: 2026-04-05
updated: 2026-04-05
tags: [RAG, reranker, FazWaz, hybrid-search]
---

## Résumé

Guide complet pour setup RAG indexing de 60k URLs FazWaz. Architecture avec sitemap parsing → crawl → embedding → hybrid search → live refresh layer.

## Points clés

### Stack recommandé
- **Crawl** : Crawl4AI + BeautifulSoup
- **Schema** : Pydantic-AI → PropertyDoc
- **Embed** : E5-large-v2 ou BGE-Large
- **Vector DB** : Qdrant (HNSW)
- **Search** : BM25 + vector → MMR re-rank
- **Live** : r.jina.ai pour refresh données volatiles
- **LLM** : Llama-3-70B local via LlamaIndex
- **Orchestration** : Supabase + Grafana

### Différenciateur
- Static vs dynamic data separation
- 30% boost pertinence vs vector-only
- P95 latency < 2.5s

## Connexions

- [[entities/fazwaz]]
- [[concepts/rag]]
- [[concepts/immobilier-thailand]]
