---
created: 2026-05-14
updated: 2026-05-14
tags: [source, project, roadmap, reflexion, recall, patrimonasia]
sources: [raw/✅ ROADMAP 2026.md]
---

## ROADMAP 2026 — Strategic Planning for REcall Ecosystem

**Source:** ChatGPT conversation
**Date:** 2025-12-25

### Core Strategic Direction

REcall Agency = tech core building
reflexion.asia = Thailand property showcase + AI agent
patrimonasia.com = B2B European investor bridge

All powered by REcall Agency.

---

### Technical Architecture

#### Stack (Confirmed)
- **Frontend:** Next.js + TailwindCSS + shadcn/ui
- **Backend:** Supabase (PostgreSQL), Qdrant (vectors), Neo4j (graphs), Redis
- **AI:** OpenRouter + Ollama (local for sensitive data)
- **Orchestration:** n8n, LangGraph/Flowise
- **Data Pipeline:** Crawl4AI + Pydantic
- **3D:** Unreal Engine 5 + Cesium

#### Hosting
- Hostinger for WordPress (current)
- Migrate to Next.js progressively
- Vercel for frontend deployment
- Cut Amazon dependency by end of 2025

---

### Branding & Visual Identity

#### REcall Agency
- **Colors:** Noir / graphite / bleu électrique
- **Style:** Minimalisme Apple, micro-interactions futuristes
- **Message:** "AI-Driven Real Estate Pipeline"

#### Reflexion.asia
- **Colors:** Blanc / sable / bleu océan
- **Style:** Luxe moderne, photos haut de gamme
- **Message:** "Découvrir mes opportunités personnalisées"

#### Patrimonasia
- **Colors:** Bleu nuit / or discret
- **Style:** Sérieux, institutionnel (HSBC Private Banking + Knight Frank reference)

---

### UE5 / 360 Strategy

**Decision:** Start simple with Camera360 + basic montage, subcontract UE5 work

#### Pipeline:
1. Capture 360 video (5K or 8K)
2. Gaussian splatting reconstruction
3. UE5 scene integration (floor, skybox, light)
4. Web export (WebGL or video interactive)
5. 10-15 sec teaser for social networks

#### Budget:
- 300-600€ per project ( subcontracted )
- Sell at cost for first 3 POC to build portfolio
- Then scale to 900-1500€/project

#### Vendor Strategy:
- Find local Thailand videast with UE5 skills
- Use "genius editor" for post-production
- Fast validation of price

---

### Reflexion.asia — "Palantir for Real Estate Thailand"

#### Vision
Build an AI expert agent that:
- Knows Thailand A to Z
- Queries vectorized DB + SQL + graph
- Finds best opportunities from Thai portals
- Provides intelligent onboarding (magic link)
- Dashboard with 3D feature mapping
- Data-lens for alternative view on rental

#### Technical Layer
- **Data:** Scraping Thai portals (FazWaz, DDproperty, Hipflat, ThaiProperty)
- **Storage:** PostgreSQL (structured), Qdrant (vectors), Neo4j (graphs)
- **Agent:** RAG on multi-DB, explicable answers with confidence scores
- **Onboarding:** 5-question quiz → investor fingerprint → magic link

#### Features
1. Intelligent search + AI advisory
2. Property scoring (Reflexion Score 0-100)
3. Heatmaps + 3D maps (Three.js / Mapbox)
4. ROI comparator (rental, Airbnb, long-term)
5. Automated alerts (price drops, new listings)
6. Digital twins (UE5 light integration)

---

### Monthly Roadmap 2026

| Month | Focus | Key Deliverables |
|-------|-------|------------------|
| **Jan** | Launch | 2 paid projects, 10 EU leads, 1 drone partnership |
| **Feb** | Automation | IoT demo, 1 digital twin delivered, 50 reflexion.asia leads |
| **Mar** | Cybersecurity | 3 audits sold, 1 recurring contract |
| **Apr** | EU Expansion | 25 active apporteurs, 100 EU leads, 3 sales |
| **May** | Digital Twin Premium | 5 digital twins sold, 1 VR interactive project |
| **Jun** | Consolidation | Documentation, QA, 95% satisfaction |
| **Jul** | Thailand Scaling | 10 agency partners, 50 digitized properties |
| **Aug** | System Automation | 30% tasks automated, 2 big B2B accounts |
| **Sep** | AI Predictive | REcall Predict launch, 100 tool users |
| **Oct** | Premium | Ticket increase +35% |
| **Nov** | International | Vietnam, Indonesia, Cambodia expansion |
| **Dec** | Evaluation | REcall OS platform launch, 500K€ revenue target |

---

### Financial Estimates

| Site | Development Cost |
|------|-----------------|
| REcall Agency (Next.js) | 2,700-4,700€ |
| Reflexion.asia (Next.js + Strapi) | 3,000-5,000€ |
| Patrimonasia (Astro) | 700-1,300€ |
| **Total** | **6,400-11,000€** |

---

### Obsidian Integration

Setup Copilot plugin with 4 specialized agents:
1. Strategic Operator (business/priorities)
2. Technical Architect (pipelines, dev, security)
3. Brand Director (identity, UX)
4. Execution Assistant (micro-tasks)

---

## Sources

- [[raw/✅ ROADMAP 2026]]
- [[raw/Project_Blueprint]]
- [[concepts/recall-os]]