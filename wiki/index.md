# Wiki Index

> Catalogue du wiki. Mis à jour lors de chaque ingest.

**Dernière mise à jour** : 2026-05-14 (mega-consolidation complete)

---

## Vue d'ensemble

Wiki maintenu par LLM selon [Karpathy LLM Wiki](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f).
117 sources dans `sources/`. Voir [WIKI_SCHEMA.md](WIKI_SCHEMA.md) pour le workflow complet.

---

## Synthesis (3 analyses transversales)

- [[synthesis/ai-factory-for-real-estate]] — NVIDIA blueprints + Palanthai stack → AI factory architecture for Thai property intelligence
- [[synthesis/thailand-property-intelligence]] — FazWaz + valuation research + deal intelligence → data layer for Thai real estate AI
- [[synthesis/mega-consolidation]] — 4 vaults merged: ObsiVault, Gemini-obsidian, OSINT, DEEPTECH → unified REcall OS knowledge

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
- [[concepts/recall-os]] — REcall OS: Palantir for Real Estate SEA

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

### AI/ML Research & Architecture (13)
[[sources/deloitte-agentic-ai-lessons]] | [[sources/rag-reranker-setup]] | [[sources/rag-plus-reranker]] | [[sources/from-transcripts-to-ai-agents]] | [[sources/data-pipeline-unit-recommendations]] | [[sources/data-processing]] | [[sources/dataflow-architecture]] | [[sources/deep-learning-electronic-service-quality]] | [[sources/zero-shot-neuro-symbolic-architecture]] | [[sources/architecture-of-trust-real-estate]] | [[sources/trust-infrastructure-data]] | [[sources/custom-instructions-guide]] | [[sources/s2vec-google-built-environment]]

### Thailand Real Estate (22)
[[sources/fazwaz-premium]] | [[sources/bot-sniper-immobilier]] | [[sources/extracteur-donnees-immobilieres-thailandaises]] | [[sources/systeme-ontologique]] | [[sources/palanthai-opensource-stack]] | [[sources/sansiri-prd]] | [[sources/yc-combinator-spitch]] | [[sources/multi-modal-house-price-prediction]] | [[sources/probabilistic-disaggregation-property-value]] | [[sources/gcn-floor-plan-valuation]] | [[sources/visual-modalities-missing-data]] | [[sources/self-supervised-vit-valuation]] | [[sources/thailand-satellite-valuation]] | [[sources/building-condition-patch-convnet]] | [[sources/sub-city-price-index-forecasting]] | [[sources/rotterdam-spatial-analysis]] | [[sources/ensemble-decision-real-estate-images]] | [[sources/online-advertising-spatial-interactions]] | [[sources/digital-twins-tourism-heritage]] | [[sources/asean-real-estate-2026-investor-map]] | [[sources/nationthailand-thai-property-developers-ltr-visas]] | [[sources/c9-sessions-phuket-property-maintenance-fees]]

---

## Stats

