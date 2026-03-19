# Pipeline Main Scraper (Real Estate v2)

## 📋 Summary
Project: **Pipeline Agentic Real Estate v2**
A robust web scraping pipeline targeting real estate sites (LivePhuket), enriching data, and exporting to three specialized databases: Supabase, Qdrant, and Neo4j.

## 📁 Source
- **Local Path:** `/Users/phil/Documents/The_Lab/Pipeline/main_scraper`
- **Symlinked in Vault:** [[20_Projects/Active/main_scraper]]

## 🏗 Architecture
The pipeline extracts data through Phase 1 scripts and ingests it into:
1. **Supabase (PostgreSQL)**: Structured data for filtering and CRUD.
2. **Qdrant (Vector Store)**: Semantic search and NLP queries.
3. **Neo4j (Graph DB)**: Relationship analytics and pattern discovery.

### Phase 1 Extractor Scripts
| Script | Purpose |
|--------|---------|
| `phase1_project_extractor.py` | Main extractor (Crawl4AI) for 10 predefined regions/types. |
| `phase1_developer_extractor.py` | Developer data + enrichment for Neo4j relationships. |
| `phase1_faq_extractor.py` | FAQ article extraction from FazWaz. |

## 🚀 Status (as of 13 Mar 2026)
- **Extraction:** 7/10 regions completed (Phuket, Samui, Pattaya, Hua Hin).
- **In Progress:** Bangkok Condos/Villas.
- **Next Steps:** VPS migration and Mapbox GL JS 3D visualization.

## 🔗 Related Notes
- [[10_Infrastructure/Data_Architecture]]
- [[20_Projects/Active/main_scraper/CLAUDE.md|Project Documentation (CLAUDE.md)]]
