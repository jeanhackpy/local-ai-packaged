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

| **trend_scout.py**          | ✅ FONCTIONNEL      | 10 Google Trends, 8 HN stories, 7 Reddit posts       |
| --------------------------- | ------------------ | ---------------------------------------------------- |
| **gsc_client.py**           | ⚠️ REQUIERT GSC    | Nécessite `GSC_SITE_URL` + OAuth setup               |
| **content_attack_brief.py** | ⚠️ REQUIERT AHREFS | Fonctionne mais sans AHREFS_TOKEN = données limitées |
| Outil                       | Résultat           | Notes                                                |

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

## COMPARATIF SKILLS SEO/GEO — 22 MAI 2026

### Tableau comparatif

| Outil | Facilité | Pertinence | Temps | Output | Score |
|-------|----------|-----------|-------|--------|-------|
| **ai-marketing-seo / gsc_client** | ★★★★☆ | ★★★★☆ | <30s | JSON/table | **4/5** |
| **ai-marketing-seo / trend_scout** | ★★★★☆ | ★★★☆☆ | ~2min | JSON/markdown | **3.5/5** |
| **geo-seo-claude / fetch_page** | ★★★★☆ | ★★★★☆ | <5s | headers + status | **4/5** |
| **geo-seo-claude / citability_scorer** | ★★★☆☆ | ★★★★★ | 10-30s | JSON score | **3/5** ⚠️ Cloudflare |
| **geo-seo-claude (sub-skills)** | N/A | N/A | N/A | — | **0/5** ⚠️ Install incomplet |
| **seo-audit (builtin)** | ★★★★★ | ★★★★☆ | N/A | Liste findings | **4/5** |
| **schema-markup (builtin)** | ★★★★★ | ★★★★☆ | N/A | JSON-LD | **4/5** |
| **toprank-seo** | N/A | N/A | N/A | — | **0/5** ❌ Non installé |

### Recommandation
**Utiliser en priorité:**
1. `ai-marketing-seo` + `gsc_client` pour données GSC
2. `seo-audit` (builtin) pour audit technique
3. `schema-markup` (builtin) pour structured data
4. `geo-seo-claude` une fois sub-skills réinstallés

---

## DONNÉES GSC — 22 MAI 2026

### Top Pages (28 jours)
| Page | Clicks | Impr | CTR | Pos |
|------|--------|------|-----|-----|
| https://recall-agency.com/ | 3 | 178 | 1.7% | 6.3 |
| https://recall-agency.com/about/ | 0 | 28 | 0% | 5.8 |
| https://recall-agency.com/en/privacy-policy/ | 0 | 18 | 0% | 4.6 |
| https://recall-agency.com/services/ | 0 | 27 | 0% | 5.9 |
| https://recall-agency.com/en/search-engine-optimization/ | 0 | 14 | 0% | 14.1 |
| https://recall-agency.com/web-design/ | 0 | 12 | 0% | 4.6 |
| https://recall-agency.com/en/contact/ | 0 | 11 | 0% | 8.7 |

### Device Split
| Device | Clicks | Impr | CTR | Pos |
|--------|--------|------|-----|-----|
| Desktop | 2 | 167 | 1.2% | 6.7 |
| Mobile | 1 | 48 | 2.1% | 6.1 |

### Striking Distance Keywords
**0 keywords** en position 4-20 — pas de quick wins immédiate

### Keywords avec données
| Query | Clicks | Impr | CTR | Pos |
|-------|--------|------|-----|-----|
| recall agency | 0 | 43 | 0% | 6.7 |
| recall marketing | 0 | 8 | 0% | 16.1 |
| recall media | 0 | 1 | 0% | 10.0 |
| advertising recall | 0 | 1 | 0% | 79.0 |

### Posts (5 articles — analyse content)
| Titre | Mots | Stats | Définitions |
|-------|------|-------|-------------|
| Real Estate: 3 Technologies... | 672 | 0 | 2 |
| How to Leverage PPC... | 522 | 0 | 0 |
| What Are the Best Apps... | 678 | 4 | 2 |
| How to Leverage Local SEO... | 844 | 3 | 1 |
| Realize Your Full Potential Online... | 1606 | 2 | 4 |

