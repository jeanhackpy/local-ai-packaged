---
title: "Cyborg Enterprise RAG Blueprint by Cyborg"
source: "https://build.nvidia.com/cyborg/cyborg-enterprise-rag"
author:
published:
created: 2026-04-05
description: "Securely extract, embed, and index multimodal data with encryption in-use for fast, accurate semantic search."
tags:
  - "clippings"
---
j

Connect AI applications to multimodal enterprise data with a scalable retrieval augmented generation (RAG) pipeline built on highly performant, industry-leading NIM microservices, enhanced with enterprise-grade vector database security through CyborgDB's encryption-in-use capabilities.

The Cyborg Enterprise RAG Blueprint gives developers a foundational starting point for building scalable, customizable retrieval pipelines that deliver both high accuracy, throughput, and enterprise security. Use this blueprint to build RAG applications that provide context-aware responses by connecting LLMs to extensive multimodal enterprise data—including text, tables, charts, and infographics from millions of PDFs—while maintaining encryption-in-use for vector embeddings. With 15x faster multimodal PDF data extraction, 50% fewer incorrect answers, and zero plaintext exposure of vector data, enterprises can unlock actionable insights from data and drive productivity at scale with enhanced security.

This blueprint can be used as-is, combined with other NVIDIA Blueprints, such as the Digital Human blueprint or the AI Assistant for customer service blueprint, or integrated with an agent to support more advanced use cases. Get started with this reference architecture to ground AI-driven decisions in relevant enterprise data with enterprise-grade vector database security - wherever it resides.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/cyborg-enterprise-rag/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/cyborg-enterprise-rag/diagram.jpg)

## What’s Included in the Blueprint

This blueprint provides an example and documentation of an end-to-end secure enterprise RAG using CyborgDB and its encrypted vector embedding functionality along with other NIM components involving multi-modal data ingestion, context-aware interactions with LLMs and retrieval / reranking.

## Key Features

- Multimodal PDF data extraction support with text, tables, charts, and infographics
- Support for audio file ingestion
- Native Python library support
- Custom metadata support
- Multi-collection searchability
- Opt-in for Vision Language Model (VLM) Support in the answer generation pipeline.
- Document summarization
- Hybrid search with dense and sparse search
- Opt-in image captioning with vision language models (VLMs)
- Reranking to further improve accuracy
- GPU-accelerated Index creation and search
- Multi-turn conversations
- Multi-session support
- Telemetry and observability
- Opt-in for reflection to improve accuracy
- Opt-in for guardrailing conversations
- Sample user interface
- OpenAI-compatible APIs
- Decomposable and customizable
- Encryption-in-use for vector embeddings
- Customer-controlled key management (BYOK/HYOK)
- Zero plaintext exposure of vector data
- Multi-tenant isolation and workload segregation

## Minimum System Requirements

#### Hardware Requirements

The blueprint offers two primary modes of deployment. By default, it deploys the referenced NIM microservices locally. Each method lists its minimum required hardware. This will change if the deployment turns on optional configuration settings.

##### Docker

- 2xH100 or 3xA100
- 32GB+ RAM (additional overhead for encryption operations)

##### Kubernetes

- 8xH100-80GB or 9xA100-80GB
- 64GB+ RAM for production workloads

#### OS Requirements

- Ubuntu 22.04 OS

#### Deployment Options

- Docker
- Kubernetes

### Included NIM Microservices

#### NVIDIA Technology

The following [NIM](https://www.nvidia.com/en-us/ai/) microservices are used in this blueprint:

- [NeMo Retriever Llama 3.2 embedding NIM](https://build.nvidia.com/nvidia/llama-3_2-nv-embedqa-1b-v2)
- [NeMo Retriever Llama 3.2 reranking NIM](https://build.nvidia.com/nvidia/llama-3_2-nv-rerankqa-1b-v2)
- [Llama 3.3 Nemotron Super 49B v1 NIM](https://build.nvidia.com/nvidia/llama-3_3-nemotron-super-49b-v1)
- [NeMo Retriever page elements NIM](https://build.nvidia.com/nvidia/nemoretriever-page-elements-v2)
- [NeMo Retriever table structure NIM](https://build.nvidia.com/nvidia/nemoretriever-table-structure-v1)
- [NeMo Retriever graphic elements NIM](https://build.nvidia.com/baidu/paddleocr)
- [PaddleOCR NIM](https://build.nvidia.com/baidu/paddleocr)
- [NeMo Retriever parse NIM](https://build.nvidia.com/nvidia/nemoretriever-parse) (optional)
- [Llama 3.1 NemoGuard 8B content safety NIM](https://build.nvidia.com/nvidia/llama-3_1-nemoguard-8b-content-safety) (optional)
- [Llama 3.1 NemoGuard 8B topic control NIM](https://build.nvidia.com/nvidia/llama-3_1-nemoguard-8b-topic-control) (optional)
- [Llama 3.2 11B vision instruct NIM](https://build.nvidia.com/meta/llama-3.2-11b-vision-instruct) (optional)
- [Mixtral 8x22B instruct 0.1](https://build.nvidia.com/mistralai/mixtral-8x22b-instruct) (optional)

#### 3rd Party Software

- [LangChain](https://www.langchain.com/)
- [CyborgDB secure vector database (PostgreSQL with pgvector and transparent encryption proxy)](https://docs.cyborg.co/)
- [Redis](https://redis.io/)

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility, and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure the models meet requirements for the relevant industry and use case and address unforeseen product misuse. For more detailed information on ethical considerations for the models, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards. Please report security vulnerabilities or NVIDIA AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

Use of the models in this AI virtual assistant for customer service blueprint is governed by the [NVIDIA AI Foundation Models Community License](https://docs.nvidia.com/ai-foundation-models-community-license.pdf).

CyborgDB components require separate commercial licensing.

## Terms of Use

The software, NIM microservices and materials are governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and the Product-Specific Terms for [NVIDIA AI Products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/), except that models are governed by the [NVIDIA Community Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-community-models-license/). The NVIDIA RAG Dataset is governed by the [NVIDIA Asset License Agreement](https://github.com/NVIDIA-AI-Blueprints/rag/blob/main/data/LICENSE.DATA). If this Blueprint is deployed using NVIDIA API endpoints on build.nvidia.com, use of the service is governed by [NVIDIA API Trial Terms of Service](https://assets.ngc.nvidia.com/products/api-catalog/legal/NVIDIA%20API%20Trial%20Terms%20of%20Service.pdf).

### ADDITIONAL INFORMATION

The [Llama 3.1 Community License Agreement](https://www.llama.com/llama3_1/license/) for the llama-3.1-nemoguard-8b-content-safety and llama-3.1-nemoguard-8b-topic-control models. The [Llama 3.2 Community License Agreement](https://www.llama.com/llama3_2/license/) for the nvidia/llama-3.2-nv-embedqa-1b-v2, nvidia/llama-3.2-nv-rerankqa-1b-v2 and llama-3.2-11b-vision-instruct models. The [Llama 3.3 Community License Agreement](https://github.com/meta-llama/llama-models/blob/main/models/llama3_3/LICENSE) for the llama-3.3-nemotron-super-49b-v1 model. Built with Llama. Apache 2.0 for NVIDIA Ingest and for the nemoretriever-page-elements-v2, nemoretriever-table-structure-v1, nemoretriever-graphic-elements-v1, paddleocr and mixtral-8x22b-instruct-v0.1 models.