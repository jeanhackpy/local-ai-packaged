---
authors:
  - "[[MiniMax Agent]]"
date: 2026-03-26
tags:
  - "real estate"
  - "recommendation system"
  - "data pipeline"
  - "LLM integration"
  - "vector search"
created: 2026-04-05
---

# Data Pipeline for AI-Powered Unit Recommendations

## Overview

Architecture for building a real estate data pipeline that combines:
- **Scrapers** for data collection
- **Supabase** for structured data
- **Qdrant** for vector search
- **Neo4j** for graph relationships
- **LLM** for natural language querying

## Architecture

```
┌─────────────────────────────────────────────────────────────────────────┐
│                           DATA FLOW ARCHITECTURE                         │
├─────────────────────────────────────────────────────────────────────────┤
│                                                                          │
│  ┌──────────┐    ┌───────────┐    ┌───────────┐    ┌───────────┐      │
│  │          │    │           │    │           │    │           │      │
│  │ SCRAPER  │───▶│ SUPABASE  │───▶│  QDRANT   │───▶│   LLM     │      │
│  │          │    │           │    │           │    │  (Query)  │      │
│  └──────────┘    └───────────┘    └───────────┘    └───────────┘      │
│       │               │                │                │               │
│       │               │                │                │               │
│       ▼               ▼                ▼                ▼               │
│  ┌──────────────────────────────────────────────────────────────────┐   │
│  │                         NEO4J (Graph DB)                         │   │
│  │   - Property relationships                                       │   │
│  │   - Location graphs                                             │   │
│  │   - User preferences graph                                       │   │
│  └──────────────────────────────────────────────────────────────────┘   │
│                                                                          │
└─────────────────────────────────────────────────────────────────────────┘
```

## Component Roles

### Supabase (Relational Data)
- Property master data
- User profiles and preferences
- Transaction history
- Real-time sync

### Qdrant (Vector Search)
- Property embeddings
- Semantic similarity matching
- Natural language query processing

### Neo4j (Graph Relationships)
- Location graphs
- Property comparisons
- User preference propagation
- Route/commute analysis

### LLM Integration
- Natural language query parsing
- Structured query generation
- Recommendation explanation

## Key Strategies

1. **Hybrid Search**: Combine vector similarity with filters
2. **Multi-vector Fields**: Separate embeddings for different aspects
3. **Re-ranking**: Cross-encoders for final ordering
4. **Feedback Loop**: Closed-loop with outcomes for continuous improvement

## Decision Tree Backtracking

The system implements a decision tree approach where:
- Investment goals are parsed into decision criteria
- Backtracking narrows candidates through decision nodes
- Properties are scored against all criteria
- Results ranked by weighted importance

## References

- [MiniMax Agent Chat](

## Related Concepts

- [[Real Estate Technology]]
- [[Recommendation Systems]]
- [[Vector Databases]]
- [[Graph Databases]]
- [[LLM Integration]]

---
*Source: [[Clippings]] | [[MiniMax Agent]]*