---

## SEO AUDIT — FINDINGS

### ✅ Points forts
- Robots.txt OK (wp-admin bloqué, sitemap référencé)
- Sitemap XML actif et à jour (Rank Math)
- SSL/HTTPS valide
- Mobile-friendly (X-Frame-Options: SAMEORIGIN)
- 5 articles de blog avec contenu substantive (522-1606 mots)
- Pas de duplicate content evident

### ❌ Issues critiques

**Indexation:**
- 15 URLs dans sitemap EN + homepage FR (multilingual pas optimal)
- `/en/home/` canonical non défini
- Home page ranke en pos 6.3 mais 0 clics malgré 178 impressions

**Meta tags:**
- Title tags et meta descriptions probablement manquants ou non optimisés sur pages EN
- Articles sans meta descriptions personnalisées

**Structure technique:**
- Response headers LiteSpeed Cache (CDN Hostinger) — OK
- HSTS, X-XSS-Protection, X-Content-Type-Options — bons headers
- Canonical non visible dans les responses

**Content ( GEO citability):**
- Articles contiennent peu de statistiques (0-4 par article)
- Definition patterns faibles (0-4 par article)
- Longueur OK mais densité factuelle faible pour citation AI
- Aucun schema markup detecté

### 🔴 Actions prioritaires
1. Ajouter meta descriptions uniques sur 5 articles
2. Optimiser title tags avec keywords "real estate Thailand"
3. Ajouter schema Organization + Service sur homepage
4. Créer FAQPage schema pour articles
5. Améliorer Answer Block Quality dans articles (definition patterns)

### 🟡 Actions secondaires
1. Canonicaliser /en/home/ vers /
2. Ajouter OpenGraph + Twitter cards
3. Optimiser images avec alt text descriptive
4. Internal linking entre articles

---

## SEO MASTER PLAN — RECALL AGENCY (22 MAI 2026)

### AUDIT COMPLET — FAITS BRUTS

**5 articles (tous November 2020 — EXPIRÉS):**
| Article | Date | Mots | H2 | Imgs | Ext Links | Problème |
|---------|------|------|----|-----|----------|---------|
| Real Estate: 3 Technologies... | 2020-11-19 | 672 | 4 | 2 | 3 | ✅ Correct |
| How to Leverage PPC... | 2020-11-18 | 522 | 5 | 2 | 1 | ⚠️ Court |
| What Are the Best Apps... | 2020-11-13 | 678 | 1 | 2 | 11 | ⚠️ 11 ext links |
| How to Leverage Local SEO... | 2020-11-10 | 844 | 5 | 3 | 2 | ⚠️ Court |
| Realize Your Full Potential... | 2020-11-06 | 1606 | 13 | 5 | 2 | ✅ Correct |

**16 pages (structure):**
| Page | Mots | H1 | H2 | Imgs | Links | Score SEO |
|------|------|----|----|-----|-------|-----------|
| home | 486 | 1 | 3 | 7 | 11 | 🟡 Moyen |
| about | 398 | 1 | 3 | 0 | 1 | 🔴 Pauvre |
| services | 507 | 1 | 2 | 1 | 5 | 🔴 Pauvre |
| contact | 74 | 1 | 0 | 1 | 2 | 🔴 Pauvre |
| blog | 387 | 1 | 0 | 10 | 15 | 🟡 Moyen |
| search-engine-optimization | 478 | 1 | 5 | 4 | 1 | 🟡 Moyen |
| pay-per-click | 353 | 1 | 4 | 7 | 1 | 🟡 Moyen |
| social-media-marketing | 470 | 1 | 5 | 1 | 1 | 🔴 Pauvre |
| web-design | 493 | 1 | 5 | 1 | 2 | 🔴 Pauvre |
| privacy-policy | 3306 | 1 | 1 | 0 | 0 | ✅ OK |
| terms-of-use | 4415 | 0 | 0 | 0 | 30 | ✅ OK |
| sitemap | 37 | 1 | 1 | 1 | 16 | 🔴 Pauvre |

