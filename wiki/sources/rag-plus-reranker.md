---
created: 2026-04-05
updated: 2026-04-21
tags: [rag, reranker, real-estate, hybrid-search, cross-encoder, bge]
sources: [raw/rag-plus-reranker.md]
---

## Résumé

Setup stratégique RAG + reranker pour immobilier. Sans reranker : 30-40% false positives. Avec BGE-reranker : <10%. BGE-reranker-large ou ColBERT-v2 pour échelle 600k propriétés. Stratégie fallback pour latence.

## Points clés

- Hybrid search (dense + sparse) sans reranker : 30-40% false positives
- BGE-reranker-large réduit false positives à <10%
- ColBERT-v2 pour scale 600k propriétés avec bonne latency
- Fallback strategy : direct search si reranker timeout
- Critique pour production RAG systems fiabilité

## Connexions

- [[sources/rag-reranker-setup]]
- [[entities/qdrant]]
- [[sources/from-transcripts-to-ai-agents]]
