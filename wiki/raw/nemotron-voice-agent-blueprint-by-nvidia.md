---
created: 2026-04-05
tags:
  - "nvidia"
  - "blueprint"
  - "voice-agent"
  - "nemotron"
  - "asr"
  - "tts"
  - "clippings"
---

## Summary

A comprehensive voice agent blueprint integrating NVIDIA Nemotron ASR, LLM, and TTS models in a cascaded pipeline. Solves complexities of streaming, interruptible conversations with built-in voice activation detection (VAD) and end-of-utterance (EOU) logic for natural conversational flow.

## Points Clés

- **Cascaded Voice Pipeline**: Parakeet ASR → Nemotron LLM → Magpie TTS
- **Voice Activation Detection (VAD)**: Intelligent start/stop speaking detection
- **End of Utterance (EOU)**: Natural conversation flow with interruption support
- **Multilingual TTS**: 7 languages optimized by Magpie multilingual model
- **Sub-Second Latency**: <1s E2E latency with 64 parallel streams (3xH100)
- **Enterprise Scaling**: Multiple concurrent instances supported
- **Use Cases**: Healthcare, Telco, Retail, FSI, Airlines, Hospitality

## Connexions

- [[wiki/sources/ambient-healthcare-agents-blueprint-by-nvidia|Ambient Healthcare Agents]] - Healthcare-specific voice deployment
- [[wiki/sources/streaming-data-to-rag-blueprint-by-nvidia|Streaming Data to RAG]] - Related real-time speech processing
- [[wiki/concepts/voice-ai|Voice AI]] - Voice interface patterns
- [[wiki/concepts/nemotron|Nemotron]] - NVIDIA's family of LLMs

