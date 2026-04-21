# Thailand Property Intelligence

> Analyse transversale — FazWaz, Sansiri, valuation research, deal intelligence.

## Thesis

Thailand's property market is data-rich but poorly structured — 60k+ units listed across platforms with inconsistent attributes, dual-language descriptions, and minimal structured metadata. The opportunity is to build a property intelligence layer that: (1) aggregates and normalizes fragmented listing data, (2) applies multi-modal valuation models to fill gaps, and (3) delivers trustworthy recommendations through an agentic interface. The NVIDIA AI stack + academic valuation research + Palanthai's open-source implementation form the complete picture.

---

## 1. The Data Problem — Fragmentation

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/fazwaz-premium]] | 60k+ listings, 10-portal syndication, but inconsistent structured data |
| [[sources/extracteur-donnees-immobilieres-thailandaises]] | Scraping guide for FazWaz, DDProperty, Hipflat, Baania |
| [[sources/sansiri-prd]] | Sansiri's PRD reveals developer-side data structure: project → building → unit |
| [[sources/systeme-ontologique]] | Ontology: location → property type → features → pricing layers |
| [[sources/bot-sniper-immobilier]] | Draft: AI bot for real-time deal identification across platforms |

### Key insight

FazWaz is the dominant aggregator but its data is marketing material, not structured property intelligence. The ontology source defines the right schema (location hierarchy, property type taxonomy, feature layers, pricing). The extraction pipeline (PydanticAI PropertyDoc model) is the operationalization.

### Implication

1. **Crawl + structure first** — n8n + Crawl4AI + PydanticAI (per rag-reranker-setup pipeline)
2. **Normalize to ontology** — transform raw listings into: project_id, building_id, unit_id, geo, type, bedrooms, area, price, features, developer
3. **Track provenance** — source URL, fetch date, lastmod, for trust/attribution

---

## 2. Valuation — Multi-Modal is Non-Negotiable

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/multi-modal-house-price-prediction]] | Embeddings from text + images + geo outperform single-modality models |
| [[sources/gcn-floor-plan-valuation]] | GCN on floor plan graphs captures spatial relationships rooms can't |
| [[sources/thailand-satellite-valuation]] | Satellite/aerial imagery captures neighborhood quality |
| [[sources/self-supervised-vit-valuation]] | Self-supervised ViT avoids labeled data bottleneck |
| [[sources/probabilistic-disaggregation-property-value]] | Probabilistic disaggregation handles mixed-use property attribution |
| [[sources/building-condition-patch-convnet]] | Patch ConvNets assess building facade condition from images |
| [[sources/visual-modalities-missing-data]] | Multi-modal learning with missing modalities (e.g., no floor plan available) |
| [[sources/architecture-of-trust-real-estate]] | Trust framework: uncertainty quantification, provenance, model honesty |

### Key insight

**No single modality is sufficient for Thai property valuation.** The academic literature converges: best results combine structured attributes (price/sqm, bedrooms) + text descriptions + images (facade, interior, floor plan) + geo context (BTS proximity, amenities, neighborhood). Self-supervised pre-training reduces the labeled data bottleneck that makes Thai real estate ML hard.

### Implication for Palanthai

1. **Multi-modal embeddings** — encode listing text + images + floor plan into a joint vector
2. **GCN for floor plans** — graph convolutional networks capture room adjacency (verified superior to CNN)
3. **Satellite for neighborhood** — combine with on-the-ground data (schools, malls, transit) for location features
4. **Uncertainty quantification** — the trust framework requires knowing what the model doesn't know; probabilistic outputs are essential

---

## 3. Trust Infrastructure — Honest AI for High-Stakes Decisions

### Source evidence

| Source | Contribution |
|--------|-------------|
| [[sources/architecture-of-trust-real-estate]] | UAD 3.6 framework: structured data + AI + human expertise |
| [[sources/trust-infrastructure-data]] | Trust as a data problem: provenance, lineage, freshness |
| [[sources/deep-learning-electronic-service-quality]] | Service quality scoring for real estate websites |

### Key insight

Property transactions are high-stakes. A valuation that appears precise but lacks provenance is worse than no valuation. The trust framework requires:
1. **Data provenance** — where did this price estimate come from?
2. **Model uncertainty** — what's the confidence interval?
3. **Freshness** — when was this data last updated?
4. **Alignment** — who benefits if the AI says the price is higher?

### Implication

Build the trust layer before the valuation layer. Every unit in Qdrant should carry metadata: source, fetch_date, lastmod, embedding_model_version, valuation_model_version, confidence_score.

---

## 4. The Path Forward — Phases

| Phase | Focus | Key source |
|-------|-------|------------|
| **Phase 1** | Crawl + structure + RAG | [[sources/rag-reranker-setup]], [[sources/extracteur-donnees-immobilieres-thailandaises]] |
| **Phase 2** | Embeddings + hybrid search | [[sources/palanthai-opensource-stack]], [[sources/rag-plus-reranker]] |
| **Phase 3** | Multi-modal valuation | [[sources/multi-modal-house-price-prediction]], [[sources/gcn-floor-plan-valuation]] |
| **Phase 4** | Agentic interface | [[sources/retail-shopping-assistant-blueprint]], [[sources/ambient-healthcare-agents]] |
| **Phase 5** | Data flywheel + fine-tuning | [[sources/ai-orchestration-data-flywheel-mlrun]], [[sources/ai-observability-data-flywheel-wandb]] |

---

**Sources**: [[sources/fazwaz-premium]], [[sources/sansiri-prd]], [[sources/extracteur-donnees-immobilieres-thailandaises]], [[sources/systeme-ontologique]], [[sources/multi-modal-house-price-prediction]], [[sources/gcn-floor-plan-valuation]], [[sources/thailand-satellite-valuation]], [[sources/self-supervised-vit-valuation]], [[sources/probabilistic-disaggregation-property-value]], [[sources/architecture-of-trust-real-estate]], [[sources/trust-infrastructure-data]], [[sources/bot-sniper-immobilier]]
