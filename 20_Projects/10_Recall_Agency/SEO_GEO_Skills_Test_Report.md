# SEO/GEO Skills Test Report — recall-agency.com
**Date:** 22 mai 2026
**Status:** Tests completed (lecture seule, aucun impact VPS)

---

## RESSOURCES ANALYSÉES

### 1. Brand Book & Documents Stratégiques

| Document | Path | Status |
|----------|------|--------|
| Brand Book v1 (Reflexion) | `/20_Projects/Active/websites redesign/reflexion.asia/brand-book-v1.md` | ✓ Lu |
| Business Concept Flywheel | `/20_Projects/Active/Business Concept Anti-fragile et Flywheel.md` | ✓ Lu |
| Stratégie Triptyque | `/20_Projects/Active/Stratégie framework — le triptyque REcall -Reflexion -Patrimonasia.md` | ✓ Lu |
| Articles Existants | `/recall-agency.com/code/src/lib/articles.ts` | ✓ Lu (5 articles) |

---

## SKILLS TESTÉS

### Skill 1: `ai-marketing-seo` (ai-marketing-skills/ericosiu)

**Contenu testé:** `content_attack_brief.py`, `gsc_client.py`, `trend_scout.py`

#### Résultats:

| Outil | Résultat | Notes |
|-------|----------|-------|
| **trend_scout.py** | ✅ FONCTIONNEL | 10 Google Trends, 8 HN stories, 7 Reddit posts |
| **gsc_client.py** | ⚠️ REQUIERT GSC | Nécessite `GSC_SITE_URL` + OAuth setup |
| **content_attack_brief.py** | ⚠️ REQUIERT AHREFS | Fonctionne mais sans AHREFS_TOKEN = données limitées |

**Scores:**
- Facilité d'utilisation: ★★★★☆ (4/5)
- Pertinence pour Recall: ★★★☆☆ (3/5) - orienté US/marketing general
- Temps requis: ~2 min pour trend_scout
- Output: JSON + markdown

**Limites detectées:**
- Géolocalisé US par défaut
- Nécessite credentials GSC pour full features
- Orientation marketing B2C plus que B2B/tech

---

### Skill 2: `toprank-seo` (nowork-studio/toprank)

**Installation détectée:** Non (copie incomplete)

**Problème:** Les fichiers `.md` de sous-dossiers (seo-analysis, geo-optimizer, etc.) n'ont pas été copiés correctement dans `~/.claude/skills/`

**Fichiers présents:**
- `toprank-seo/` (dossier vide ou incomplet)
- `toprank-google-ads/` (dossier présent)

**Action requise:** Réinstaller correctement avec la structure de sous-dossiers

---

### Skill 3: `schema-markup` (builtin)

**Droits disponibles:** Oui

**Usage:** Optimisation du schema markup pour AI search

---

### Skill 4: `seo-audit` (builtin)

**Droits disponibles:** Oui

**Usage:** Audit technique SEO

---

## ANALYSE WORDPRESS ACTUELLE

### Structure du site recall-agency.com

**Pages (16 total):**
| ID | Titre | Slug |
|----|----|------|
| 9 | Home (EN) | home |
| 25 | About | about |
| 26 | Services | services |
| 29 | Contact | contact |
| 647 | Blog | blog |
| 1461 | Search Engine Optimization | search-engine-optimization |
| 1468 | Pay Per Click | pay-per-click |
| 1649 | Social Media | social-media-marketing |
| 1655 | Web Design | web-design |
| 1854 | Sitemap | sitemap |
| 2954 | Privacy Policy | privacy-policy |
| 2964 | Terms of Use | terms-of-use |

**Posts (5 articles):**
1. "The Hidden Cost of Fragmented Property Data in Thailand"
2. "Real Estate Automation in Southeast Asia: What Operators Get Wrong"
3. "Semantic Search for Property: Beyond Keywords"
4. "Building a Market Knowledge Graph for Thai Real Estate"
5. "Why Real Estate Firms Should Think in Systems, Not Services"

**Media:** 10 images (uploads 2025/06)

---

## CONTENU EXISTANT — ANALYSE

### Forces du contenu actuel:
1. **Expertise technique démontrée** — Les articles montrent une connaissance profonde (data pipelines, knowledge graphs, semantic search)
2. **Cas d'usage concrets** — "44,988 properties indexed", "27 units/minute", "16,417 edges"
3. **Positionnement différenciant** — "Systems over services", "structural automation vs cosmetic"
4. **Vocabulary aligné avec brand** — "intelligence layer", "ontology", "data pipeline", "operational OS"

