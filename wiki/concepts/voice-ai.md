---
created: 2026-04-05
updated: 2026-04-21
tags: [concept, voice-AI, ASR, TTS, VAD, conversational-AI]
sources: [raw/nemotron-voice-agent-nvidia.md, raw/nemotron-voice-agent-blueprint-by-nvidia.md, raw/streaming-data-rag-nvidia.md, raw/streaming-data-to-rag-blueprint-by-nvidia.md]
---

## Voice AI

Voice AI connects ASR (speech-to-text), LLMs (intent and response generation), and TTS (text-to-speech) in cascaded pipelines for natural spoken dialogue with AI agents.

### Architecture

1. **ASR** → Parakeet CTC model (NVIDIA Riva) converts speech to text in real-time
2. **LLM** → Nemotron or Llama model processes intent, retrieves context, generates response
3. **TTS** → Magpie multilingual model converts response to speech

### Key Capabilities

- **Voice Activation Detection (VAD)** — intelligent start/stop speaking detection
- **End-of-Utterance (EOU)** — handles interruption mid-speech naturally
- **Multilingual** — 7+ languages with culturally-aware prompts
- **Sub-second latency** — <1s end-to-end with GPU acceleration (3× H100)

### Use Cases

- **Healthcare**: Ambient documentation (SOAP note generation from patient-provider conversation)
- **Real estate**: Voice-first property search ("show me 3-bed condos near BTS Asok under 5M")
- **Retail**: Voice shopping assistant with multimodal product retrieval
- **Call center**: Real-time transcription + RAG over knowledge base

## Sources

- [[sources/nemotron-voice-agent-blueprint]]
- [[sources/nemotron-voice-agent]]
- [[sources/streaming-data-to-rag-blueprint]]
- [[sources/streaming-data-rag]]
- [[sources/ambient-healthcare-agents-blueprint]]

## Connexions

- [[concepts/agentic-ai]] — voice as an interface to agents
- [[concepts/rag]] — voice queries retrieve from knowledge bases
- [[concepts/computer-vision]] — image + voice for multimodal property search
