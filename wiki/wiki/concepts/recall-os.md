---
created: 2026-05-14
updated: 2026-05-14
tags: [concept, project, recall, reflexion, patrimonasia, real-estate, AI]
sources: [raw/Project_Blueprint.md, raw/gemini-obsidian/daily_interactions/2025-07-03.md]
---

## REcall OS

**Vision**: Build the definitive intelligent infrastructure for real estate in Southeast Asia, starting with Thailand — a "Palantir for Real Estate."

### Three Brands

1. **REcall Agency** — Technology & cybersecurity core. High-end consultancy building the ecosystem.

2. **Reflexion.asia** — Flagship B2C/B2B platform for Thailand. Premium marketplace powered by REcall OS.

3. **Patrimonasia.com** — B2B bridge connecting European investors to Thai real estate market.

### Technical Stack

- **Frontend**: Next.js + TailwindCSS + shadcn/ui
- **Backend**: Supabase (PostgreSQL), Qdrant (vectors), Neo4j (graphs), Redis
- **AI**: OpenRouter + Ollama (local for sensitive data)
- **Orchestration**: n8n, LangGraph/Flowise
- **Data Pipeline**: Crawl4AI + Pydantic
- **3D**: Unreal Engine 5 + Cesium

### Launch Strategy

21-day MVP:
1. **Days 1-3**: Minimal Reflexion.asia landing page + lead capture
2. **Days 4-10**: Crawl4AI pipeline → 200-800 clean listings
3. **Days 11-21**: Onboard 20 agents + "man-behind-curtain" AI

### Key Features

- Intelligent Onboarding Quiz (swipe-based profiling)
- AI Real Estate Expert Agent (RAG on SQL + vector + graph DB)
- Agent Matching & Co-Brokerage Engine ("AI Broker Graph")
- Reputation Shield (B2B cybersecurity for agencies)
- Immersive 3D/AR/VR Layer (UE5 + Cesium digital twins)
- Web3 Integration (blockchain for agent action logging, DID auth)

### Security Architecture

- Namespace isolation in Qdrant
- Row-level security in Supabase
- Session-scoped AI memory
- JWT + Magic Links via Supabase Auth

## Sources

- [[raw/Project_Blueprint]] — Full blueprint document
- [[raw/gemini-obsidian/daily_interactions/2025-07-03]] — Daily interaction log
- [[sources/roadmap-2026]] — 12-month strategic roadmap
- [[sources/gemini-blackboard]] — Project analysis summary
- [[sources/thailand-luxury-real-estate-2025]] — Luxury market context

## Connexions

- [[entities/nvidia]] — AI blueprints reference
- [[concepts/rag]] — RAG architecture for AI agent
- [[concepts/data-pipeline]] — Crawl4AI data pipeline
- [[concepts/immobilier-thailand]] — Thailand market focus
- [[sources/blockchain-crypto-moc]] — Web3 integration reference
- [[sources/cybersecurity-osint-moc]] — Security architecture reference