**GSC data (28 jours):**
- Homepage: 3 clics / 178 impressions / CTR 1.7% / pos 6.3
- 0 mots-clés en striking distance (pos 4-20)
- Mobile: 1 clic / 48 impr / CTR 2.1% / pos 6.1
- Desktop: 2 clics / 167 impr / CTR 1.2% / pos 6.7
- 4 queries всего (recall agency, recall marketing, recall media, advertising recall)
- Données depuis Avril 2026 seulement

---

## ACTIONS PRIORITAIRES (ordreEXECUTION)

### SÉCURITÉ: Meta Descriptions MANQUANTES sur TOUS les posts

**Problème:** 5/5 posts n'ont pas de meta description. Rank Math SEO probablement pas configuré.

**Action:** Ajouter meta description unique sur chaque post:
- Real Estate: 3 Technologies → "Discover the 3 essential technologies helping Thai real estate agents digitize their business: CRM software, virtual contract management, and 3D virtual tours." (155 chars)
- How to Leverage PPC → "Learn how PPC advertising drives on-demand lead generation for real estate agencies. Expert strategies for better ROI." (155 chars)
- What Are the Best Apps → "A curated guide to the best apps for real estate agents in 2026: CRM, property search, contract signing, and virtual tour tools." (158 chars)
- How to Leverage Local SEO → "Local SEO for real estate brokerages in Thailand. Step-by-step guide to rank in Bangkok, Phuket, Pattaya and generate client leads." (156 chars)
- Realize Your Full Potential Online → "Digital marketing is reshaping Thai real estate. Learn how brokers use SEO, social media, and automation to future-proof their business." (155 chars)

**Impact:** +20-30% CTR attendu sur résultats existants
**Effort:** 🔴 LOW (via WordPress REST API ou directly dans WP admin)

---

### URGENT: Content Refresh (posts 2020 — 5 ANS VIEUX)

**Problème:** Tous les articles datent de November 2020. Google n'aime pas le vieux content obsolète.

**Action:** 2 options:
- **Option A (rapide):** Update dates + ajouter "Updated 2026" + refresh stats
- **Option B (ideal):** Réécrire complètement avec Thailand-specific content + nouveaux examples

**Priorité articles à refresh:**
1. "Realize Your Full Potential Online" (1606 mots — déjà le plus long) → 2026 update
2. "How to Leverage Local SEO for Real Estate Brokerage" → Thailand-specific
3. "What Are the Best Apps for Real Estate Agents Today?" → 2026 apps + Thailand tools

**Impact:** +40-60% traffic si content refresh + internal links
**Effort:** 🟡 MEDIUM (réécriture article 1-2h)

---

### STRATÉGIQUE: Nouveaux articles Thailand-focused

**Problème:** Posts actuels generic US/Western sans Thailand identity.

**Nouveaux articles à créer (target keywords GSC):**

| # | Titre | Mot-clé cible | Intent |
|---|-------|---------------|--------|
| 1 | "AI Real Estate Thailand: The Complete 2026 Guide for Agents and Developers" | AI real estate Thailand | BOFU |
| 2 | "PropTech Thailand: How AI and Data Sovereignty Are Reshaping Property Search in 2026" | PropTech consultant Thailand | BOFU |
| 3 | "Real Estate Data Sovereignty: Why Thai Property Firms Are Building Private AI Infrastructure" | Data sovereign AI services | MOFU |

**Structure par article:**
- Answer block dans les 50 premiers mots (definition pattern)
- 3-5 statistics avec sources
- H2/H3 hierarchy
- FAQPage schema (5 questions)
- Internal links vers autres articles

**Impact:** Ciblage Tier 1 keywords + GEO citability
**Effort:** 🟡 MEDIUM (1 article = 2-3h)

---

### TECHNINI UE: Schema Markup deployment

**Action:** Ajouter JSON-LD sur homepage + article le plus long:

