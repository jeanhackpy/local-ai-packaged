# Wiki Log

> Historique chronologique du wiki. Append-only.

```bash
# Dernières 5 entrées
grep "^## \[" wiki/log.md | tail -5

# Stats
grep -c "^## \[" wiki/log.md
```

---

## [2026-04-05] setup | Initialisation du wiki

**Type** : setup

**Actions** :
- Structure créée : raw/, wiki/, wiki/concepts/, wiki/entities/, wiki/sources/, wiki/synthesis/
- 51 fichiers déplacés vers raw/
- WIKI_SCHEMA.md créé
- wiki/index.md + wiki/log.md créés

---

## [2026-04-05] ingest-batch-1 | 3 sources initiales

**Sources** : NVIDIA DSX, Deloitte, FazWaz

---

## [2026-04-05] ingest-batch-2 | 17 sources

**Sources NVIDIA** : Virtual assistant, Healthcare agents, Retail blueprints, Voice agent, Security, Streaming RAG, Catalog enrichment

**Sources RAG** : Cyborg, RAG+Reranker, AI observability, AI orchestration, Transcripts

**Sources Thailand** : DealSniper, Extracteur, Ontologie, Palanthai, Sansiri, YC SPITCH, Trust

---

## [2026-04-05] ingest-batch-3 | 15 sources

**Research** : Multi-modal, GCN, ViT, Satellite Thailand, Building condition, Price forecasting, Rotterdam, Ensemble

**Divers** : Architecture of Trust, Service quality, Data pipeline, Neuro-symbolic, Digital twins, Custom instructions

---

## [2026-04-05] concepts | 6 concepts créés

- agentic-ai, rag, data-flywheel, digital-twins
- property-valuation, computer-vision, immobilier-thailand, trust

---

## [2026-04-21] merge-consolidation | Merged Clippings + WIKI, restructured, created syntheses

**Type** : restructure

**Actions** :
- Restructured WIKI/ to match Clippings WIKI_SCHEMA.md
- Created WIKI/raw/ (65 raw sources moved from WIKI/sources/)
- Created WIKI/synthesis/ with 2 cross-source analyses
- Created WIKI/WIKI_SCHEMA.md (copied from Clippings/)
- Created WIKI/overview.md (thesis and research axes)
- Added 6 new concepts: voice-ai, security, urban-analysis, vlm, knowledge-extraction, data-pipeline
- Updated WIKI/index.md with full catalogue

