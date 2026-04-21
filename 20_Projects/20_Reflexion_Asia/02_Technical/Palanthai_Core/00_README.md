# 🏯 PALANTHAI — Thai Real Estate Intelligence Platform

> *"Seeing stone for the Land of Smiles"*
> Palantir (all-seeing stone) × Thailand = **Palanthai**

---

## Module Architecture (Palantir → Palanthai Mapping)

| Palantir Module | Palanthai Module | Nom Thaï | Fonction |
|:---|:---|:---|:---|
| **Gotham** | **SIAM** 🗺️ | สยาม (Siam) | **S**craping **I**ntelligence & **A**cquisition **M**odule — Crawlers, extractors, ETL pipelines |
| **Foundry** | **CHANG** 🐘 | ช้าง (Éléphant) | **C**entral **H**ub for **A**ggregation, **N**ormalization & **G**overnance — Supabase, Qdrant, Neo4j |
| **Ontology** | **NAGA** 🐉 | นาค (Nāga) | **N**ode-based **A**rchitecture for **G**raph & **A**nalysis — Knowledge graph, entity resolution, dedup |
| **AIP** | **GARUDA** 🦅 | ครุฑ (Garuda) | **G**enerative **A**I-**R**eady **U**nified **D**ata **A**ccess — LLM integration, RAG, semantic search |
| **Apollo** | **KINNAREE** 💃 | กินรี (Kinnaree) | **K**ey **IN**sights, **N**otifications & **A**utomated **R**eporting **E**ngine — Market intel, due diligence, alerts |
| **Metropolis** | **LANNA** 🏰 | ล้านนา (Lanna) | **L**ive **A**nalytics, **N**otification & **N**avigation **A**pp — Frontend: chat, 3D maps, dashboards |

---

## Architecture Overview

```
┌─────────────────────────────────────────────────────────────────┐
│                    🏯 PALANTHAI Platform                        │
├─────────────────────────────────────────────────────────────────┤
│                                                                 │
│  ┌──────────┐   ┌──────────┐   ┌──────────┐   ┌──────────┐    │
│  │ 🗺️ SIAM  │──▶│ 🐘 CHANG │──▶│ 🐉 NAGA  │──▶│ 🦅 GARUDA│    │
│  │ Extract  │   │ Store    │   │ Graph    │   │ AI/RAG   │    │
│  └──────────┘   └──────────┘   └──────────┘   └──────────┘    │
│       │              │              │              │            │
│       ▼              ▼              ▼              ▼            │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              💃 KINNAREE — Intelligence               │      │
│  │  Market Reports │ Due Diligence │ Price Alerts       │      │
│  └──────────────────────────────────────────────────────┘      │
│       │                                                        │
│       ▼                                                        │
│  ┌──────────────────────────────────────────────────────┐      │
│  │              🏰 LANNA — Frontend                      │      │
│  │  Chat Agent │ 3D Map │ Dashboard │ Reports           │      │
│  └──────────────────────────────────────────────────────┘      │
│                                                                 │
└─────────────────────────────────────────────────────────────────┘
```

---

## Data Sources — Phase 1

### Primary: LivePhuket.com
- **10 Seed URLs**: 5 destinations × 2 types (condo/villa)
- **1,519 Developers**: Full directory extraction
- **JSON-LD goldmine**: Lat/Lng, structured amenities, priceRange in Schema.org format
- Destinations: Bangkok, Phuket, Koh Samui, Pattaya, Hua Hin

### Secondary: FazWaz.com
- **FAQ Knowledge Base**: Full article extraction for RAG

### Financial: SET Thailand (Stock Exchange)
- **PropCon Sector**: `https://www.set.or.th/en/market/index/set/propcon/prop`
- Tickers: AP, AWC, CPN, LH, ORI, PSH, SIRI, SPALI, etc.
- Data: Market cap, P/E, dividends, quarterly financials

### Macro: Bank of Thailand
- REIC (Real Estate Information Center) reports
- Housing price index, construction permits
- Loan-to-value ratios, mortgage statistics

### Research: CBRE Thailand
- Market studies (PDF extraction)
- Quarterly property market outlook

### Regulatory: EIA / Construction Permits
- Environmental Impact Assessment databases
- Building permit records

---

## Phase Roadmap

### Phase 1 — Structured Extraction ✅ (Current)
- [x] SIAM crawler engine (crawl4ai + JSON-LD)
- [x] 10 seed URL pipeline
- [ ] Developer directory (1,519 devs)
- [ ] FazWaz FAQ extraction
- [ ] CHANG database schema v2 (with lat/lng native)
- [ ] KINNAREE SET Thailand connector

### Phase 2 — Multi-Marketplace
- [ ] DDProperty, Hipflat, PropertyHub, Thailand-Property
- [ ] Unit-level extraction (surface, price, floor, exposure, title)
- [ ] Sitemap.xml-based discovery
- [ ] Cross-platform price comparison engine

### Phase 3 — Intelligence Layer
- [ ] GARUDA RAG pipeline (Qdrant + LLM)
- [ ] NAGA entity resolution (developer ↔ SET ticker matching)
- [ ] KINNAREE automated market reports
- [ ] Sentiment analysis on CBRE/BOT reports

### Phase 4 — Frontend (LANNA)
- [ ] Interactive 3D property map (Mapbox GL JS)
- [ ] AI chat agent (property advisor)
- [ ] Due diligence dashboard
- [ ] Price alert notifications

---

## Tech Stack

| Layer | Technology | Module |
|:---|:---|:---|
| Crawling | crawl4ai, Playwright, lxml | SIAM |
| Relational DB | Supabase (PostgreSQL) | CHANG |
| Vector DB | Qdrant (768-dim, Cosine) | CHANG |
| Graph DB | ⚠️ Neo4j **INACTIVE** | NAGA |
| Embeddings | all-MiniLM-L6-v2 | GARUDA |
| LLM | Claude API / Ollama (local) | GARUDA |
| NLP (Thai) | PyThaiNLP, spaCy | NAGA |
| Frontend Map | Mapbox GL JS (recommended) | LANNA |
| Dashboard | Apache Superset / Custom React | LANNA |
| Workflow | n8n (VPS Hostinger) | SIAM |
| CI/CD | Docker, GitHub Actions | DevOps |

---

## Key Discovery: JSON-LD Schema.org Data

LivePhuket embeds `LocalBusiness` JSON-LD with:
- **GeoCoordinates**: `latitude`, `longitude` (eliminates geocoding!)
- **PostalAddress**: `addressCountry`, `addressRegion`, `addressLocality`, `streetAddress`
- **amenityFeature**: Structured array of all facilities
- **priceRange**: Price information
- **description**: Full project description
- **image**: Gallery URLs

This is the **primary extraction strategy** — CSS parsing becomes fallback only.

---

## Repository Structure

```
rato-sequencer-condominium/
├── phase1_config.yaml              # Pipeline configuration
├── phase1_project_extractor.py     # SIAM: Main project crawler
├── phase1_developer_extractor.py   # SIAM: Developer directory
├── phase1_faq_extractor.py         # SIAM: FazWaz FAQ
├── phase1_financial_extractor.py   # KINNAREE: SET Thailand
├── v2_pipeline_orchestrator.py     # CHANG: DB exports
├── v2_dashboard_generator.py       # LANNA: HTML dashboard
├── requirements.txt                # All dependencies
├── outputs/                        # Crawl outputs (JSONL)
└── sitemap_search/                 # Phase 2 prep
```
