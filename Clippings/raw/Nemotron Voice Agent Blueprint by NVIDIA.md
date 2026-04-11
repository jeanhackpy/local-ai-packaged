---
title: "Nemotron Voice Agent Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/nemotron-voice-agent"
author:
published:
created: 2026-04-05
description: "A voice agent that uses the Nemotron model to generate responses to voice commands."
tags:
  - "clippings"
---
j

Voice is the most natural human interface, allowing for efficient and high-speed communication. This developer example provides a comprehensive, end-to-end voice agent blueprint built with **NVIDIA Nemotron** state-of-the-art open models, as NVIDIA NIM for acceleration and scaling. It is designed to guide developers through the creation of a cascaded pipeline, integrating Nemotron ASR, LLM, and TTS, while solving for the complexities of streaming, interruptible conversations. By leveraging NVIDIA NIM microservices, this developer example enables developers to accelerate the deployment of high-performance voice AI solutions.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/nemotron-voice-agent/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/nemotron-voice-agent/diagram.jpg)

### Key Features

- **Advanced Interruption Management:** Features built-in **Voice Activation Detection (VAD)** and **End of Utterance (EOU)** logic to guide the agent on exactly when to start and stop speaking, ensuring a natural conversational flow.
- **Multilingual Capabilities:** Native support for the 7 languages optimized by **Magpie TTS**.
- **Enterprise Scaling:** Supports multiple concurrent instances.

## Benchmarks

