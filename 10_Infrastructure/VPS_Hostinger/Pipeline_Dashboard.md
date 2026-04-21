# 🚀 Pipeline & Data Flow Monitoring

*Ce dashboard centralise la surveillance des scripts d'extraction et d'ingestion s'exécutant sur le VPS.*

## 🏗️ Architecture du Flux
1.  **Crawl** : `01_crawler_engine.py` (Crawl4AI)
2.  **Export** : `02_supabase_exporter.py`
3.  **Vector Ingest** : `04_qdrant_ingestor.py`
4.  **Graph Ingest** : `05_neo4j_ingestor.py`
5.  **Enrichment** : `08_data_enricher.py` (NLP)

## 🩺 État des Services Critiques
- **Supabase Connectivity** : [Vérifier via `archives/test_supabase_connect.py`]
- **Qdrant API** : [Endpoint :6333]
- **Neo4j DB** : [Endpoint :7474]

## 📅 Journaux d'Exécution (Logs)
| Script | Fréquence | Dernier Run | Statut |
|--------|-----------|-------------|--------|
| `master_runner.py` | Quotidien | - | ⚪ Non suivi |
| `qdrant_ingestor.py` | Hebdo | - | ⚪ Non suivi |
| `neo4j_ingestor.py` | Hebdo | - | ⚪ Non suivi |

## 🛠 Actions de Maintenance
- [ ] Automatiser `03_master_runner.py` via Cron sur le VPS.
- [ ] Configurer les alertes Slack si un ingestor échoue.

---
*Dernière mise à jour : 2026-04-21 — ⚠️ docker ps confirmé: Ollama OFF, Neo4j INACTIVE, Palanthai API v2.0.0 sur port 8500*
