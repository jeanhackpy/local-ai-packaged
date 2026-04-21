# External Integrations

**Analysis Date:** 2026-04-21

## APIs & External Services

**Web Scraping:**
- FazWaz - Primary property listings source (60k+ units)
- DDProperty - Secondary Thai property platform
- Hipflat - Thai property listings
- Baania - Thai property data source
- Crawl4AI - AI-powered web crawler with built-in extraction

**AI/ML Services:**
- Ollama - Local LLM inference (self-hosted on VPS)
- OpenRouter - API routing with `:free` suffix for free models
- Jina AI - Live document fetching for reranking (<5s latency requirement)

**Embedding Models:**
- BGE-large - Text embeddings (self-hosted via sentence-transformers)
- BGE-reranker - Cross-encoder for retrieval precision improvement

## Data Storage

**Databases:**
- Qdrant - Vector store (VPS port 6333)
  - Connection: `http://31.97.67.145:6333`
  - Index type: HNSW for property embeddings
- Neo4j - Graph database for property relationships
  - Connection: VPS-hosted
  - Schema: project -> building -> unit, location graph
- Supabase - PostgreSQL cloud
  - Connection: Via environment variables
  - Features: Structured property data, user data, auth, edge functions

**File Storage:**
- Local filesystem on VPS
- WordPress (92.113.28.34:65002) - reflexion.asia, recall-agency.com publishing

## Authentication & Identity

**Auth Provider:**
- Supabase Auth - User authentication for Palanthai platform

## Monitoring & Observability

**Error Tracking:**
- Not explicitly detected in documentation

**Logs:**
- Operational logs in `Palanthai/logs/` directory
- n8n workflow execution logs

**Experiment Tracking:**
- Weights & Biases (W&B) - Embedding quality tracking (Precision@K, click-through rate)
- MLRun - Pipeline orchestration logging

## CI/CD & Deployment

**Hosting:**
- Hostinger VPS (31.97.67.145) Ubuntu 24.04
- Shared hosting for WordPress sites (92.113.28.34:65002)

**CI Pipeline:**
- n8n for workflow automation
- Manual deployment via SSH

## Environment Configuration

**Required env vars:**
- Supabase connection credentials
- Qdrant connection URL
- Neo4j credentials
- Ollama endpoint
- OpenRouter API key (for model routing)

**Secrets location:**
- `/home/phil/palanthai/config/.env` on VPS
- `.env.local` in SystemMac (documented in CLAUDE.md)

## Webhooks & Callbacks

**Incoming:**
- n8n webhook triggers for sitemap monitoring
- Real-time price updates via webhooks
- New listing notifications

**Outgoing:**
- Property data syndication (FazWaz 10-portal network)
- WordPress publishing pipeline

---

*Integration audit: 2026-04-21*