---
created: 2026-04-05
updated: 2026-04-21
tags: [data-pipeline, supabase, qdrant, neo4j, recommendations, real-estate]
sources: [raw/data-pipeline-unit-recommendations.md]
---

## Résumé

Pipeline de données pour recommandations d'unités AI-powered. Supabase (structuré) + Qdrant (vecteurs) + Neo4j (relations). Serving de recommandations en temps réel.

## Points clés

- Supabase : données structurées (listings, users, transactions)
- Qdrant : vecteurs embeddings propriétés pour similarity search
- Neo4j : graphe relations (similar listings, neighborhood, preferences)
- Real-time recommendation serving architecture
- Application àproperty recommendation engine FazWaz

## Connexions

- [[entities/supabase]]
- [[entities/qdrant]]
- [[entities/neo4j]]
- [[sources/palanthai-opensource-stack]]
- [[sources/systeme-ontologique]]
