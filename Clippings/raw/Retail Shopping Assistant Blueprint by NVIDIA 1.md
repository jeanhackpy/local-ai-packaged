---
title: "Retail Shopping Assistant Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/retail-shopping-assistant"
author:
published:
created: 2026-04-05
description: "Elevate Shopping Experiences Online and In Stores."
tags:
  - "clippings"
---
j

With AI shopping assistants, retailers can deliver more engaging customer interactions, around the clock and across the world.

A retail shopping assistant needs to have personalization and the ability to answer long-tail, complex questions. However, current tools typically only perform well for shorter based, keyword oriented queries. This leads to scenarios where customers cannot find everything they are seeking or require assistance in ideating on the products they need. Whether it is curating all the necessary items for a backyard or trying to create a soccer themed birthday party for your child, the search process can often take multiple attempts and in some cases to no avail. This not only frustrates the consumer, but also represents a lost opportunity for the retailer to capture revenue and drive up-sell and cross-sell.

This NVIDIA AI Blueprint provides a reference example to enhance customer experiences, drive higher conversion rates, lower product return rates and increase the average size of orders through highly intelligent, personalized suggestions of complementary products or upgrades. It shows developers how NVIDIA NIM™ microservices can be used to develop solutions that enable more natural, personalized online shopping experiences. It features [NVIDIA AI Enterprise](https://www.nvidia.com/en-us/data-center/products/ai-enterprise/) software, including [NVIDIA NIM](https://www.nvidia.com/en-us/ai/) ™ microservices for Meta Llama 3.1 70B, NVIDIA Retrieval QA E5 Embedding v5 to deliver AI performance at scale, and [NVIDIA NeMo Guardrails](https://developer.nvidia.com/nemo-guardrails/) safety features.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/retail-shopping-assistant/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/retail-shopping-assistant/diagram.jpg)

## Key Features

- An end-to-end sample multimodal, multi-query agentic RAG pipeline that includes image-to-image similarity search with NVClip, enabling consumers to use text and images in queries
- Optimized LLM inference performance and scaling through NIM, including the Llama 3.1 70B NIM microservice bringing reasoning capabilities to AI shopping assistants for natural, humanlike interactions
- Guardrails that help ensure customer conversations with the shopping assistant remain safe and on-topic, protecting brand values
- World-class information retrieval delivers high accuracy and data privacy with NVIDIA Retrieval QA E5 Embedding v5
- Integration with LangChain and the NVIDIA cuVS GPU-accelerated Milvus vector database (illustrated in the below workflow)
- Sample retail product catalog and imagery with the ability to ingest retailers’ product catalog text and image data for accurate, context-aware responses
- The flexibility to use other models from the NVIDIA API catalog or self-hosted models

[![](https://assets.ngc.nvidia.com/products/api-catalog/retail-shopping-assistant/screenshot1.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/retail-shopping-assistant/screenshot1.jpg)

## Minimum System Requirements

### Hardware Requirements

- Expect that you will want the NIM microservices to be self-hosted as you progress in your RAG development. For self-hosting the blueprint with these microservices locally deployed, the recommended system requirement is 4 H100 GPUs with the Llama 3.1 70B NIM, the NVIDIA Retrieval QA E5 Embedding and NVCLIP NIMs, and the Milvus database accelerated with NVIDIA cuVS.

### Deployment Options

- Docker

## Software Used in This Blueprint

**NVIDIA Technology**

- [NVIDIA Retrieval QA E5 Embedding v5](https://build.nvidia.com/nvidia/nv-embedqa-e5-v5)
- [NVclip](https://build.nvidia.com/nvidia/nvclip)
- [Llama 3.1 70B Instruct NIM](https://build.nvidia.com/meta/llama-3_1-70b-instruct)
- [Llama 3.1 Nemoguard 8B Topic Control](https://build.nvidia.com/nvidia/llama-3_1-nemoguard-8b-topic-control)
- L [lama 3.1 Nemoguard 8B Content Safety](https://build.nvidia.com/nvidia/llama-3_1-nemoguard-8b-content-safety)

**3rd Party Software**

- [LangChain](https://www.langchain.com/)
- Milvus database (accelerated with NVIDIA [**cuVS**](https://github.com/rapidsai/cuvs))
- SQLite

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility, and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their supporting model team to ensure the models meet requirements for the relevant industry and use case and address unforeseen product misuse. For more detailed information on ethical considerations for the models, please see the Model Card++ Explainability, Bias, Safety & Security, and Privacy Subcards. Please report security vulnerabilities or NVIDIA AI concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

GOVERNING TERMS: Use of the blueprint software and materials and NIM containers are governed by the [NVIDIA Software License Agreement](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-software-license-agreement/) and [Product-specific Terms for AI products](https://www.nvidia.com/en-us/agreements/enterprise-software/product-specific-terms-for-ai-products/); and the use of models is governed by the [NVIDIA Community Model License](https://www.nvidia.com/en-us/agreements/enterprise-software/nvidia-community-models-license/).

ADDITIONAL INFORMATION: [Llama 3.1 Community License Agreement](https://www.llama.com/llama3_1/license/) for Llama 3.1 70B Instruct NIM, Llama 3.1 NemoGuard 8B - Content Safety and Llama 3.1 NemoGuard 8B - Topic Control models, built with Llama, (ii) MIT license for NV-EmbedQA-E5-v5.

Use of the product catalog data in the retail shopping assistant is governed by the terms of the [NVIDIA Data License for Retail Shopping Assistant (15Aug2025)](https://github.com/NVIDIA-AI-Blueprints/retail-shopping-assistant/blob/main/LICENSE-assets.txt).