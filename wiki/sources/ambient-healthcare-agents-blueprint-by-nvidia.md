---
created: 2026-04-05
tags:
  - "nvidia"
  - "blueprint"
  - "healthcare"
  - "agents"
  - "ambient"
  - "soap-notes"
  - "clippings"
---

## Summary

A comprehensive developer example for building ambient AI voice agents in healthcare settings. The blueprint features two distinct use cases: an Ambient Provider Voice Agent that generates clinical documentation (SOAP notes) from patient-provider conversations, and an Ambient Patient Voice Agent that handles high-volume patient touchpoints like intake, scheduling, and information queries.

## Points Clés

- **Dual Agent Architecture**: Provider Agent (clinical documentation) + Patient Agent (intake/scheduling)
- **Riva Speech Pipeline**: Parakeet ASR with speaker diarization and medical terminology support
- **SOAP Note Generation**: Automated clinical documentation from conversational transcripts
- **NeMo Guardrails**: Content safety and topic control for HIPAA-aligned interactions
- **NeMo Microservices**: Modular architecture with Llama Nemotron reasoning models
- **Multilingual TTS**: Magpie multilingual text-to-speech for natural voice responses
- **LangChain Integration**: For orchestration and tool calling

## Connexions

- [[wiki/sources/nemotron-voice-agent-blueprint-by-nvidia|Nemotron Voice Agent]] - Core voice agent technology
- [[wiki/sources/build-an-ai-virtual-assistant-blueprint-by-nvidia|AI Virtual Assistant]] - Broader virtual assistant patterns
- [[wiki/concepts/agentic-ai|Agentic AI]] - Autonomous agent principles
- [[wiki/concepts/rag|RAG]] - Retrieval-augmented generation for healthcare context