- **sources/** : 150 source summaries (complete ingestion)
- **raw/** : transit directory (files processed)
- **concepts/** : 14
- **entities/** : 2
- **synthesis/** : 3
- **External vaults integrated**: 4 (ObsiVault, Gemini-obsidian, OSINT, DEEPTECH)

---

## Sources by Vault

### NVIDIA Blueprints (22)
[[sources/nvidia-omniverse-dsx-blueprint]] | [[sources/build-ai-virtual-assistant-blueprint]] | [[sources/build-ai-virtual-assistant]] | [[sources/ambient-healthcare-agents-blueprint]] | [[sources/ambient-healthcare-agents]] | [[sources/retail-agentic-commerce-blueprint]] | [[sources/retail-agentic-commerce]] | [[sources/retail-shopping-assistant-blueprint]] | [[sources/retail-shopping-assistant]] | [[sources/retail-catalog-enrichment-blueprint]] | [[sources/retail-catalog-enrichment]] | [[sources/streaming-data-rag]] | [[sources/streaming-data-to-rag-blueprint]] | [[sources/nemotron-voice-agent-blueprint]] | [[sources/nemotron-voice-agent]] | [[sources/container-security-vulnerability]] | [[sources/vulnerability-analysis-container-security]] | [[sources/cyborg-enterprise-rag-blueprint]] | [[sources/cyborg-enterprise-rag]] | [[sources/ai-observability-data-flywheel-wandb]] | [[sources/ai-observability-data-flywheel-weights-biases]] | [[sources/ai-orchestration-data-flywheel-iguazio]]

### AI/ML Research & Architecture (13)
[[sources/deloitte-agentic-ai-lessons]] | [[sources/rag-reranker-setup]] | [[sources/rag-plus-reranker]] | [[sources/from-transcripts-to-ai-agents]] | [[sources/data-pipeline-unit-recommendations]] | [[sources/data-processing]] | [[sources/dataflow-architecture]] | [[sources/deep-learning-electronic-service-quality]] | [[sources/zero-shot-neuro-symbolic-architecture]] | [[sources/architecture-of-trust-real-estate]] | [[sources/trust-infrastructure-data]] | [[sources/custom-instructions-guide]] | [[sources/s2vec-google-built-environment]]

### Thailand Real Estate (22)
[[sources/fazwaz-premium]] | [[sources/bot-sniper-immobilier]] | [[sources/extracteur-donnees-immobilieres-thailandaises]] | [[sources/systeme-ontologique]] | [[sources/palanthai-opensource-stack]] | [[sources/sansiri-prd]] | [[sources/yc-combinator-spitch]] | [[sources/multi-modal-house-price-prediction]] | [[sources/probabilistic-disaggregation-property-value]] | [[sources/gcn-floor-plan-valuation]] | [[sources/visual-modalities-missing-data]] | [[sources/self-supervised-vit-valuation]] | [[sources/thailand-satellite-valuation]] | [[sources/building-condition-patch-convnet]] | [[sources/sub-city-price-index-forecasting]] | [[sources/rotterdam-spatial-analysis]] | [[sources/ensemble-decision-real-estate-images]] | [[sources/online-advertising-spatial-interactions]] | [[sources/digital-twins-tourism-heritage]] | [[sources/asean-real-estate-2026-investor-map]] | [[sources/nationthailand-thai-property-developers-ltr-visas]] | [[sources/c9-sessions-phuket-property-maintenance-fees]]

### ObsiVault Sources (21)
**Articles (7):** [[sources/obsivault-articles-chatgpt]] | [[sources/obsivault-articles-dj-set]] | [[sources/obsivault-articles-music-set-tools-and-tracks-grok]] | [[sources/obsivault-articles-philo-art-book-propaganda]] | [[sources/obsivault-articles-roadmap-2026]] | [[sources/obsivault-articles-techno-mix-bangkok-underground-adaptation-grok-1]] | [[sources/obsivault-articles-techno-mix-bangkok-underground-adaptation-grok]]

**Notes (14):** [[sources/obsivault-notes-2023-investment-thesis-deeptech-and-crypto]] | [[sources/obsivault-notes-asint-leveraging-the-criminal-mindset-for-intelligence]] | [[sources/obsivault-notes-concept-tokenized-vacation-properties]] | [[sources/obsivault-notes-crypto-bull-run-predictions-btc-eth-sol]] | [[sources/obsivault-notes-knowledge-management-evolution-beyond-para]] | [[sources/obsivault-notes-osint-detecting-social-media-astroturfing-and-bots]] | [[sources/obsivault-notes-osint-obsidian-semantic-understanding-and-nlp]] | [[sources/obsivault-notes-osint-test-note]] | [[sources/obsivault-notes-opsec-criminal-safety-advice-for-civilians]] | [[sources/obsivault-notes-psychology-study-guides]] | [[sources/obsivault-notes-social-network-analysis-overview]] | [[sources/obsivault-notes-social-network-analysis-with-python]] | [[sources/obsivault-notes-solana-token-analysis-model]] | [[sources/obsivault-notes-web3-marketing-agency-notes]]

### Gemini-Obsidian (7)
[[sources/gemini-2025-01-01-system-update]] | [[sources/gemini-2025-01-01-system-update-v2]] | [[sources/gemini-project-blueprint-context]] | [[sources/gemini-project-blueprint]] | [[sources/gemini-shared-memory]] | [[sources/gemini-reboot-obsidian]] | [[sources/gemini-daily-2025-01-01]]

### OSINT MOCs (5)
[[sources/real-estate-proptech-moc]] | [[sources/ai-ml-data-science-moc]] | [[sources/blockchain-crypto-moc]] | [[sources/cybersecurity-osint-moc]] | [[sources/thailand-luxury-real-estate-2025]]

### Deeptech Patterns (18)
[[sources/deeptech-elicitation]] | [[sources/deeptech-analysis-synthesis-creativity]] | [[sources/deeptech-analyze-claims]] | [[sources/deeptech-analyze-debate]] | [[sources/deeptech-analyze-malware]] | [[sources/deeptech-analyze-military-strategy]] | [[sources/deeptech-analyze-paper]] | [[sources/deeptech-analyze-patent]] | [[sources/deeptech-analyze-personality]] | [[sources/deeptech-analyze-prose]] | [[sources/deeptech-analyze-threat-report]] | [[sources/deeptech-analyze-answers]] | [[sources/deeptech-analyze-incident]] | [[sources/deeptech-analyze-logs]] | [[sources/deeptech-analyze-risk]] | [[sources/deeptech-analyze-cfp-submission]] | [[sources/deeptech-create-micro-summary]] | [[sources/deeptech-ask-secure-by-design-questions]]

---

## Raw Vaults (Transit)

Les fichiers raw sont en transit vers sources/. Voir [[sources/index]] pour le catalogue complet.

Voir [[log]] pour l'historique complet.
