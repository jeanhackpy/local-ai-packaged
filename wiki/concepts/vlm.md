---
created: 2026-04-21
updated: 2026-04-21
tags: [concept, VLM, vision-language-models, multimodal, retail]
sources: [raw/retail-catalog-enrichment-blueprint-by-nvidia.md, raw/retail-catalog-enrichment-nvidia.md, raw/architecture-of-trust-real-estate-ai.md]
---

## Vision Language Models (VLM)

VLMs process both images and text simultaneously, enabling richer property understanding from visual content — floor plans, photos, satellite imagery, and street-view.

### Core Capabilities

- **Image captioning** — generate textual descriptions of property photos
- **Visual QA** — answer questions about property images ("does this unit have a balcony?")
- **Document understanding** — extract data from floor plan PDFs and property brochures
- **Multimodal retrieval** — find listings similar by image (image-to-image similarity search)

### NVIDIA Nemotron VLM

Used in retail catalog enrichment blueprint:
- **FLUX Kontext** — localized product image generation with culturally-appropriate backgrounds
- **Microsoft TRELLIS** — 3D asset generation (GLB models) from product images
- **VLM quality assessment** — automated scoring of generated images

### Application to Real Estate

| Task | VLM Application |
|------|----------------|
| Floor plan extraction | Graph structure + room labels from PNG/PDF |
| Property condition | Patch ConvNets for facade assessment |
| Satellite valuation | CNN/ViT on aerial imagery |
| Listing enrichment | Auto-generate Thai-language descriptions from photos |
| Image-to-image search | Find similar units by visual appearance |

## Sources

- [[sources/retail-catalog-enrichment-blueprint]]
- [[sources/architecture-of-trust-real-estate]]

## Connexions

- [[concepts/computer-vision]] — image analysis foundation
- [[concepts/property-valuation]] — VLMs power multi-modal valuation
- [[concepts/rag]] — multimodal RAG (text + images)
