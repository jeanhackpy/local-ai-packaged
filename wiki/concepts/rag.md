---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, RAG, retrieval, embeddings]
sources: []
---

## RAG (Retrieval Augmented Generation)

Paradigme pour connecter LLMs à données externes via retrieval. Le LLM génère des réponses augmentées par des documents retrievés.

### Components

1. **Embedding** : Text → vectors (E5, BGE, OpenAI embeddings)
2. **Vector DB** : Stockage et search (Qdrant, Pinecone, Chroma)
3. **Retrieval** : BM25, semantic search, hybrid search
4. **Reranking** : Cross-encoder pour améliorer pertinence
5. **Generation** : LLM génère réponse finale

### Patterns

- **Hybrid Search** : BM25 + vector → meilleur que chacun seul
- **MMR (Maximal Marginal Relevance)** : Diversité dans results
- **Reranking** : Cross-encoder après retrieval initial
- **Multi-modal RAG** : Text + images + tables
- **Streaming RAG** : Données en temps réel

## Sources

- [[sources/cyborg-enterprise-rag]]
- [[sources/rag-reranker-setup]]
- [[sources/streaming-data-rag-nvidia]]
- [[sources/from-transcripts-to-ai-agents]]
- [[sources/retail-shopping-assistant-nvidia]]

## Connexions

- [[concepts/agentic-ai]] (grounding)
- [[concepts/knowledge-graph]] (structuring)
