# Technology Stack

**Analysis Date:** 2026-04-21

## Languages

**Primary:**
- Markdown - Vault documentation (concepts, sources, synthesis documents)
- Python - Pipeline scripts (scraping, extraction, embedding, ETL)
- JavaScript/TypeScript - n8n workflows, potential frontend components

## Runtime

**Environment:**
- Python venv at `/home/phil/venv` on VPS (31.97.67.145)

**Package Manager:**
- pip (Python)
- npm (Node.js for n8n)

## Frameworks

**Core:**
- Pydantic/Pydantic-AI - Structured data extraction from raw HTML
- LlamaIndex - RAG framework for property queries
- Crawl4AI - Web scraping with AI extraction capabilities
- BeautifulSoup - HTML parsing fallback

**Data Storage:**
- Qdrant - Vector embeddings storage (HNSW index)
- Neo4j - Property relationship graph (project, building, unit hierarchy)
- Supabase - PostgreSQL for structured data, auth, edge functions

**AI Inference:**
- Ollama - Local LLM inference (privacy, cost reduction)
- BGE-large - Text embeddings model
- BGE-reranker - Cross-encoder reranking for retrieval precision

**Workflow:**
- n8n - Workflow automation and orchestration (sitemap monitoring, webhook triggers)

**Observability:**
- Weights & Biases (W&B) - Experiment tracking for data flywheel
- MLRun - Pipeline orchestration for AI factory

## Key Dependencies

**Critical:**
- `pydantic` - Data validation schemas (PropertyDoc model)
- `llama-index` - RAG pipeline implementation
- `crawl4ai` - AI-powered web crawler
- `qdrant-client` - Vector DB client

**Infrastructure:**
- `neo4j` - Graph database driver
- `supabase` / `postgresql` - Structured data store
- `ollama` - Local model serving

**Embeddings & Retrieval:**
- `sentence-transformers` (BGE models) - Text vectorization
- `Jina AI` - Live document fetching when embeddings insufficient

## Configuration

**Environment:**
- VPS environment variables at `/home/phil/palanthai/config/.env`
- Supabase project credentials
- Qdrant connection (VPS port 6333)
- Neo4j connection credentials

**Build:**
- No traditional build system (Obsidian vault)
- Python scripts run directly via SSH on VPS

## Platform Requirements

**Development:**
- Obsidian vault for documentation
- SSH access to VPS for script execution

**Production:**
- VPS (31.97.67.145) Ubuntu 24.04
- Supabase cloud (PostgreSQL, Auth, Edge Functions)
- Qdrant self-hosted on VPS
- Neo4j self-hosted on VPS
- Ollama local inference

---

*Stack analysis: 2026-04-21*