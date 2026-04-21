# AI Factory for Real Estate

> Analyse transversale — NVIDIA blueprints + Palanthai stack + data flywheel research.

## Thesis

An AI factory for Thai property intelligence requires three layers working in concert: a **data flywheel** that continuously collects and labels property data, a **RAG pipeline** that makes that data queryable at scale, and **agentic workflows** that turn queries into actions (valuation, recommendations, lead qualification). The NVIDIA blueprint ecosystem — spanning observability (W&B), orchestration (MLRun), and microservices (NeMo NIM) — provides the reference architecture for each layer.

---

## 1. The Data Flywheel

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/nvidia-omniverse-dsx-blueprint]] | Digital twins for physical assets — property as a digital twin |
| [[sources/ai-orchestration-data-flywheel-mlrun]] | MLRun orchestrates the flywheel: data collection → training → evaluation → deployment |
| [[sources/ai-observability-data-flywheel-wandb]] | W&B Weave adds traceability and experiment tracking to model optimization |
| [[sources/data-pipeline-unit-recommendations]] | Concrete stack: Supabase + Qdrant + Neo4j for property recommendations |
| [[sources/palanthai-opensource-stack]] | Open-source implementation of the Thai real estate intelligence stack |

### Key insight

The Palanthai stack (Qdrant for embeddings, Neo4j for relationships, Supabase for structured data, Ollama for local inference) is a **mini AI factory** for property data. The NVIDIA blueprints show how to automate the model improvement loop: production traffic → evaluation → fine-tuning → deployment.

### Implication for Palanthai

1. **Embed feedback signals** — when users click listings, send the signal back to the vector DB
2. **Use MLRun or n8n** to orchestrate the crawl → extract → embed → evaluate pipeline
3. **Add W&B** to track embedding quality over time (Precision@K, click-through rate)

---

## 2. RAG Pipeline — Scale and Quality

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/cyborg-enterprise-rag-blueprint]] | 15x faster multimodal PDF extraction; 50% fewer incorrect answers |
| [[sources/rag-plus-reranker]] | Without reranker: 30-40% false positives. With BGE-reranker: <10% |
| [[sources/streaming-data-rag]] | Real-time streaming RAG with <5s latency for dynamic data |
| [[sources/rag-reranker-setup]] | Setup for 60k FazWaz URLs with BM25 + vector hybrid search |

### Key insight

**Embedding-only retrieval is insufficient for property queries.** A query like "3-bed condo with river view near BTS Saphan Taksin" contains geo-constraints, attribute filters, and semantic nuance that pure vector search mishandles. Cross-encoder reranking (BGE-reranker-large or ColBERT-v2) dramatically improves precision.

### Implication for Palanthai

1. Start with BGE-large embeddings → BGE-reranker-base (<50ms GPU)
2. Add BM25 hybrid search for structured attribute filtering (price range, bedrooms)
3. Only live-fetch top-8 after reranking (≥70% fewer Jina calls)
4. Store reranker scores in Qdrant payload with 6h TTL

---

## 3. Agentic Commerce — From RAG to Action

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/retail-agentic-commerce-blueprint]] | ACP/UCP protocols for agent-to-merchant communication; NeMo Agent Toolkit |
| [[sources/retail-shopping-assistant-blueprint]] | Multimodal RAG (NVClip for image similarity) + cross-sell recommendations |
| [[sources/ambient-healthcare-agents]] | Dual-agent pattern: provider (documentation) + patient (intake) |
| [[sources/build-ai-virtual-assistant-blueprint]] | NeMo Guardrails + RAG for customer service automation |
| [[sources/deal-sniper-bot]] | AI bot for real-time deal identification and alerting |

### Key insight

The NVIDIA retail blueprints demonstrate **agentic commerce**: AI agents that autonomously discover products, negotiate, complete checkouts, and deliver post-purchase experiences. For real estate, this maps to: property discovery → valuation → negotiation → transaction support. The dual-agent pattern (ambient provider + ambient patient) is directly applicable to buyer agent + seller agent.

### Implication for Palanthai

1. Build two agents: **Buyer Agent** (preferences → search → valuation → tour scheduling) and **Seller Agent** (listing quality → pricing → lead qualification)
2. Use NeMo Guardrails for content safety (no misleading price claims)
3. Start with RAG over listings; add tool-calling for calculator, calendar, messaging

---

## 4. Infrastructure Requirements

### GPU Requirements (from blueprints)

| Workload | GPUs |
|----------|------|
| Enterprise RAG (CyborgDB) | 2× H100 or 3× A100 |
| Self-hosted LLM Judge (flywheel) | 6× H100 or A100 |
| Remote LLM Judge | 2× H100 or A100 |
| Voice Agent (3 languages, <1s latency) | 3× H100 |
| Nemotron VLM (catalog enrichment) | 1× A100 |

### Thai real estate context

The Palanthai stack currently runs on a single VPS (31.97.67.145). The NVIDIA blueprints assume enterprise-scale GPU clusters. The practical path forward:
- **Phase 1**: Ollama local inference (no GPU required for small models)
- **Phase 2**: Add one A100 for reranking + embedding inference
- **Phase 3**: MLRun orchestration + W&B observability when GPU budget allows

---

## Conclusion

The AI factory for Thai real estate is not a single system — it is a stack:
1. **Data layer**: Supabase (structured) + Qdrant (vectors) + Neo4j (relationships)
2. **Retrieval layer**: BM25 + BGE embeddings + BGE-reranker for precision
3. **Model layer**: Ollama for generation, fine-tuned on Thai property corpus
4. **Agentic layer**: n8n workflows + future NeMo Agent Toolkit for autonomous actions
5. **Observability layer**: W&B for experiment tracking, n8n for operational monitoring

The NVIDIA blueprints provide the architectural template at enterprise scale; Palanthai provides the operational reality at Thai market scale.

---

**Sources**: [[sources/nvidia-omniverse-dsx-blueprint]], [[sources/ai-orchestration-data-flywheel-mlrun]], [[sources/ai-observability-data-flywheel-wandb]], [[sources/cyborg-enterprise-rag-blueprint]], [[sources/rag-plus-reranker]], [[sources/retail-agentic-commerce-blueprint]], [[sources/retail-shopping-assistant-blueprint]], [[sources/ambient-healthcare-agents]], [[sources/data-pipeline-unit-recommendations]], [[sources/palanthai-opensource-stack]]
