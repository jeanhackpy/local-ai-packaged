---
title: "Retail Agentic Commerce Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/retail-agentic-commerce"
author:
published:
created: 2026-04-05
description: "Reference implementation of the Agentic Commerce Protocol (ACP) and Universal Commerce Protocol (UCP) enabling AI-powered checkout negotiation while maintaining merchant of record."
tags:
  - "clippings"
---
j

![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fretail-agentic-commerce.jpg&w=3840&q=75)

## Retail Agentic Commerce

Reference implementation of the Agentic Commerce Protocol (ACP) and Universal Commerce Protocol (UCP) enabling AI-powered checkout negotiation while maintaining merchant of record.

With AI-powered agentic commerce, retailers can enable AI agents to autonomously discover products, negotiate promotions, complete secure checkouts, and deliver personalized post-purchase experiences — all while maintaining full merchant control over pricing, payments, and compliance.

As AI agents become an interface for online shopping, retailers face a fundamental integration challenge. Today's e-commerce infrastructure was built for human-driven browser sessions, not autonomous agent workflows. There is no standardized way for AI agents to discover merchant capabilities, negotiate checkout terms, or process payments securely on a customer's behalf. Without a common protocol, each agent platform requires custom, fragile integrations that don't scale. Meanwhile, merchants risk losing control of critical business logic — dynamic pricing, inventory management, regulatory compliance — when delegating decisions to third-party agents. This gap between agent capabilities and merchant infrastructure limits conversion, erodes margins, and creates friction in the emerging agentic shopping experience.

This NVIDIA AI developer example provides a reference implementation for building secure, protocol-compliant agentic commerce systems that enable AI agents to conduct end-to-end shopping transactions under merchant authority. It shows developers how to implement dual-protocol support — the Agentic Commerce Protocol (ACP) and the Universal Commerce Protocol (UCP) — for standardized agent-to-merchant communication including discovery, checkout, delegated payments, and webhook-driven order lifecycle events. It features NVIDIA AI Enterprise software, including the NVIDIA NeMo Agent Toolkit for multi-agent orchestration, NVIDIA NIM™ microservices for NVIDIA Nemotron LLM for intelligent promotion strategy selection and multilingual post-purchase messaging, NV-EmbedQA-E5 for semantic product embeddings, and an Agentic Retrieval Augmented Generation (ARAG) recommendation pipeline with specialized agents for personalized cross-sell suggestions — delivering an Apps SDK integration with MCP server and merchant-owned widget, Milvus-powered vector search, and visibility into agent reasoning and checkout flow behavior.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/retail-agentic-commerce/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/retail-agentic-commerce/diagram.jpg)

### Key Features

- **Dual Protocol Support:** ACP and UCP implementation for standardized agent-to-merchant checkout, payments, and discovery
- **Intelligent Promotions:** NVIDIA Nemotron LLM-powered dynamic pricing based on real-time competitive signals and inventory pressure
- **ARAG Recommendations:** Multi-agent retrieval augmented generation pipeline with four specialized agents for personalized cross-sell suggestions
- **Semantic Product Search:** NV-EmbedQA-E5 embeddings with Milvus vector search for natural-language product discovery
- **Multilingual Post-Purchase:** AI-generated shipping updates in configurable brand tones and languages across the order lifecycle
- **Apps SDK Integration:** MCP server with merchant-owned widget for embedded cart, checkout, and recommendation experiences

## Minimum System Requirements

### Hardware Requirements

- Expect that you will want the NIM microservices to be self-hosted as you progress in your agentic commerce development. For self-hosting the project with these microservices locally deployed, the recommended system requirement is 2xA100 or 2xH100 GPUs — one for the NVIDIA Nemotron LLM NIM for intelligent promotion strategy selection, multilingual post-purchase messaging, and multi-agent recommendation orchestration, and one for the NV-EmbedQA-E5 NIM for semantic product embeddings powering vector search and the ARAG recommendation pipeline. Additionally, a Milvus vector database instance is required for product catalog embeddings, and Arize Phoenix is recommended for distributed tracing and observability across the multi-agent workflow.

### Deployment Options

- Docker 28.0+
- Docker compose

## Software Used in This Blueprint

**NVIDIA NIM Technology**

- [**nemotron-3-nano-30b-a3b**](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b)
- [**nv-embedqa-e5-v5**](https://build.nvidia.com/nvidia/nv-embedqa-e5-v5)

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal team to ensure this blueprint meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

GOVERNING TERMS: The Blueprint scripts are governed by Apache License, Version 2.0, and enables use of separate open source and proprietary software governed by their respective licenses: [Nemotron-Nano-V3](https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nemotron-3-nano?version=1.7.0), [NV-EmbedQA-E5-v5](https://build.nvidia.com/nvidia/nv-embedqa-e5-v5). The sample data is governed by the [NVIDIA Data License for Retail Agentic Commerce](https://github.com/NVIDIA-AI-Blueprints/Retail-Agentic-Commerce/blob/main/LICENSE-assets.txt).