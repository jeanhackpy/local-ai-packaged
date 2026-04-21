---
created: 2026-04-05
updated: 2026-04-21
tags: [thailand, open-source, palanthai, stack, qdrant, neo4j, supabase]
sources: [raw/palanthai-opensource-stack.md]
---

## Résumé

Stack technique open-source pour marketplace immobilier thaïlandais. Qdrant pour les embeddings vectoriels, Neo4j pour les relations entre propriétés, Supabase pour les données structurées, Ollama pour l'inférence locale. Implémentation de référence de l'AI factory pour property intelligence.

## Points clés

- Qdrant : stockage vectoriel haute performance pour embeddings de propriétés
- Neo4j : graphe de relations immobilières (quartiers, équipements, prix)
- Supabase : base de données PostgreSQL structurées + auth + edge functions
- Ollama : inférence LLM locale pour privacy et coût réduit
- Pipeline ETL intégré pour ingestion et sync des données

## Connexions

- [[entities/qdrant]]
- [[entities/neo4j]]
- [[entities/supabase]]
- [[sources/systeme-ontologique]]
- [[sources/data-pipeline-unit-recommendations]]
