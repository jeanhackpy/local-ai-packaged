# 🏗️ Data Architecture & Schemas

*Ce document est la source de vérité pour la structure des données à travers la stack.*

> ⚠️ **Dernière mise à jour: 2026-04-21** — Audit VPS complet

---

## 🚨 État des Services (2026-04-21)

| Service | Status | Notes |
|---------|--------|-------|
| Qdrant | ✅ Running (Docker) | `units`: 45,039 pts, **768 dims**, Cosine |
| Supabase (Postgres) | ✅ Running (Docker) | 10 containers |
| Neo4j | ❌ **INACTIVE** | Pas de container, service inactif |
| Ollama | ⚠️ **STOPPED** | Container exited (17h ago) |
| Valkey (Redis) | ✅ Running (Docker) | Cache/Queue |
| Palanthai API | ✅ Running (systemd) | v2.0.0, port 8500 |
| reflexion_kb | ⚠️ Daté | 203 entries, last updated **2026-03-20** |

---

## 🗄️ Relational Schema (Supabase / PostgreSQL)

*Basé sur SQLModel utilisé dans les scripts d'ingestion.*

### Tables Principales
| Table | Description | Champs Clés |
| :--- | :--- | :--- |
| `Constructor` | Promoteurs immobiliers | `id`, `name` (unique), `description` |
| `Residence` | Projets/Immeubles | `id`, `name`, `location`, `year_built`, `constructor_id` (FK) |
| `Listing` | Annonces spécifiques | `id`, `url`, `unit_type`, `price`, `sqm`, `residence_id` (FK) |

### Relations
- **Constructor** (1) <---> (N) **Residence**
- **Residence** (1) <---> (N) **Listing**

---

## 🧠 Vector Search Schema (Qdrant)

*Utilisé pour la recherche sémantique et le RAG.*

### Collections Réelles (2026-04-21)
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

### Collection : `palanthai_knowledge`
- **Dimensions**: 768
- **Contenu**: Connaissance Reflexion / brand content

---

## 🕸️ Graph Schema (Neo4j)

> ⚠️ **INACTIVE** — Neo4j n'est pas en cours d'exécution. Les endpoints `/api/v1/sync/neo4j/*` existent dans Palanthai API v2.0.0 mais le serveur Neo4j est inactif.

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

## 🔄 Data Pipeline Flow (Phase 1)

1. **Extraction** : `phase1_project_extractor.py` (Crawl4AI) récupère les données structurées pour 10 régions/types (Bangkok, Phuket, Samui, Pattaya, Hua Hin).
2. **Parsing** : Extraction directe via YAML config (`phase1_config.yaml`).
3. **Developer Enrichment** : `phase1_developer_extractor.py` pour enrichir les données promoteurs (~1519).
4. **Knowledge Extraction** : `phase1_faq_extractor.py` pour les articles FAQ de FazWaz.
5. **Vectorization** : Palanthai API → Qdrant `units` (45k vectors)
6. **Graph Linking** : ⚠️ `05_neo4j_ingestor.py` — Neo4j INACTIF

---

## ⚠️ Points de Vigilance

- **Neo4j OFF**: Aucune synchronisation graph n'a lieu. Réactiver si NAGA est utilisé.
- **Ollama OFF**: Pas de LLM local. OpenRouter API nécessaire si Ollama redémarré.
- **KB dated (2026-03-20)**: `reflexion_kb_clean.json` pas mis à jour depuis 1 mois.

---

*Dernière mise à jour : 2026-04-21*
*Source : [[20_Projects/Active/Pipeline_Main_Scraper]]*
