# WIKI Overview

> Vue d'ensemble évolutive du wiki. Thèse et axes de recherche.

---

## Thesis

This wiki documents the intersection of **AI/ML applied to Thai real estate** — specifically the data infrastructure, models, and workflows needed to build a property intelligence platform. The core question: how do you build an AI system that understands Thai properties well enough to value, recommend, and broker them?

## Axes de recherche

### 1. Property Intelligence Stack

Thai real estate is data-sparse and fragmented — FazWaz lists 60k+ units with poor structured data. The Palanthai stack (Qdrant + Supabase + Ollama) addresses this with a pipeline: crawl → extract → embed → query. **Neo4j est INACTIF** — réactivation nécessaire pour NAGA knowledge graph. **Ollama Docker est STOPPED**. Le Palanthai API v2.0.0 tourne sur port 8500 (systemd). Le data flywheel pattern (NVIDIA blueprints + MLRun + W&B) est l'architecture de référence pour améliorer le pipeline.

### 2. Valuation Models

Academic research on property valuation (multi-modal deep learning, GCN floor plans, satellite imagery, self-supervised ViT) converges on one insight: **no single modality is sufficient**. The best results combine structured attributes + text descriptions + images + geo-spatial context. Palanthai's open-source stack is the operationalization of this insight.

### 3. Agentic Commerce

The NVIDIA retail blueprints (shopping assistant, agentic commerce, catalog enrichment) are the template for how property agents should work: RAG over listings, multi-turn conversations, multimodal retrieval, and eventually autonomous transaction support. The RAG + reranker setup (BGE + ColBERT-v2) is the concrete implementation for the 60k-unit FazWaz corpus.

### 4. Trust Infrastructure

Real estate is trust-heavy. The "Architecture of Trust" framework (UAD 3.6) and trust-infrastructure-data source define what it means to be honest in property valuation: provenance of data, uncertainty quantification, and transparency about what the model doesn't know.

### 5. Thai Market Specifics

Sansiri's PRD, FazWaz Premium, and the deal sniper bot capture the realities of the Thai market: developer-heavy supply, dual-language marketing, BTR/condo differentiation, and the role of local agents vs. platforms.

---

*Last updated: 2026-04-21*
