---
created: 2026-04-05
tags:
  - nvidia
  - blueprint
  - voice-agent
  - nemotron
  - asr
  - tts
---

# Nemotron Voice Agent Blueprint by NVIDIA

## Summary

NVIDIA blueprint for cascaded voice agent pipeline integrating Nemotron ASR, LLM, and TTS models. Solves complexities of streaming, interruptible conversations with built-in voice activation detection (VAD) and end-of-utterance (EOU) logic for natural conversational flow.

## Key Concepts

- **Cascaded Voice Pipeline**: Parakeet ASR → Nemotron LLM → Magpie TTS
- **Voice Activation Detection (VAD)**: Intelligent start/stop speaking detection
- **End of Utterance (EOU)**: Natural conversation flow with interruption support
- **Multilingual TTS**: 7 languages optimized by Magpie multilingual model
- **Sub-Second Latency**: <1s E2E latency with 64 parallel streams (3xH100)
- **Use Cases**: Healthcare, Telco, Retail, FSI, Airlines, Hospitality

## Architecture

Multi-backend voice pipeline with ASR-LLM-TTS cascade, VAD/EOU logic for turn-taking, and enterprise scaling support for multiple concurrent instances.

## Connections

- [[sources/nemotron-voice-agent]] — Core voice agent technology
- [[sources/ambient-healthcare-agents-blueprint]] — Healthcare-specific deployment
- [[concepts/voice-ai]] — Voice interface patterns