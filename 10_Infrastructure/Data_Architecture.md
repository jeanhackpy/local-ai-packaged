# 🏗️ Data Architecture & Schemas

*Ce document est la source de vérité pour la structure des données à travers la stack.*

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

### Collection : `residences`
- **Modèle d'Embedding** : `all-MiniLM-L6-v2` (Dimensions : 384)
- **Distance** : Cosine

### Structure du Payload (Metadata)
| Champ | Type | Description |
| :--- | :--- | :--- |
| `name` | String | Nom du projet |
| `address` | String | Localisation textuelle |
| `developer` | String | Nom du promoteur |
| `sale_price_min` | Float | Prix min de vente |
| `rent_price_min` | Float | Prix min de location |
| `region` | String | Région (ex: Phuket, Bangkok) |
| `property_type` | String | Type (Condo, Villa) |
| `image` | URL | Image principale du projet |

---

## 🕸️ Graph Schema (Neo4j)
*Utilisé pour les relations complexes et l'analyse de réseau.*

### Nodes (Nœuds)
- `:Project` {name, location, year}
- `:Developer` {name}
- `:Location` {name, city, district}
- `:Feature` {name} (ex: Pool, Gym, Sea View)

### Relationships (Relations)
- `(:Project)-[:DEVELOPED_BY]->(:Developer)`
- `(:Project)-[:LOCATED_IN]->(:Location)`
- `(:Project)-[:HAS_FEATURE]->(:Feature)`

---

## 🔄 Data Pipeline Flow (Phase 1)
1. **Extraction** : `phase1_project_extractor.py` (Crawl4AI) récupère les données structurées pour 10 régions/types (Bangkok, Phuket, Samui, Pattaya, Hua Hin).
2. **Parsing** : Extraction directe via YAML config (`phase1_config.yaml`).
3. **Developer Enrichment** : `phase1_developer_extractor.py` pour enrichir les données promoteurs (~1519).
4. **Knowledge Extraction** : `phase1_faq_extractor.py` pour les articles FAQ de FazWaz.
5. **Vectorization** : `04_qdrant_ingestor.py` crée les embeddings.
6. **Graph Linking** : `05_neo4j_ingestor.py` crée les relations.

---
*Dernière mise à jour : 2026-03-13*
*Source : [[20_Projects/Active/Pipeline_Main_Scraper]]*
