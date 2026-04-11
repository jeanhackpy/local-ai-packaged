---
title: "Streaming Data to RAG Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/streaming-data-to-rag"
author:
published:
created: 2026-04-05
description: "Sensor-captured radio enables real-time awareness, AI-driven analytics for actionable, searchable insights."
tags:
  - "clippings"
---
j

![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fstreaming-data-to-rag.jpg&w=3840&q=75)

## Streaming Data to RAG

Sensor-captured radio enables real-time awareness, AI-driven analytics for actionable, searchable insights.

Traditional retrieval-augmented generation (RAG) systems rely on static data ingested in batches, which limits their ability to support time-critical use cases like emergency response or live monitoring. These situations require immediate access to dynamic data sources such as sensor feeds or radio signals.

The Streaming Data to RAG developer example solves this by enabling RAG systems to process live data streams in real-time. It features a GPU-accelerated software-defined radio (SDR) pipeline that continuously captures radio frequency (RF) signals, transcribes them into searchable text, embeds, and indexes them in real time. This live data is then fed to a large language model (LLM), allowing context-aware queries over dynamic streams.

Designed for scalability across edge and cloud environments, this reference example unlocks real-time situational awareness for use cases like spectrum monitoring, intelligence gathering, and other mission-critical applications—while retaining RAG’s strengths in delivering accurate, relevant results.

To learn more about how this blueprint is applied in real-world implementations, check out the detailed tech blogs from [Deepwave](https://deepwave.ai/news/mission-ready-ai-radio-intelligence-at-the-edge/) and [DataRobot](https://www.datarobot.com/blog/radio-intelligence-ai-agent/).

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/streaming-data-to-rag/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/streaming-data-to-rag/diagram.jpg)

## Key Features

- **Real-Time RF Signal Ingestion**: Capture and process live FM radio signals via UDP data streams with enterprise-grade reliability
- **GPU-Accelerated Processing**: Leverage NVIDIA Holoscan and Riva for high-performance, scalable signal processing pipelines
- **Seamless RAG Integration**: Built on proven Video Search and Summarization (VSS) blueprint architecture for immediate deployment
- **Automatic Speech Recognition (ASR)**: Convert decoded audio streams into structured text optimized for LLM ingestion
- **Context-Aware Querying**: Enable time-based queries such as "Summarize the last 5 minutes" with intelligent temporal awareness
- **Interactive Chat Interface**: Intuitive conversation interface for querying and analyzing streaming RF data in real-time
- **Sub-5-Second Latency**: Transcribe speech to text in real-time
- **Continuous Document Ingestion**: Achieve end-to-end ingestion and context update processing with minimal delay for time-critical applications.
- **Comprehensive Monitoring**: Built-in pipeline health monitoring, logging, and error tracking for production-ready deployments
- **Containerized Deployment**: Docker Compose-based deployment for easy integration into existing development workflows
- **Developer-Friendly Toolkit**: Includes notebook tutorials, NVIDIA Launchable, and comprehensive documentation for rapid prototyping
- **Audio File Playback Support**: Test and develop with audio file inputs that simulate live radio streams for development environments

## Minimum System Requirements

### Hardware

- For Data Center Deployment: NVIDIA L40, L40S, or any data center GPU of equal or greater capability
- For Desktop Deployment: NVIDIA RTX™ 5090, RTX A6000, or equivalent high-end consumer or professional GPU
- VRAM: 24 GB

These GPUs ensure sufficient memory and compute resources for advanced AI, visualization, and generative workloads.

### Software

- OS Requirements: Ubuntu 22.04
- Deployment: Docker Compose

**NVIDIA Technology**

- [Llama NeMo Retriever 3.2 embedding NIM](https://build.nvidia.com/nvidia/llama-3_2-nv-embedqa-1b-v2) (deployed locally)
- [Llama NeMo Retriever 3.2 reranking NIM](https://build.nvidia.com/nvidia/llama-3_2-nv-rerankqa-1b-v2) (API endpoint)
- [NVIDIA Riva Parakeet ASR NIM](https://build.nvidia.com/nvidia/parakeet-ctc-0_6b-asr) (deployed locally)
- [NVIDIA Nemotron Nano 9b v2](https://build.nvidia.com/nvidia/nvidia-nemotron-nano-9b-v2) (API endpoint)
- [NVIDIA Holoscan](https://github.com/nvidia-holoscan)
- [NVIDIA NeMo Agent Toolkit UI](https://github.com/NVIDIA/NeMo-Agent-Toolkit-UI)
- [Context Aware RAG](https://github.com/NVIDIA/context-aware-rag)

**3rd Party Software**

- [PyTorch](https://pytorch.org/)
- [CuPy](https://cupy.dev/)
- [Librosa](https://librosa.org/)

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility, and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure the models meet requirements for the relevant industry and use case and address unforeseen product misuse. Please report security vulnerabilities or NVIDIA AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

Use of the models in this blueprint is governed by the [NVIDIA AI Foundation Models Community License](https://docs.nvidia.com/ai-foundation-models-community-license.pdf).

## Terms of Use

The software and materials are governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and the [Product-Specific Terms for AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/); except for NVIDIA Nemotron Nano 9B v2, which is governed by the the [NVIDIA Open Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-open-model-license/); the other models, which are governed by the [NVIDIA Community Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-community-models-license/); the NVIDIA NeMo Agent Toolkit UI, which is governed by the [MIT License](https://github.com/NVIDIA/NeMo-Agent-Toolkit-UI/blob/main/LICENSE); the NVIDIA Holoscan SDK and the NVIDIA Context Aware RAG, which are governed by the [Apache 2.0 License](https://www.apache.org/licenses/LICENSE-2.0); and the audio files, which are licensed under the [Creative Commons Attribution 4.0 International License (CC BY 4.0)](https://creativecommons.org/licenses/by/4.0/legalcode).

#### Additional Information

For llama-3.2-nv-embedqa-1b-v2 and llama-3.2-nv-rerankqa-1b-v2, the [Llama 3.2 Community License Agreement](https://www.llama.com/llama3_2/license/). Built with Llama.