---
title: "Retail Catalog Enrichment Blueprint by NVIDIA"
source: "https://build.nvidia.com/nvidia/retail-catalog-enrichment"
author:
published:
created: 2026-04-05
description: "A GenAI system that enhances and localizes product catalogs with rich text content and imagery."
tags:
  - "clippings"
---
j

![](https://build.nvidia.com/_next/image?url=https%3A%2F%2Fassets.ngc.nvidia.com%2Fproducts%2Fapi-catalog%2Fimages%2Fretail-catalog-enrichment.jpg&w=3840&q=75)

## Retail Catalog Enrichment

A GenAI system that enhances and localizes product catalogs with rich text content and imagery.

[nemotron-nano-12b-v2-vl](https://build.nvidia.com/nvidia/nemotron-nano-12b-v2-vl) [nemotron-3-nano-30b-a3b](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b) [flux\_1-kontext-dev](https://build.nvidia.com/black-forest-labs/flux_1-kontext-dev) [trellis](https://build.nvidia.com/microsoft/trellis)

[NVIDIA AI](https://build.nvidia.com/blueprints?filters=blueprintType%3Ablueprinttype_nvidia_ai) [nim](https://build.nvidia.com/blueprints?label=nim)

With AI-powered catalog enrichment, retailers can transform basic product images into comprehensive, engaging catalog entries that drive discovery, conversion, and customer confidence across global markets.

Product catalogs often suffer from minimal, low-quality information with basic images and sparse descriptions that limit customer engagement and search discoverability. Manual enrichment is time-consuming, error-prone, and doesn't scale. Human categorization is particularly susceptible to inconsistencies and classification errors that negatively impact search functionality. Moreover, catalogs quickly become outdated as market trends evolve, and catalog managers lack visibility into how customers actually use products in real-world contexts, what terminology resonates with audiences, and what trends are emerging on social media. This disconnect between catalog content and market reality leads to missed opportunities for engagement, conversion, and revenue growth.

This NVIDIA AI developer example provides a reference to enhance product discoverability, drive higher conversion rates, and deliver culturally-authentic shopping experiences through AI-generated product descriptions, variation images, 3D assets, and automated quality assessment. It shows developers how NVIDIA NIM™ microservices can be used to develop solutions that augment existing product data with rich, localized content while maintaining brand consistency. It features NVIDIA AI Enterprise software, including NVIDIA NIM™ microservices for NVIDIA Nemotron VLM for visual product analysis and content augmentation, NVIDIA Nemotron LLM for culturally-aware prompt planning, FLUX Kontext model for generating localized product variations, Microsoft TRELLIS for 3D asset generation, and VLM-based reflection for automated quality assessment—delivering scalable AI performance with built-in quality control across 10 regional locales. Note that the FLUX.1-Kontext-Dev NIM uses a model that is for non-commercial use. Contact [sales@blackforestlabs.ai](mailto:sales@blackforestlabs.ai) for commercial terms.

## Architecture Diagram

[![](https://assets.ngc.nvidia.com/products/api-catalog/retail-catalog-enrichment/diagram.jpg)](https://assets.ngc.nvidia.com/products/api-catalog/retail-catalog-enrichment/diagram.jpg)

### Key Features

- **AI-Powered Analysis**: NVIDIA Nemotron VLM for intelligent product understanding
- **Smart Categorization**: Automatic classification into predefined product categories
- **Intelligent Prompt Planning**: Context-aware image variation planning based on regional aesthetics
- **Multi-Language Support**: Generate product titles and descriptions in **10 regional locales**
- **Cultural Image Generation**: Create culturally-appropriate product backgrounds (Spanish courtyards, Mexican family spaces, British formal settings)
- **Quality Evaluation**: Automated VLM-based quality assessment of generated images with detailed scoring
- **3D Asset Generation**: Transform 2D product images into interactive 3D GLB models using Microsoft TRELLIS
- **Modular API**: Separate endpoints for VLM analysis, image generation, and 3D asset generation

[Watch the YouTube demo to see the blueprint in action.](https://youtu.be/VGXCQeRZELg)

## Minimum System Requirements

### Hardware Requirements

- Expect that you will want the NIM microservices to be self-hosted as you progress in your catalog enrichment pipeline development. For self-hosting the project with these microservices locally deployed, the recommended system requirement is 4 H100 GPUs with the NVIDIA Nemotron VLM NIM for visual product analysis and content augmentation, the NVIDIA Nemotron LLM NIM for culturally-aware prompt planning and quality assessment, the FLUX NIM for localized product image generation, and the Microsoft TRELLIS model for 3D asset generation. Additionally, scalable storage infrastructure is required for managing generated assets including product variations, 3D models, metadata, and quality assessment artifacts.

### Deployment Options

- Docker 28.0+
- Docker compose

## Software Used in This Blueprint

**NVIDIA NIM Technology**

- [nemotron-nano-12b-v2-vl](https://build.nvidia.com/nvidia/nemotron-nano-12b-v2-vl)
- [nemotron-3-nano-30b-a3b](https://build.nvidia.com/nvidia/nemotron-3-nano-30b-a3b)
- [flux\_1-kontext-dev](https://build.nvidia.com/black-forest-labs/flux_1-kontext-dev)
- [trellis](https://build.nvidia.com/microsoft/trellis)

## Ethical Considerations

NVIDIA believes Trustworthy AI is a shared responsibility and we have established policies and practices to enable development for a wide array of AI applications. When downloaded or used in accordance with our terms of service, developers should work with their internal team to ensure this blueprint meets requirements for the relevant industry and use case and addresses unforeseen product misuse.

Please report quality, risk, security vulnerabilities or NVIDIA AI Concerns [here](https://www.nvidia.com/en-us/support/submit-security-vulnerability/).

## License

GOVERNING TERMS: The Blueprint scripts are governed by Apache License, Version 2.0, and enables use of separate open source and proprietary software governed by their respective licenses: [NVIDIA-Nemotron-Nano-12B-v2-VL](https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nemotron-nano-12b-v2-vl?version=1), [nemotron-3-nano-30b-a3b](https://catalog.ngc.nvidia.com/orgs/nim/teams/nvidia/containers/nemotron-3-nano/tags?version=latest), [FLUX.1-Kontext-Dev](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md), and [Microsoft TRELLIS](https://catalog.ngc.nvidia.com/orgs/nim/teams/microsoft/containers/trellis?version=1).

ADDITIONAL INFORMATION:  
FLUX.1-Kontext-Dev license: [https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev/blob/main/LICENSE.md)

Third-Party Community Consideration:  
The FLUX Kontext model is not owned or developed by NVIDIA. This model has been developed and built to a third-party’s requirements for this application and use case; see link to: black-forest-labs/FLUX.1-Kontext-dev Model Card - [https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev](https://huggingface.co/black-forest-labs/FLUX.1-Kontext-dev)