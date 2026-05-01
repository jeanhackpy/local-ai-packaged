# 🏗️ Data Architecture & Schemas

*Ce document est la source de vérité pour la structure des données à travers la stack.*

> ⚠️ **Dernière mise à jour: 2026-05-01** — Security audit + full VPS structure mapping

---

## 🚨 État des Services (2026-05-01)

| Service | Status | Notes |
|---------|--------|-------|
| Qdrant | ✅ Running (Docker) | `units`: 45,039 pts, **768 dims**, Cosine |
| Supabase (Postgres) | ✅ Running (Docker) | 10 containers |
| Neo4j | ❌ **INACTIVE** | Container not running |
| Ollama | ⚠️ **STOPPED** | Container exited |
| Valkey (Redis) | ✅ Running (Docker) | Cache/Queue |
| Palanthai API | ✅ Running (systemd) | v2.0.0, port 8500 |
| n8n | ✅ Running (Docker) | https://n8n.recall-agency.com |
| reflexion_kb | ⚠️ Daté | 203 entries, last updated **2026-03-20** |

> 🔐 **SECURITY ALERT**: Multiple CRITICAL vulnerabilities found — see [[VPS_Security_Audit_2026-05-01]]

---

## 🗄️ Palanthai — Pipeline Phases

### Phase 1 : Scraping (`/home/phil/palanthai/phase1-project-directory/`)

```
source_crawler.py        → Discovers project/unit URLs from livephuket.com
                          → 6 active regions: bangkok, phuket, surat-thani,
                            chiang-mai, chon-buri, prachuap-kiri-khan
livephuket_login.py      → Playwright auth (credentials in env vars ✓)
project_extractor.py     → Playwright extraction of project details
crawling_extractor.py   → Unit extraction adapter (quality threshold: 75)
unit_extractor_v2.py    → Phase 5 unit extractor
models_parsers_00.py    → Pydantic models + parsers (ProjectRecord, etc.)

fullrun/fullrun.py      → Full pipeline: discover → projects → units
                          → Writes JSONL batches to disk BEFORE DB calls
                          → Crash-safe: --resume, /tmp/fullrun_PAUSE support
                          → RECYCLE_EVERY = 35 URLs per browser session
                          → max 2 concurrent Playwright pages (Semaphore(2))
                          → Waits if free RAM < 800 MiB (⚠️ could hang indefinitely)

wf_extract/             → 12 city-specific extraction scripts
  WF-extract-*-condo.py  (6 files)
  WF-extract-*-villa.py  (6 files)
  Phuket has pagination loop (other cities don't)

ingestor_v5.py          → Phase 5 multi-DB ingestor
                          ⚠️ CRITICAL: hardcoded Postgres fallback password
db_ingestor_units.py   → Unit ingestor (insert_supabase_direct, uuid5_from_url)
sync_service.py         → FastAPI service (port 8500)
                          ⚠️ CRITICAL: hardcoded PG + command injection

lab_test_SCRIPTS/       → Unit test scripts (not yet audited)
  TEST_api_db.py
  TEST_crawl4ai.py
  TEST_source_crawler.py
```

### Phase 2 : Extraction (`/home/phil/palanthai/phase2/`)

```
sequencer_v2.py         → Batch orchestrator (master_queue.json + progress.json)
unit_extractor_v2.py    → Unit extraction
unit_schema.py          → Pydantic UnitRecord (33 fields)
quality_checker.py      → Quality validation
db_ingestor_units.py    → DB insertion
data/
  master_queue.json     → Global queue
  progress.json         → Checkpoint
  batches/batch_NNN/    → Per-batch: units.jsonl, metrics.json,
                          quality_report.json, db_result.json
logs/sequencer_v2_*.log
```

### Phase 3 : Content & Embedding (`/home/phil/palanthai/phase3-embedding&graph/`)

```
content/
  data_cleaner.py       → Pydantic: replaces source brands → "Reflexion"
  embed_to_qdrant.py    → Ollama embedding → Qdrant
  model_config.py       → OpenRouter FREE model routing + chat()
kb_reflexion-leon/      → Knowledge base (154 files)
```

### Phase 7 : Agentic (Langraph)
```
phase7-agentic-langraph/  → (not audited)
```

---

## 🗄️ Relational Schema (Supabase / PostgreSQL)

*Basé sur SQLModel utilisé dans les scripts d'ingestion.*

