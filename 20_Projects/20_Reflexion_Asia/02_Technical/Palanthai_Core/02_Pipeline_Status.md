# 📊 SIAM Pipeline — Status Tracker

> ⚠️ **Dernière mise à jour: 2026-04-21** — Audit VPS complet nécessaire

---

## 🔍 Analyse VPS — Dossier Palanthai (2026-04-21)

### Structure des dossiers

```
/home/phil/palanthai/
├── palanthai_api.py              # Ancien fichier API (32KB)
├── palanthai-sync.service        # Symlink → systemd
├── sync_service.py               # ✅ FastAPI principal (port 8500, systemd)
├── phase1-project-directory/     # ← Active (PAS phase1/)
│   ├── sync_service.py          # Copie locale du service
│   ├── project_extractor.py      # Crawl4AI + Puppeteer Chrome
│   ├── crawling_extractor.py     # Extraction par URL unique
│   ├── ingestor_v5.py            # Upsert Supabase
│   ├── neo4j_ingestor.py         # ⚠️ INACTIVE (Neo4j off)
│   ├── source_crawler.py         # Discovery des URLs
│   ├── bulk_embed.log            # 336KB, dernière activité 2026-04-20
│   ├── sync.log                  # Projet crawl 2026-04-20 (119 projects)
│   ├── uvicorn.log               # Erreur 422 /api/v1/source/units
│   └── sync_run_results_*.json   # Résultats runs (2026-04-19, 10, 10)
├── phase2-units/
│   ├── sequencer_v2.py           # httpx + BeautifulSoup (pas de browser)
│   ├── unit_extractor_v2.py      # Extraction unit par URL
│   ├── db_ingestor_units.py      # Ingest batch Supabase
│   ├── quality_checker.py         # Validation qualité
│   └── bulk_embed_units.py       # Embed vers Qdrant ( trickle + burst modes)
├── phase3-embedding&graph/
│   ├── massive_embedding.ipynb   # Notebook d'embedding
│   ├── n8n/                      # Workflows n8n
│   └── supabase-edge-functions/  # Edge functions
├── phase4-image-classification/
└── phase5-frontend/

```

### sync_service.py — FastAPI Phase 5 (port 8500)

**Endpoints clés:**
| Endpoint | Fonction |
|:---|:---|
| `POST /api/v1/source/projects` | Crawl projets via source_crawler |
| `POST /api/v1/source/units` | Crawl units via crawl_and_extract |
| `POST /api/v1/source/projects/updated` | UUID-diff vs Supabase puis crawl |
| `GET /api/v1/admin/runs` | Historique des sync_runs |
| `GET /api/v1/admin/failures` | URLs échouées avec retry_count |
| `POST /api/v1/export_embed` | Trigger Kaggle kernel BGE-M3 |
| `POST /api/v1/sync/neo4j/projects` | ⚠️ INACTIVE — Neo4j off |
| `POST /api/v1/migrate` | Applique phase5_migration.sql |

**Flux principal (n8n cron → sync_service):**
1. `source_crawler.get_project_cards()` — Discovery URLs LivePhuket
2. `_filter_new_urls()` — UUID5 diff vs Supabase projects
3. `_crawl_projects()` — Crawl4AI + Puppeteer Chrome, qualité ≥ 60
4. `ingestor_v5.ingest_projects()` — Upsert Supabase, marque `needs_embedding=TRUE`
5. `_crawl_units()` — Parallel Crawl4AI units liés
6. `ingestor_v5.ingest_units()` — Upsert units
7. n8n upload CSV → Kaggle → `POST /export_embed` trigger BGE-M3

### Erreur 422 sur /api/v1/source/units

**Diagnostic:** L'erreur 422 vient du conteneur n8n/docker (172.18.0.19) appelant l'endpoint `/api/v1/source/units`. Le endpoint reçoit des données non valides pour le modèle Pydantic `UnitSourceRequest`.

**Observation:** Le run 2026-04-19 (422) a crawled=0 sur toutes les régions. Le run suivant 2026-04-20 (projets uniquement) a réussi avec 119 projects upserted.

**Cause probable:** Payload malformé envoyé par n8n lors de l'appel unit source scan. À investiguer dans les logs n8n.

### bulk_embed_units.py — Deux modes

| Mode | Batch | Pause | Usage |
|:---|:---|:---|:---|
| **TRICKLE** (default) | 10 units | 30s | Background 24/7, ~1200 units/h |
| **BURST** | 100 units | 3s | Catch-up off-peak, ~33 units/s |

---

## 🚨 État VPS Réel (2026-04-21)

| Service | Status | Notes |
|---------|--------|-------|
| Qdrant (Docker) | ✅ Running | `units`: 45,039 pts, 768 dims |
| n8n (Docker) | ✅ Running | https://n8n.recall-agency.com |
| Caddy (Docker) | ✅ Running | Reverse proxy + TLS |
| Supabase (Docker) | ✅ Running | 10 containers (kong, postgres, auth, etc.) |
| Valkey/Redis | ✅ Running | Cache/Queue |
| MinIO (Docker) | ✅ Running | Object storage |
| SearXNG (Docker) | ✅ Running | Moteur recherche |
| **Palanthai API** | ✅ Running | `palanthai-sync.service`, v2.0.0, port 8500 |
| reflexion_kb_clean.json | ⚠️ Daté | 203 entries, last updated **2026-03-20** |
| **Neo4j** | ❌ INACTIVE | Pas de container, service inactif |
| **Ollama** | ⚠️ STOPPED | Container Docker exited (17h ago) |
| **open-webui** | ⚠️ STOPPED | Container exited (137) |
| Disk | ⚠️ 83% | 80G/96G used |

---

> Last updated: 2026-04-21

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