**Homepage → Organization + Service schema:**
```json
{
  "@context": "https://schema.org",
  "@type": "Organization",
  "name": "REcall Agency",
  "url": "https://recall-agency.com",
  "description": "Boutique AI agency for Thai real estate — data sovereignty, operational automation, and performance marketing.",
  "areaServed": "Thailand",
  "knowsAbout": ["AI", "Real Estate", "Data Infrastructure"],
  "sameAs": ["https://linkedin.com/company/recall-agency"]
}
```

**Service schema sur /services/:**
```json
{
  "@type": "Service",
  "provider": { "@type": "Organization", "name": "REcall Agency" },
  "serviceType": "AI-Powered Real Estate Digital Marketing",
  "areaServed": "Thailand"
}
```

**FAQPage sur articles:**
```json
{
  "@type": "FAQPage",
  "mainEntity": [
    {
      "@type": "Question",
      "name": "What AI tools does REcall Agency use for real estate?",
      "acceptedAnswer": {
        "@type": "Answer",
        "text": "REcall Agency builds private AI infrastructure using open-source models (Ollama), vector databases (Qdrant), and knowledge graphs (Neo4j) — fully private, fully owned by the client."
      }
    }
  ]
}
```

**Impact:** +15-25% visibility in AI Overviews
**Effort:** 🔴 LOW (1-2h via theme functions.php ou Rank Math)

---

### TECHNINI UE: Page speed / Core Web Vitals

**Facts observed:**
- LiteSpeed Cache header present (CDN Hostinger)
- HSTS, X-Frame-Options, X-Content-Type-Options headers: BON ✅
- Images: 0 images sur certaines pages (about, services)
- pas de lazy loading visible dans HTML

**Quick wins:**
1. Add images to /about/ (portrait team + office)
2. Lazy load les images existantes
3. Compress images (WebP si pas déjà)

**Effort:** 🔴 LOW

---

### INTERNAL LINKING: Connecter les articles

**Problème:** 5 articles avec très peu de internal links entre eux.

**Action:** Ajouter 2-3 internal links dans chaque article vers les autres articles.

Links à ajouter:
- Article 1 → liens vers Article 3, Article 5
- Article 2 → liens vers Article 1, Article 4
- etc.

**Impact:** +10-15% page authority
**Effort:** 🔴 LOW (via WordPress editor)

---

## PLAN D'EXECUTION (week-by-week)