| Model / API | Reasoning Mode | Text Only Standalone LLM (%) | LLM In Voice Agent Pipeline (%) |
| --- | --- | --- | --- |
| [Nemotron 49B](https://build.nvidia.com/nvidia/llama-3_3-nemotron-super-49b-v1_5/modelcard) | Reasoning ON | 91.90 | 81.30 |
| [Nemotron 49B](https://build.nvidia.com/nvidia/llama-3_3-nemotron-super-49b-v1_5/modelcard) | Reasoning OFF | 82.70 | 60.30 |
| [Nemotron 30B](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b/modelcard) | Reasoning ON Reasoning Budget - 500 | 78.76 | 75.60 |
| [Nemotron 30B](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b/modelcard) | Reasoning OFF | 56.50 | 50.40 |

Benchmarks based on internal testing. Evaluation source code provided on GitHub.

[![](https://assets.ngc.nvidia.com/products/api-catalog/nemotron-voice-agent/modelperformance.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/nemotron-voice-agent/modelperformance.jpg)

| Parallel Streams | E2E Latency | ASR Latency | TTS TTFB | LLM TTFT | LLM first-sentence latency |
| --- | --- | --- | --- | --- | --- |
| 1 | 0.79 | 0.04 | 0.078 | 0.126 | 0.138 |
| 4 | 0.76 | 0.046 | 0.066 | 0.061 | 0.181 |
| 8 | 0.77 | 0.052 | 0.066 | 0.062 | 0.136 |
| 16 | 0.91 | 0.057 | 0.068 | 0.105 | 0.208 |
| 32 | 0.8 | 0.061 | 0.08 | 0.073 | 0.294 |
| 64 | 1 | 0.067 | 0.11 | 0.156 | 0.386 |

The benchmark table demonstrates that the NVIDIA Nemotron Voice Agent achieves sub-second End-to-End Latency across up to 64 parallel streams with a setup utilizing 3xH100 GPUs (one for Parakeet CTC 1.1B, one for Magpie TTS, and two for Nemotron-3-Nano LLM model) with speculative speech processing enabled.

This developer example is powered by a suite of NVIDIA-optimized microservices designed for maximum throughput and minimal latency.

| Category | Component | Recommended Model |
| --- | --- | --- |
| **Speech-to-Text or Automatic Speech Recognition** | ASR / AST | [NVIDIA Nemotron Speech (RNNT or CTC)](https://build.nvidia.com/explore/speech) |
| **Logic & Reasoning** | LLM | [Nemotron Nano](https://huggingface.co/nvidia/NVIDIA-Nemotron-3-Nano-30B-A3B-BF16) / [Nemotron Super](https://huggingface.co/nvidia/Llama-3_3-Nemotron-Super-49B-v1) |
| **Text-to-Speech** | TTS | [Magpie TTS Multilingual](https://build.nvidia.com/nvidia/magpie-tts-multilingual/modelcard) |
| **Control** | Behavioral Logic | VAD, SVAD, EOU |

## Self-Hosted Configuration

To achieve sub-second response times and high-fidelity audio handling, the following hardware configurations are recommended for local deployment.

| Service | Use Case | Recommended GPU |
| --- | --- | --- |
| **Nemotron Speech ASR/TTS** | Audio Transcription & Synthesis | 1x L40, A100 (80GB), or H100 |
| **Reasoning Model** | LLM & Agentic Logic | 2x H100 (80GB) or 4x A100 (80GB) |
| **Voice Agent** | Entire workflow | [Jetson Thor](https://www.nvidia.com/en-us/autonomous-machines/embedded-systems/jetson-thor/) |

## Use Cases

- Healthcare: A voice-first agent automates the patient intake process by capturing symptoms and medical history hands-free, allowing clinicians to focus entirely on patient care.
- Telco: Real-time virtual assistants handle complex technical troubleshooting and plan upgrades over the phone, reducing wait times while providing instant, multilingual support.
- Retail: Interactive voice agents integrated into in-store kiosks or mobile apps allow customers to browse inventory, check prices, and manage their carts using natural conversation.
- Financial Services (FSI): Secure voice agents enable customers to perform balance inquiries, confirm recent payments, or initiate fraud disputes through a low-latency voice interface.
- Airlines: Travel assistants provide immediate support for rebooking flights, tracking baggage, or selecting seats during high-volume disruption events when traditional call centers are overwhelmed.
- Hospitality: Digital concierge agents handle room service orders and local recommendations in multiple languages, providing a premium, high-speed guest experience without human intervention.

## Getting Started

The code base serves as a playground to test new models and expand basic ASR/LLM/TTS flows.

**Clone the Repo:** Access the public [reference code on GitHub](https://github.com/NVIDIA-AI-Blueprints/nemotron-voice-agent).

**Setup NVIDIA NIM:** Deploy your local system/pipeline using NVIDIA NIM microservices.

This developer example empowers developers to rapidly build, customize, and deploy enterprise-grade voice agents for customer service, and user interactions in healthcare, telecom, retail, and financial services.

Explore the [Ambient Healthcare Agents blueprint](https://build.nvidia.com/nvidia/ambient-healthcare-agents) to deploy ambient agents that assist with patient intake, symptom triage, and compliance for HIPAA/PCI. This blueprint has tightly integrated, healthcare-tuned models (e.g., clinical LLMs, medical diarization, guardrails for HIPAA alignment, SOAP/ICD form automation). It is designed to be “out-of-the-box” for clinical scenarios.

## Additional Voice Agent Examples

1. **Scalable Voice-to-Voice Workflow:** Production reference Kubernetes deployment using NVIDIA NIM for optimized inference, featuring custom Prometheus and Grafana observability. [GitHub Repository](https://github.com/SDcodehub/voice-voice-workflow)
2. **Integrated ASR+EOU**, tracking different speakers across turns, tool calling, evaluation pipeline: [GitHub Repository](https://github.com/NVIDIA-NeMo/NeMo/tree/main/examples/voice_agent)
3. **Daily/Pipecat** - This repo is sample code for building voice agents with three NVIDIA open source models: Nemotron Speech ASR, Nemotron 3 Nano LLM, Magpie TTS (Preview) [GitHub Repository](https://github.com/pipecat-ai/nemotron-january-2026/). Read the [blog post](https://www.daily.co/blog/building-voice-agents-with-nvidia-open-models/) for more details. Deployed on DGX Spark.
4. Vertical examples - five examples from different verticals to converse with a voice agent - [https://github.com/fciannella/nemotron-speech-demos/tree/main](https://github.com/fciannella/nemotron-speech-demos/tree/main).
	1. Claim Investigatr (Tier 1)
		2. Healthcare Agent
		3. Banking Fee Inquiry Resolver
		4. Telco Agent: Billing Specialist
		5. Wire Transfer Agent with Twilio integration. (Call transfer) included.
5. [Ambient Healthcare Agents](https://build.nvidia.com/nvidia/ambient-healthcare-agents) + Guardrails - [Github Repository](https://github.com/NVIDIA-AI-Blueprints/ambient-healthcare-agents)
6. NeMo Agent Toolkit Observability: Logging, metrics, and traces for production monitoring. [GitHub Repository](https://github.com/NVIDIA/voice-agent-examples/tree/main/examples/nat_agent)

## Ethical considerations

NVIDIA believes trustworthy AI is a shared responsibility. When using this example in accordance with our terms of service, work with your model and compliance teams to ensure the system meets requirements for your industry and use case. Report security or AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).