### Faiblesses du contenu actuel:
1. **Pas de focus géographique explicite** — Thailand/SEA mentionné mais pas structuré
2. **Pas de CTAs clairs** — Aucun call-to-action dans les articles
3. **Absence de schema markup** — Pas de Organization, Service, FAQPage
4. **Structure non optimisée pour SEO** — Meta descriptions, H1 multiples, internal linking

---

## STRATÉGIE SEO/GEO RECOMMANDÉE

### Positionnement Adapté

**De:** "AI Sovereignty Layer for Real Estate" (trop corporate)
**Vers:** "Boutique AI sur mesure pour l'immobilier Thailandais"

**Storytelling:**
> "Nous ne vendons pas de l'IA. Nous construisons des systèmes opérationnels qui donnent aux acteurs de l'immobilier thaïlandais le contrôle absolu sur leurs données — open-source, privés, pensés pour vous."

### Keywords Cibles

**Tier 1 - BOFU (High Intent):**
| Keyword | Volume | Difficulté | Priorité |
|---------|--------|------------|----------|
| AI real estate Thailand | ? | ? | ★★★★★ |
| PropTech consultant Thailand | ? | ? | ★★★★★ |
| Real estate AI infrastructure | ? | ? | ★★★★☆ |
| Data sovereign AI services | ? | ? | ★★★★☆ |

**Tier 2 - MOFU (Consideration):**
| Keyword | Volume | Difficulté | Priorité |
|---------|--------|------------|----------|
| AI integration real estate | ? | ? | ★★★☆☆ |
| Open source AI real estate | ? | ? | ★★★☆☆ |
| Privacy first AI solutions | ? | ? | ★★★☆☆ |

**Tier 3 - TOFU (Awareness):**
| Keyword | Volume | Difficulté | Priorité |
|---------|--------|------------|----------|
| Real estate digital transformation Thailand | ? | ? | ★★☆☆☆ |
| AI for property developers | ? | ? | ★★☆☆☆ |

### Content Flywheel

```
1 ARTICLE (1000-2000 mots)
│
├── LinkedIn (5 posts x 150 mots)
├── Twitter/X (10 tweets)
├── Newsletter (résumé 300 mots)
├── Carousels (3 x 5 slides)
├── Thread Quora/Reddit (1)
└── FAQ SEO (5 questions long-tail)
```

### GEO Strategy (AI Search)

**Cibles:** ChatGPT, Perplexity, Claude AI Overviews, Google AI Overviews

**Techniques:**
1. **Authoritative content** — Citations de sources, données précises, expertise démontrée
2. **Structured data** — Schema Organization, Service, FAQPage, Article
3. **Entity optimization** — Développeurs thaï, projets, zones géographiques
4. **Direct answers** — Paragraphes de 40-60 mots répondant aux questions directes

---

## RECOMMANDATIONS SKILLS

### Skills à utiliser:

| Skill | Usage | Priorité |
|-------|-------|----------|
| `ai-marketing-seo/trend_scout.py` | Détection trends hebdo | Haute |
| `seo-audit` | Audit technique initial | Haute |
| `schema-markup` | Ajout structured data | Haute |
| `ai-marketing-seo/content_attack_brief.py` | Après setup GSC | Moyenne |

### Skills à corriger/reinstaller:

| Skill | Action requise |
|-------|---------------|
| `toprank-seo` | Réinstaller correctement avec sous-dossiers |
| `toprank-google-ads` | Vérifier installation |

---

## PROCHAINES ÉTAPES

### Phase 1: Configuration (J1-J2)
- [ ] Configurer GSC_SITE_URL pour recall-agency.com
- [ ] Réinstaller top-rank-seo correctement
- [ ] Setup OAuth GSC

### Phase 2: Audit (J3-J5)
- [ ] Lancer `seo-audit` sur le site
- [ ] Analyser keywords avec `content_attack_brief.py`
- [ ] Identifier competitor gaps

### Phase 3: Optimisation (J6-J10)
- [ ] Ajouter schema markup (Organization + Service + FAQPage)
- [ ] Optimiser meta tags existants
- [ ] Créer nouveaux articles optimisés

### Phase 4: Publication (J11-J15)
- [ ] Implémenter content flywheel
- [ ] Publier sur LinkedIn/Twitter
- [ ] Monitorer trends avec trend_scout

---

## NOTES

- Tous les tests ont été effectués en **lecture seule**
- Aucun impact sur le VPS ou WordPress
- Credentials WordPress validés (ttnl:7pGDI4LZsdXQyNARMIDF)
- Skills fonctionnent avec Python 3 + requests library

---

**Document généré:** 22 mai 2026
**Testé par:** Claude Code (lecture seule)
**Prochaine action:** Valider stratégie avec utilisateur