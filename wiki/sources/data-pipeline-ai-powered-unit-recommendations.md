---
created: 2026-05-14
updated: 2026-05-14
tags: [real-estate, recommendation-system, data-pipeline, LLM, vector-search, Neo4j, Qdrant, Supabase]
sources: [raw/Data-Pipeline-for-AI-Powered-Unit-Recommendations.md]
authors: [MiniMax Agent]
---

# Data Pipeline for AI-Powered Unit Recommendations

## Summary

Architecture for real estate data pipeline combining scrapers, Supabase (structured data), Qdrant (vector search), Neo4j (graph relationships), and LLM for natural language querying. Implements hybrid search with re-ranking and closed-loop feedback.

## Key Concepts

- **Multi-backend architecture**: Supabase + Qdrant + Neo4j + LLM
- **Hybrid search**: Vector similarity with filters
- **Decision tree backtracking**: Investment criteria parsing and property scoring
- **Graph relationships**: Location graphs, commute analysis, preference propagation
- **Feedback loop**: Closed-loop with outcomes for continuous improvement

## Connections

- [[concepts/recommendation-systems]] — Property recommendation AI
- [[concepts/vector-databases]] — Qdrant semantic search
- [[concepts/graph-databases]] — Neo4j relationship mapping
- [[concepts/property-valuation]] — Real estate intelligence