---
created: 2026-03-30
tags:
  - "rag"
  - "reranking"
  - "real-estate"
  - "hybrid-search"
  - "bge-reranker"
  - "cross-encoder"
---

# RAG + Reranker

Strategic guidance on RAG setup for real estate property indexing with hybrid search and reranking for lead queries.

## Executive Summary

A good reranker changes the game — especially when prospects ask nuanced queries ("3-bed condo with river view near BTS Saphan Taksin").

- **Without reranker**: top-K from simple embedding contains often 30-40% false positives
- **With cross-encoder reranker**: drop under 10% noise, increase click-through and reduce costs

## Architecture Overview

```
mermaid
flowchart TD
    A[Sitemap monitor<br/>(n8n)] --> B(Crawl workers<br/>Crawl4AI)
    B --> C(Pydantic‑AI<br/>PropertyDoc)
    C --> D1[Postgres<br/>BM25] & D2[Qdrant<br/>HNSW]
    E(Lead prompt<br/>NL query) --> F(Hybrid search<br/>MMR)
    F --> G{Top‑K URLs}
    G --> H[Live fetch<br/>Jina AI]
    H --> I[LlamaIndex RAG]
    I --> J(Answer +<br/>listings cards)
    J --> Supabase[Feedback store]
```

## Tech Stack

| Stage | Technology | Notes |
|-------|-------------|-------|
| Sitemap parsing | n8n + HTTP Request | Incremental via `<lastmod>` + SHA-1 hash |
| Crawl & Extraction | Crawl4AI + BeautifulSoup | CSS rules in YAML |
| Structuration | Pydantic-AI | PropertyDoc model |
| Embedding | E5-large-v2 or BGE-Large | Qdrant (HNSW) |
| Hybrid Search | BM25 + Vector | MMR re-rank |
| Live Refresh | FastAPI middleware | Jina AI API for volatile fields |
| Generation | Llama-3-70B-Instruct-Q4_K_M | Local via LlamaIndex |
| Orchestration | Supabase + Grafana/Prometheus | |

## Reranking Options (2025)

| Reranker | Strengths | Precision@5 | Latency/20 docs | License |
|----------|-----------|-------------|-----------------|----------|
| **BGE-reranker-large** | Multilingual (fr+en), 335M params | ⭐⭐⭐⭐ | 90ms | MIT |
| **FlashRank** (mxbai-rerank-v1) | Quantized, CPU-friendly | ⭐⭐⭐ | 130ms CPU | Apache-2.0 |
| **ColBERT-v2** | Late-interaction, reindexable | ⭐⭐⭐⭐ | 60ms (GPU) | MIT |
| **RankLLM** (GPT-4o listwise) | SOTA but expensive | ⭐⭐⭐⭐⭐ | 350ms API | Apache-2.0 |

## Why Embeddings Alone Are Not Enough

1. **Structured details** (max price, bedrooms) are poorly weighted in bi-encoders
2. **Geo constraints**: "near Wat Priwat BRT" ↔ 5km is "close" for humans, not for models
3. **Marketing noise**: descriptions full of superlatives dilute the signal

Cross-encoders read *query+document* together: they capture these fine details and fold false positives.

## Actionable Recommendations

### Start Simple
1. Top-40 via BGE-embedding
2. Rerank with `bge-reranker-base` (110M) via `rerankers` lib → <50ms GPU
3. Measure: `Precision@5`, `TTFB`

### Scale Up
1. Switch to *bge-reranker-large* or *ColBERT-v2* if expanding to 600k properties
2. Batch re-ranking in vLLM: `tensor_parallel_size=2`

### Fail-Safe Latency
1. Timeout 150ms; if exceeded, fall back to embedding score
2. Store reranker score in Qdrant payload to avoid recalculation (TTL = 6h)

### Optimize Jina API
1. Do live fetch **only** on top 8 after rerank → ≥70% fewer Jina calls

### A/B Test
1. 10% traffic without rerank as control group
2. Metrics: *CTR listings card*, *conversion email/magic-link*, *cost per qualified lead*

## Success Metrics

| Metric | Target |
|--------|--------|
| Precision@5 | ≥ 0.80 |
| TTFB chatbot | < 2.5s (95th pct) |
| Jina calls/lead | ≥ 40% reduction |
| "Relevant matches" rated by prospect | ≥ 4/5 |

## Related

- [[cyborg-enterprise-rag-blueprint]]
- [[rag-concept]]
- [[from-transcripts-to-ai-agents]]

---
*Source: [ChatGPT Conversation](
