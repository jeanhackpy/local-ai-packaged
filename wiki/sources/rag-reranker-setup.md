---
created: 2026-04-05
updated: 2026-04-21
tags: [rag, reranker, fazwaz, real-estate, hybrid-search, bge, n8n]
sources: [raw/rag-reranker-setup.md]
---

## Résumé

Setup RAG indexing pour 60k URLs de propriétés FazWaz. BM25 + BGE-large embeddings dans Qdrant. Crawl4AI + BeautifulSoup + Pydantic-AI pour extraction. LlamaIndex RAG avec Jina AI live fetch.

## Points clés

- BM25 + BGE-large embeddings hybrid search dans Qdrant
- Crawl4AI + BeautifulSoup pour parsing HTML robuste
- Pydantic-AI pour extraction entitiesstructurées
- 60k property URLs indexées pour search haute performance
- Jina AI pour live fetch quand embeddings insuffisants

## Connexions

- [[entities/fazwaz]]
- [[entities/qdrant]]
- [[sources/rag-plus-reranker]]
- [[sources/palanthai-opensource-stack]]
