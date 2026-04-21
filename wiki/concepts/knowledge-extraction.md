---
created: 2026-04-21
updated: 2026-04-21
tags: [concept, knowledge-extraction, transcripts, conversational-AI, evaluation]
sources: [raw/from-transcripts-to-ai-agents.md]
---

## Knowledge Extraction

Extracting structured knowledge from conversational transcripts and documents, integrating it into RAG pipelines, and evaluating the resulting AI assistants.

### From Transcripts to Knowledge

Research on converting raw conversational transcripts into structured knowledge:
- **Entity extraction** — names, dates, property specs, price ranges mentioned
- **Intent classification** — buyer vs. seller inquiry, viewing request, pricing question
- **Relationship mapping** — which entities relate to which (buyer → preferred_area → Bang Na)
- **Temporal tracking** — how preferences evolve across conversation turns

### RAG Integration Patterns

Knowledge extracted from transcripts feeds back into RAG for:
- **Context maintenance** — conversation history as a retrieval corpus
- **Preference learning** — buyers' implicit preferences inferred from questions asked
- **Agent memory** — persistent context across sessions

### Evaluation Frameworks

Robust evaluation of conversational AI assistants requires:
- **Task completion metrics** — did the agent successfully answer/act?
- **Retrieval quality** — is the retrieved context relevant and complete?
- **Hallucination detection** — does the agent's answer match the retrieved documents?
- **User satisfaction** — end-to-end conversation quality

## Sources

- [[sources/from-transcripts-to-ai-agents]]

## Connexions

- [[concepts/rag]] — knowledge extraction feeds RAG pipelines
- [[concepts/agentic-ai]] — agents that remember and learn from conversations
- [[concepts/immobilier-thailand]] — buyer agent that learns preferences over time
