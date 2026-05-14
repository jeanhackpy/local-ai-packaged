---
created: 2026-04-05
tags:
  - nvidia
  - blueprint
  - retail
  - catalog
  - genai
  - localization
  - 3d
---

# Retail Catalog Enrichment Blueprint by NVIDIA

## Summary

GenAI system that transforms basic product images into comprehensive catalog entries with AI-generated descriptions, variation images, 3D assets, and automated quality assessment. Supports 10 regional locales for culturally-authentic global shopping experiences.

## Key Concepts

- **NVIDIA Nemotron VLM**: Visual product analysis and content augmentation
- **NVIDIA Nemotron LLM**: Culturally-aware prompt planning for regional variations
- **FLUX Kontext**: Localized product image generation with culturally-appropriate backgrounds
- **Microsoft TRELLIS**: 3D asset generation (GLB models) from product images
- **10 Regional Locales**: Multi-language titles, descriptions, and cultural image variations
- **VLM Quality Assessment**: Automated evaluation of generated images with scoring
- **Modular API Architecture**: Separate endpoints for VLM analysis, image gen, 3D assets

## Connections

- [[sources/retail-shopping-assistant-blueprint-by-nvidia]] — Enriched catalogs power better recommendations
- [[sources/retail-agentic-commerce-blueprint-by-nvidia]] — Upstream catalog data source
- [[concepts/vlm]] — Vision Language Models technology