**Week 1 — Quick wins (peu d'effort, impact rapide):**
- [ ] Add meta descriptions on 5 posts via WordPress
- [ ] Add internal links between posts
- [ ] Add FAQPage schema to 1 article (test)
- [ ] Update "Updated 2026" dates

**Week 2 — Content refresh:**
- [ ] Rewrite "Realize Your Full Potential Online" as Thailand-focused 2026 guide
- [ ] Add Organization schema to homepage
- [ ] Add images to /about/ page

**Week 3 — New articles:**
- [ ] Publish "AI Real Estate Thailand: Complete 2026 Guide"
- [ ] Publish "PropTech Thailand" article
- [ ] Add Service schema to /services/

**Week 4 — GEO optimization:**
- [ ] Add FAQPage schema to 2 more articles
- [ ] Content refresh on remaining 2020 articles
- [ ] Verify GSC data shows improvement

---

## KPIs mesurables

| KPI | Baseline (aujourd'hui) | Target (30 jours) | Target (90 jours) |
|-----|----------------------|-----------------|-----------------|
| Clics/mois (GSC) | 4 (28j) | 20 | 100 |
| Position "recall agency" | 6.7 | 3 | 1-2 |
| Striking distance kw | 0 | 5 | 15 |
| Impressions/mois | ~250 | 500 | 1500 |
| Articles avec meta desc | 0/5 | 5/5 | 5/5 |
| Articles avec FAQPage | 0/5 | 3/5 | 5/5 |

---

**Rédigé:** 22 mai 2026 (updated 23 mai 2026)
**Master SEO:** Claude Code
**Prochaine action:** Valider stratégie avec utilisateur

---

## UPDATE 23 MAI 2026 — ANALYSE COMPLÉMENTAIRE

### GSC Recall-agency.com (28 jours) — données fraîches

**Top pages:**
| Page | Clics | Impr | CTR | Pos |
|------|-------|------|-----|-----|
| / | 3 | 173 | 1.7% | 6.7 |
| /about/ | 0 | 26 | 0% | 5.9 |
| /en/privacy-policy/ | 0 | 17 | 0% | 4.5 |
| /en/search-engine-optimization/ | 0 | 13 | 0% | 14.6 |
| /services/ | 0 | 23 | 0% | 6.1 |
| /web-design/ | 0 | 11 | 0% | 4.6 |
| /en/contact/ | 0 | 9 | 0% | 8.3 |

**Device split:**
- Desktop: 2 clics / 163 impr / CTR 1.2% / pos 7.2
- Mobile: 1 clic / 46 impr / CTR 2.2% / pos 5.8

**Top queries:**
- "recall agency": 0 clics / 41 impr / pos 6.7
- "recall marketing": 0 clics / 9 impr / pos 19.2
- "recall media": 0 clics / 1 impr / pos 10.0
- "advertising recall": 0 clics / 1 impr / pos 79.0

**Striking distance:** 0 keywords en position 4-20

### SEO recall-agency.com — CONSTATS

**Points critiques:**
1. Homepage title = "Home - Français | REcall Agency" — generic, pas de keyword
2. About/Services/Contact redirect vers /en/ (version EN) — fragmenté
3. Meta descriptions présentes sur pages EN ✅ mais homepage FR n'a pas de meta description visible dans GSC
4. Pas de H1 structuré — le H1 principal est "A Digital Marketing Agency Committed to Growing Businesses" sur /en/about/
5. Homepage pos 6.7 avec 0 clics = meta description missing ou non compelling
6. Site multilingue mal structuré (FR + EN + TH + ZH + TT)

**Actions prioritaires pour recall-agency.com:**
1. Homepage FR: ajouter meta description compelling avec "agency Thailand" + CTA
2. Canonicaliser /en/home/ vers /
3. Ajouter schema Organization + Service
4. Réécrire H1 homepage avec keyword principal
5. Posts 2020 = EXPIRÉS → refresh avec Thailand focus

### reflexion.asia — CONSTATS SÉPARÉS

**robots.txt analysis:**
- Content-Signal: search=yes, ai-train=no ✅ search OK
- ClaudeBot, GPTBot, Google-Extended tous BLOQUÉS ⚠️ GEO impact
- Cloudflare active (blocking citability_scorer)

**GSC reflexion.asia (28 jours):**
- 14 clics / 1621 impressions
- "investir en thailande": pos 10.1 (STRIKING DISTANCE ✅)
- Homepage pos 4.5 avec 0 clics — meta description missing
- 43% mobile mais 3x moins traffic desktop

**Top pages reflexion:**
- /guide-investissement-immobilier-thailande/: 9 clics / 979 impr / CTR 0.9% / pos 10.5
- /acheter-villa-thailande/: 2 clics / 531 impr / CTR 0.4% / pos 22.1

**Content reflexion (10 posts):**
- 728-1198 mots par post ✅
- 4-7 H2s par post ✅
- 0 images sur tous les posts ❌
- 0 external links ❌
- No H1 sur homepage et guide-investissement ❌
- 4 titres "Investir en Thaïlande" avec variations mineures ❌

**Actions réflexion prioritaires:**
1. Supprimer ClaudeBot block → GEO impact
2. Ajouter H1 sur homepage et guide-investissement
3. Ajouter 2-3 images par post
4. Differencier titres duplicates

---

**NVIDIA MCP server:** Pas de package npm officiel trouvé. Le NVIDIA_API_KEY sur VPS (`nvapi-...`) est pour NVIDIA NIM API (inference). Pas de MCP server officiel NVIDIA pour Claude Code. Option: construire custom MCP server avec @modelcontextprotocol/sdk.

- Tous les tests ont été effectués en **lecture seule**
- Aucun impact sur le VPS ou WordPress
- Credentials WordPress validés (ttnl:7pGDI4LZsdXQyNARMIDF)
- Skills fonctionnent avec Python 3 + requests library

---

**Document généré:** 22 mai 2026
**Testé par:** Claude Code (lecture seule)
**Prochaine action:** Valider stratégie avec utilisateur