**Stats post-merge** :
- **raw/** : 65 sources
- **sources/** : 0 summaries (in progress)
- **concepts/** : 14 (8 original + 6 new)
- **entities/** : 2
- **synthesis/** : 2 (ai-factory-for-real-estate, thailand-property-intelligence)

---

## [2026-04-21] ingest-full | 57 sources summaries ingested

**Type** : ingest

**Actions** :
- 22 NVIDIA blueprint source summaries created in sources/
- 33 Thailand/AI-ML/Research source summaries created in sources/
- 2 new source summaries: dubai-satellite-news-price-forecasting, multi-modal-deep-learninghouse-price-prediction-v2

**Stats**:
- **Sources ingérées** : 57/65 (all distinct content covered — remaining 8 raw files are duplicates with different filenames)
- **Concepts** : 8
- **Entities** : 2

---

---

## [2026-05-14] mega-consolidation | 4 vaults merged into SystemMac/WIKI

**Type**: restructure

**Source vaults**:
- ObsiVault (365 files → consolidated)
- Gemini-obsidian (Project Blueprint, daily logs)
- OSINT (Real Estate, AI/ML, Blockchain, Cybersecurity areas)
- DEEPTECH (structure intact)

**Actions**:
- Created `raw/obsivault/` (7 articles, real-estate/ai-ml/blockchain-crypto/osint-security sources)
- Created `raw/gemini-obsidian/` (Project_Blueprint.md, daily interactions, 000_Blackboard.md)
- Created `raw/osint/` (areas: Real Estate, AI/ML, Blockchain, Cybersecurity + clippings)
- Merged all into `raw/` at root level

**Stats post-consolidation**:
- **raw/** : 89 sources (69 original + 20 from external vaults)
- **sources/** : 61 summaries
- **New content**: Gemini Project Blueprint, ObsiVault clippings, OSINT areas

---

## [2026-05-14] ingest-batch | ASEAN 2026 + 2 Thailand sources

**Type** : ingest

**Sources** :
1. ASEAN Real Estate 2026: Investor Map (Younis Hijazi) — yields, tier framework, Thailand data
2. Nation Thailand — Thai developers bundle LTR visas with condos (Sansiri >6.4B target)
3. C9 Sessions Phuket — Maintenance fees & sinking funds (CBRE Thailand)

**Actions** :
- Created `raw/asean-real-estate-2026-investor-map.md` + `sources/`
- Created `raw/nationthailand-thai-property-developers-ltr-visas.md` + `sources/`
- Created `raw/c9-sessions-phuket-property-maintenance-fees.md` + `sources/`
- Updated `concepts/immobilier-thailand.md` — LTR visa, Phuket fees, ASEAN context
- Updated `index.md` — Thailand (20→22 sources), stats (69 raw, 61 sources)

**Stats**:
- **raw/** : 67 → 69 sources
- **sources/** : 59 → 61 source summaries
- **Concepts updated** : immobilier-thailand (LTR visa strategy, Phuket property management)

---

## [2026-05-14] lint | Wiki health check — fixed broken links + added sources

**Type** : lint

**Issues found**:
1. **Broken links (2)**: `AI-observability` → removed, `AI-factory` → `synthesis/ai-factory-for-real-estate`
2. **Missing Sources (5)**: computer-vision, data-flywheel, immobilier-thailand, property-valuation, trust
3. **Orphan sources (15)**: c9-sessions, nationthailand, s2vec, yc-combinator-spitch, etc.

**Actions**:
- Fixed `data-flywheel.md`: replaced `[[concepts/AI-observability]]` → `[[sources/ai-observability-data-flywheel-weights-biases]]`, added Sources frontmatter
- Fixed `digital-twins.md`: replaced `[[concepts/AI-factory]]` → `[[synthesis/ai-factory-for-real-estate]]`, added Sources frontmatter
- Added Sources frontmatter: agentic-ai, computer-vision, data-pipeline, digital-twins, property-valuation, rag, security, trust, urban-analysis, voix-ai
- Added source links to concepts: immobilier-thailand, agentic-ai, property-valuation, urban-analysis
- Fixed rag.md Connexions: replaced `knowledge-graph` → `data-pipeline`

**Stats**:
- **Concepts updated**: 10 concepts now have Sources frontmatter
- **Broken links fixed**: 2
- **Orphan sources reduced**: 15 → 7 (c9-sessions, nationthailand, dubai, multi-modal-v2, nvidia-ai-blueprints, retail-catalog-enrichment, zero-shot)

---

## [2026-05-14] ingest | ASEAN Real Estate 2026 Investor Map

**Type** : ingest

**Source** : ASEAN Real Estate 2026: Investor Map — Younis Hijazi, PhD

**Actions** :
- Created `raw/asean-real-estate-2026-investor-map.md` — full source
- Created `sources/asean-real-estate-2026-investor-map.md` — structured summary
- Updated `concepts/immobilier-thailand.md` — added ASEAN investment context, updated sources
- Updated `index.md` — Thailand section (19→20 sources), stats (67 raw, 59 sources)

**Stats**:
- **raw/** : 66 → 67 sources
- **sources/** : 58 → 59 source summaries
- **Concepts updated** : immobilier-thailand (ASEAN yields, LTR Visa, Phuket 8-15%)

---

## [2026-05-14] ingest-gemini-osint | Source summaries for consolidated vaults

**Type** : ingest

**Sources** :
1. project-blueprint-recall-os.md — REcall OS full spec (already exists)
2. gemini-blackboard.md — 000_Blackboard summary (project analysis, vault org)
3. roadmap-2026.md — 12-month strategic roadmap with tech stack, branding, financial estimates
4. thailand-luxury-real-estate-2025.md — Thailand luxury market analysis
5. daily-interactions-2025-07-03.md — Early collaboration log from gemini-obsidian
6. real-estate-proptech-moc.md — OSINT Real Estate master index
7. ai-ml-data-science-moc.md — OSINT AI/ML master index
8. blockchain-crypto-moc.md — OSINT Blockchain master index
9. cybersecurity-osint-moc.md — OSINT Cybersecurity master index

**Actions** :
- Created 8 new source summaries for consolidated files
- MOCs provide index structure for OSINT areas
- Roadmap connects to recall-os concept

**Stats**:
- **raw/** : 89 sources
- **sources/** : 59 → 67 source summaries (+8)
- **Concepts**: recall-os already created, linking to new sources

**Next Steps** (from mega-consolidation):
1. [x] Create source summaries for ObsiVault real-estate files (see roadmap-2026)
2. [x] Create source summaries for Gemini project files (gemini-blackboard, daily-interactions)
3. [x] Update concept links across new sources (recall-os, security, immobilier-thailand, agentic-ai)
4. [ ] Create additional synthesis pages for cross-vault insights
5. [ ] Archive original 4 vaults (keep raw, mark as consolidated)

---

## [2026-05-14] ingest-complete | Full vault ingestion complete

**Type** : ingest

**Summary:**
- **ObsiVault**: 22 source summaries (7 articles + 15 notes)
- **Gemini-obsidian**: 7 source summaries (root files + daily interactions)
- **OSINT MOCs**: 5 source summaries (already created in previous batch)
- **Deeptech Patterns**: 18 source summaries

**Total sources**: 61 → 117 source summaries (+56)

**Actions:**
- Created 56 new source summaries for consolidated vault content
- Updated sources/index.md with vault organization
- Updated index.md with source catalog by vault

**Next Steps (from mega-consolidation) - ALL COMPLETE:**
1. [x] Create source summaries for ObsiVault real-estate files
2. [x] Create source summaries for Gemini project files
3. [x] Update concept links across new sources
4. [x] Create additional synthesis pages for cross-vault insights
5. [x] Archive original 4 vaults (raw files preserved, marked as consolidated)

**Type** : verify

**Verified migrations**:
- **ObsiVault** : 7 articles + 15 notes = 22 files copied
  - articles: ChatGPT, DJ set, Music Set Tools, Philo Art Book, Techno Mix (x2), ROADMAP 2026
  - notes: 2023 Investment Thesis, ASINT, Concept Tokenized, Crypto Bull Run, Knowledge Management, OSINT Detecting Astroturfing, OSINT Obsidian NLP, OSINT Test, OpSec Criminal Safety, Psychology Study Guides, Social Network Analysis (x2), Solana Token Analysis, Web3 Marketing Agency
- **Gemini-obsidian** : 8 files (Project_Blueprint, 000_Blackboard, GEMINI, daily_interactions x2, system updates x2, reboot)
- **OSINT** : Full area structure (Real Estate, AI_ML_DataScience, Blockchain, Cybersecurity, Business, etc.)
- **DEEPTECH** : General, ai-ml-deeptech, blockchain-crypto, business-amazon, osint-security, patterns

**Actions**:
- Updated index.md with complete vault structure
- Reorganized external vaults section by source vault
- Updated stats: 100+ raw sources, 4 external vaults merged

**Stats**:
- **raw/** : 89 → 100+ sources
- **External vaults**: 4 (ObsiVault, Gemini-obsidian, OSINT, DEEPTECH)
- **Index updated**: vault structure, file listings, stats
