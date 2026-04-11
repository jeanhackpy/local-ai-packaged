# 📊 SIAM Pipeline — Status Tracker

> Last updated: 2026-03-12

---

## Phase 1 Progress

| Component | Script | Status | Notes |
|:---|:---|:---|:---|
| 🗺️ Project Extractor | `phase1_project_extractor.py` | ✅ Ready | JSON-LD + CSS, Pydantic validated, Cloudflare bypass (`magic=True`), facilities as full name lists |
| 👷 Developer Extractor | `phase1_developer_extractor.py` | ✅ Ready | 16 pages, ~1519 devs, optional enrichment |
| 📚 FAQ Extractor | `phase1_faq_extractor.py` | ✅ Ready | FazWaz advice articles for RAG |
| 📈 Financial Extractor | `phase1_financial_extractor.py` | 🔜 Planned | SET Thailand PropCon sector |
| ⚙️ Pipeline Config | `phase1_config.yaml` | ✅ Ready | 10 jobs + dev + faq config |
| 📦 Requirements | `requirements.txt` | ✅ Ready | All dependencies listed |
| 🏗️ DB Orchestrator | `v2_pipeline_orchestrator.py` | ✅ Ready | Supabase + Qdrant + Neo4j exports |
| 📊 Dashboard Generator | `v2_dashboard_generator.py` | ✅ Ready | Interactive HTML with Chart.js |

---

## Key Discovery: JSON-LD Schema.org

LivePhuket embeds `LocalBusiness` JSON-LD in every project page:
- **GeoCoordinates**: `latitude`, `longitude` → eliminates Nominatim geocoding
- **PostalAddress**: structured with region/locality/street
- **amenityFeature**: clean array of all facilities
- **priceRange**: price information
- **description**: full project text

**Impact**: Quality score improvement ~+15pts, geocoding latency eliminated.

---

## Seed URLs (10 Jobs)

| Region | Type | Status |
|:---|:---|:---|
| Bangkok | Condo | 🔄 Ready |
| Bangkok | Villa | 🔄 Ready |
| Phuket | Condo | 🔄 Ready |
| Phuket | Villa | 🔄 Ready |
| Koh Samui | Condo | 🔄 Ready |
| Koh Samui | Villa | 🔄 Ready |
| Pattaya | Condo | 🔄 Ready |
| Pattaya | Villa | 🔄 Ready |
| Hua Hin | Condo | 🔄 Ready |
| Hua Hin | Villa | 🔄 Ready |

---

## Data Sources Roadmap

### Active (Phase 1)
- [x] LivePhuket.com — Projects + Developers
- [x] FazWaz.com — FAQ Knowledge Base

### Planned (Phase 1.5 — KINNAREE)
- [ ] SET Thailand (`set.or.th`) — PropCon sector financials
- [ ] Bank of Thailand — REIC housing index, construction permits
- [ ] CBRE Thailand — Quarterly market reports (PDF)
- [ ] EIA databases — Environmental impact assessments

### Phase 2 — Multi-Marketplace
- [ ] DDProperty.com
- [ ] Hipflat.co.th
- [ ] PropertyHub.in.th
- [ ] Thailand-Property.com
- [ ] Sitemap.xml discovery engine

---

## Code Location

Repository: `rato-sequencer-condominium/`
Symlink: [[../../../10_Infrastructure/Code_Links/palanthai_scripts]]
