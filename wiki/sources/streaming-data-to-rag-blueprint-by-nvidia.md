---
---
created: 2026-04-05
tags:
  - "nvidia"
  - "blueprint"
  - "streaming"
  - "rag"
  - "sdr"
  - "rf-signals"
  - "real-time"
  - "clippings"
---

## Summary

A real-time RAG pipeline that processes live data streams from GPU-accelerated software-defined radio (SDR). Captures RF signals, transcribes speech, embeds and indexes in real-time, enabling context-aware queries over dynamic streams for mission-critical applications.

## Points Clés

- **GPU-Accelerated SDR Pipeline**: NVIDIA Holoscan for high-performance signal processing
- **Real-Time RF Ingestion**: Live FM radio capture via UDP with enterprise reliability
- **NVIDIA Riva ASR**: Parakeet CTC model for real-time speech-to-text (<5s latency)
- **Temporal RAG Queries**: Time-based queries like "Summarize the last 5 minutes"
- **Llama NeMo Retriever 3.2**: Embedding and reranking NIMs for semantic search
- **Sub-5-Second Latency**: End-to-end speech-to-searchable-insight pipeline
- **Continuous Document Ingestion**: Minimal delay for time-critical applications
- **Interactive Chat UI**: NeMo Agent Toolkit UI for real-time conversation

## Connexions

- [[wiki/sources/nemotron-voice-agent-blueprint-by-nvidia|Nemotron Voice Agent]] - Related voice pipeline technology
- [[wiki/sources/ambient-healthcare-agents-blueprint-by-nvidia|Ambient Healthcare Agents]] - Real-time speech processing
- [[wiki/concepts/rag|RAG]] - Core RAG architecture
- [[wiki/concepts/real-time-ai|Real-Time AI]] - Streaming inference patterns