### Tables Principales
| Table | Description | Champs Clés |
| :--- | :--- | :--- |
| `Constructor` | Promoteurs immobiliers | `id`, `name` (unique), `description` |
| `Residence` | Projets/Immeubles | `id`, `name`, `location`, `year_built`, `constructor_id` (FK) |
| `Listing` | Annonces spécifiques | `id`, `url`, `unit_type`, `price`, `sqm`, `residence_id` (FK) |

### fullrun_* Tables (Phase 5 — test mode 3)
```
fullrun_projects_live
fullrun_project_images
fullrun_project_floor_plans
fullrun_unit
fullrun_unit_images
fullrun_unit_floor_plans
```
→ Written exclusively by `fullrun/fullrun.py` (PHASE5_TEST_MODE=3)

### Relations
- **Constructor** (1) <---> (N) **Residence**
- **Residence** (1) <---> (N) **Listing**

---

## 🧠 Vector Search Schema (Qdrant)

*Utilisé pour la recherche sémantique et le RAG.*

### Collections Réelles (2026-05-01)
| Collection | Points | Dimensions | Distance |
|:---|:---|:---|:---|
| `units` | **45,039** | **768** | Cosine |
| `units_v3` | 200 | — (payload only) | — |
| `palanthai_knowledge` | 612 | 768 | Cosine |
| `palanthai_memory` | 1 | 768 | Cosine |
| `mem0migrations` | 1 | 1536 | Cosine |
| `projects_v3` | 100 | — (payload only) | — |

### Collection : `units` (principale — 45k+ points)
- **Modèle**: Unknown (768 dims — probablement BGE-large ou E5)
- **Distance**: Cosine
- **Quality gate**: Only embed units with quality score ≥ 75/100

### Collection : `palanthai_knowledge`
- **Dimensions**: 768
- **Contenu**: Connaissance Reflexion / brand content

---

## 🕸️ Graph Schema (Neo4j)

> ⚠️ **INACTIVE** — Neo4j n'est pas en cours d'exécution. Les endpoints `/api/v1/sync/neo4j/*` existent dans Palanthai API v2.0.0 mais le serveur Neo4j est inactif.

### Credentials (hardcoded — SECURITY RISK)
```
NEO4J_URI = bolt://localhost:7687
NEO4J_USER = neo4j
NEO4J_PASS = 9PXofEGxRCw2O119HC3RnRUK  ← EXPOSED, rotate immediately
```

### Nodes Prévus (quand Neo4j réactivé)
- `:Project` {name, location, year}
- `:Developer` {name}
- `:Location` {name, city, district}
- `:Feature` {name} (ex: Pool, Gym, Sea View)

### Relationships Prévus
- `(:Project)-[:DEVELOPED_BY]->(:Developer)`
- `(:Project)-[:LOCATED_IN]->(:Location)`
- `(:Project)-[:HAS_FEATURE]->(:Feature)`

---

## 🔄 Data Pipeline Flow (Complete)

```
LivePhuket.com (scraping)
    ↓
source_crawler.py        → URL discovery (6 regions)
    ↓
wf_extract/*.py         → Project extraction (12 city/type combos)
    ↓
fullrun/fullrun.py       → orchestrator: discover → projects → units
    ↓ (JSONL batches written to disk)
ingestor_v5.py          → multi-DB ingest (PG, Supabase)
    ↓
phase2/sequencer_v2.py  → Unit extraction + quality check
    ↓
db_ingestor_units.py    → Supabase upsert
    ↓
phase3/embed_to_qdrant.py → Ollama embedding → Qdrant units collection
    ↓ (quality ≥ 75 gate)
Qdrant vector store     → 45,039 units (768 dims)
    ↓
Palanthai API           → RAG queries, sync endpoints
    ↓
n8n workflows           → SEO automation, content generation
    ↓
WordPress (reflexion.asia, recall-agency.com)
```

---

## ⚠️ Points de Vigilance

- **Neo4j OFF**: Aucune synchronisation graph n'a lieu. Réactiver si utilisé.
- **Ollama OFF**: Pas de LLM local. OpenRouter API nécessaire si Ollama redémarré.
- **KB dated (2026-03-20)**: `reflexion_kb_clean.json` pas mis à jour depuis 1 mois.
- **SECURITY**: Multiple hardcoded credentials exposed — rotate immediately. See [[VPS_Security_Audit_2026-05-01]]

---

*Dernière mise à jour : 2026-05-01*
*Source : [[VPS_INFRASTRUCTURE_REFERENCE]], [[VPS_Security_Audit_2026-05-01]]*