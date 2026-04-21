# Wiki Index

> Catalogue du wiki. Mis à jour lors de chaque ingest.

**Dernière mise à jour** : 2026-04-21 (full ingest complete)

---

## Vue d'ensemble

Wiki maintenu par LLM selon [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
65 sources dans `raw/`. Résumés dans `sources/`. Voir [WIKI_SCHEMA.md](WIKI_SCHEMA.md) pour le workflow complet.

---

## Synthesis (2 analyses transversales)

- [[synthesis/ai-factory-for-real-estate]] — NVIDIA blueprints + Palanthai stack → AI factory architecture for Thai property intelligence
- [[synthesis/thailand-property-intelligence]] — FazWaz + valuation research + deal intelligence → data layer for Thai real estate AI

---

## Concepts (14)

### AI/ML Applied
- [[concepts/agentic-ai]] — AI that executes actions, not just generates content
- [[concepts/rag]] — Retrieval Augmented Generation + hybrid search + reranking
- [[concepts/data-flywheel]] — Continuous model improvement from production data
- [[concepts/data-pipeline]] — ETL: crawl → extract → embed → index (Supabase + Qdrant + Neo4j)
- [[concepts/knowledge-extraction]] — Structured knowledge from conversational transcripts
- [[concepts/voice-ai]] — Cascaded ASR → LLM → TTS pipelines for spoken dialogue
- [[concepts/vlm]] — Vision Language Models for property images, floor plans, satellite
- [[concepts/security]] — Container vulnerability analysis, CVE RAG, encryption-in-use

### Domain
- [[concepts/immobilier-thailand]] — Thai real estate market structure and platforms
- [[concepts/property-valuation]] — Multi-modal AI valuation (text + images + geo + floor plans)
- [[concepts/digital-twins]] — Virtual property simulation and tourism heritage
- [[concepts/computer-vision]] — Image analysis for real estate (facade, floor plan, satellite)
- [[concepts/trust]] — Trust infrastructure: provenance, uncertainty, transparency
- [[concepts/urban-analysis]] — Spatial analysis: street conditions, price indices, GIS

---

## Entities (2)

- [[entities/nvidia]] — GPU/AI, NIM microservices, NVIDIA Blueprints (11 blueprints)
- [[entities/fazwaz]] — Thailand's dominant property marketplace (60k+ listings)

---

## Sources (65 raw, summaries in progress)

Raw sources: `raw/[filename].md`
Source summaries: `sources/[slug].md`

### NVIDIA Blueprints (22)
[[sources/nvidia-omniverse-dsx-blueprint]] | [[sources/build-ai-virtual-assistant-blueprint]] | [[sources/build-ai-virtual-assistant]] | [[sources/ambient-healthcare-agents-blueprint]] | [[sources/ambient-healthcare-agents]] | [[sources/retail-agentic-commerce-blueprint]] | [[sources/retail-agentic-commerce]] | [[sources/retail-shopping-assistant-blueprint]] | [[sources/retail-shopping-assistant]] | [[sources/retail-catalog-enrichment-blueprint]] | [[sources/retail-catalog-enrichment]] | [[sources/streaming-data-rag]] | [[sources/streaming-data-to-rag-blueprint]] | [[sources/nemotron-voice-agent-blueprint]] | [[sources/nemotron-voice-agent]] | [[sources/container-security-vulnerability]] | [[sources/vulnerability-analysis-container-security]] | [[sources/cyborg-enterprise-rag-blueprint]] | [[sources/cyborg-enterprise-rag]] | [[sources/ai-observability-data-flywheel-wandb]] | [[sources/ai-observability-data-flywheel-weights-biases]] | [[sources/ai-orchestration-data-flywheel-iguazio]] | [[sources/ai-orchestration-data-flywheel-mlrun]]

### AI/ML Research & Architecture (12)
[[sources/deloitte-agentic-ai-lessons]] | [[sources/rag-reranker-setup]] | [[sources/rag-plus-reranker]] | [[sources/from-transcripts-to-ai-agents]] | [[sources/data-pipeline-unit-recommendations]] | [[sources/data-processing]] | [[sources/dataflow-architecture]] | [[sources/deep-learning-electronic-service-quality]] | [[sources/zero-shot-neuro-symbolic-architecture]] | [[sources/architecture-of-trust-real-estate]] | [[sources/trust-infrastructure-data]] | [[sources/custom-instructions-guide]]

### Thailand Real Estate (19)
[[sources/fazwaz-premium]] | [[sources/bot-sniper-immobilier]] | [[sources/extracteur-donnees-immobilieres-thailandaises]] | [[sources/systeme-ontologique]] | [[sources/palanthai-opensource-stack]] | [[sources/sansiri-prd]] | [[sources/yc-combinator-spitch]] | [[sources/multi-modal-house-price-prediction]] | [[sources/probabilistic-disaggregation-property-value]] | [[sources/gcn-floor-plan-valuation]] | [[sources/visual-modalities-missing-data]] | [[sources/self-supervised-vit-valuation]] | [[sources/thailand-satellite-valuation]] | [[sources/building-condition-patch-convnet]] | [[sources/sub-city-price-index-forecasting]] | [[sources/rotterdam-spatial-analysis]] | [[sources/ensemble-decision-real-estate-images]] | [[sources/online-advertising-spatial-interactions]] | [[sources/digital-twins-tourism-heritage]]

---

## Stats

- **raw/** : 65 sources
- **sources/** : 57 source summaries (all 65 raw files covered — some raw files are duplicates with different filenames)
- **concepts/** : 14
- **entities/** : 2
- **synthesis/** : 2

Voir [[log]] pour l'historique complet.
