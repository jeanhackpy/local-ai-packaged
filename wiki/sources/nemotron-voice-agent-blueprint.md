---
created: 2026-04-05
updated: 2026-04-21
tags: [nvidia, blueprint, voice, asr, tts, nemotron, cascaded]
sources: [raw/nemotron-voice-agent-blueprint-by-nvidia.md]
---

## Résumé

Voice agent blueprint: Parakeet ASR → Nemotron LLM → Magpie TTS cascaded pipeline. Voice activation detection (VAD), end-of-utterance (EOU), interruption handling. Sub-1-second latency with 64 parallel streams (3×H100). 7 multilingual TTS languages.

## Points clés

- Cascaded pipeline: Parakeet ASR → Nemotron LLM → Magpie TTS
- Intelligent VAD + EOU detection with natural interruption handling
- Sub-1-second latency; 64 parallel streams on 3×H100; 7 multilingual TTS languages

## Connexions

- [[entities/nvidia]]
- [[concepts/voice-ai]]
- [[sources/ambient-healthcare-agents-blueprint]]
