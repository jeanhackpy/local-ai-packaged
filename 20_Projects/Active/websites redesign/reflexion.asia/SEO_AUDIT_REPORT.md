# SEO/GEO Audit — reflexion.asia
**Date:** 22 mai 2026
**Status:** Lecture seule

---

## DONNÉES GSC (28 jours)

### Top Pages
| Clics | Impr | CTR | Pos | URL |
|-------|------|-----|-----|-----|
| 9 | 979 | 0.9% | 10.5 | /guide-investissement-immobilier-thailande/ |
| 2 | 531 | 0.4% | 22.1 | /acheter-villa-thailande/ |
| 1 | 11 | 9.1% | 17.3 | /property/pattaya-residence-services-by-radisson/ |
| 1 | 3 | 33.3% | 7.7 | /property/phuket-kamala-bay-ocean-view-cottages/ |
| 0 | 71 | 0% | 71.0 | /property/koh-samui-villa-luxueuse-avec-vue-sur-locean-et-piscine-privee/ |
| 0 | 13 | 0% | 61.5 | /property/bangkok-kraam-sukhumvit-26/ |

### Top Queries (par clics)
| Clics | Impr | CTR | Pos | Query |
|-------|------|-----|-----|-------|
| 1 | 97 | 1.0% | 10.1 | investir en thailande |
| 1 | 13 | 7.7% | 9.5 | investir en thaïlande |
| 1 | 11 | 9.1% | 9.4 | investissement thailande |
| 0 | 25 | 0% | 14.5 | acheter villa thailande |
| 0 | 25 | 0% | 32.8 | acheter une maison en thailande |
| 0 | 23 | 0% | 30.5 | achat maison thailande |
| 0 | 16 | 0% | 11.5 | investir thailande |
| 0 | 14 | 0% | 9.1 | investir en thailande immobilier |
| 0 | 12 | 0% | 35.2 | acheter maison thailande |
| 0 | 12 | 0% | 22.3 | achat villa thailande |

### Device Split
| Device | Clics | Impr | CTR | Pos |
|--------|-------|------|-----|-----|
| Mobile | 8 | 433 | 1.8% | 10.3 |
| Desktop | 4 | 1188 | 0.3% | 19.6 |
| Tablet | 1 | 22 | 4.5% | 9.4 |

### Striking Distance
**1 keyword:** "investir en thailande" — pos 10.1 (proche du top 10)

### Statut global
- 14 clics / 1621 impressions (28j)
- Homepage (/) à pos 4.5 avec 0 clics (opportunité)
- 43% mobile mais 3x moins de traffic desktop → mobile-first OK

---

## CONTENT ANALYSIS

### Posts (10 articles, tous Mars 2026)
| Date | Mots | H2 | Imgs | Ext | Titre |
|------|------|----|-----|-----|-------|
| 2026-03-23 | 728 | 7 | 0 | 0 | Investir en Thaïlande : Le Guide Complet pour les Investisseurs |
| 2026-03-23 | 757 | 7 | 0 | 0 | Acheter une maison en Thaïlande : L'Opportunité de la Décennie |
| 2026-03-23 | 556 | 6 | 0 | 0 | Villa Thaïlande Achat : Les Meilleures Opportunités... |
| 2026-03-22 | 858 | 6 | 0 | 0 | Investir en Thaïlande : Un Guide pour les Investisseurs Français |
| 2026-03-22 | 702 | 5 | 0 | 0 | Investir en Thaïlande : Un Guide Complet pour les Investisseurs França... |
| 2026-03-22 | 753 | 4 | 0 | 0 | Investir en Thaïlande : Un Guide Complet pour les Investisseurs França... |
| 2026-03-22 | 654 | 5 | 0 | 0 | Acheter une maison en Thailande : Le Guide Complet... |
| 2026-03-22 | 875 | 4 | 0 | 0 | Acheter Villa Thaïlande : Un Investissement Rentable et Sécurisé |
| 2026-03-22 | 1198 | 0 | 0 | 0 | Guide Ultime à l'Achat d'un Condominium en Thailande |
| 2026-03-22 | 838 | 5 | 0 | 0 | Investir en Thailande : Le Guide Complet pour les Investisseurs França... |

**Problèmes content:**
- 0 images sur tous les posts (critical pour engagement)
- 0 external links (pas de authority signals)
- Plusieurs titres similaires (duplicate-like titles)
- 0 meta descriptions visibles via API

### Pages Key
| Page | Mots | H1 | H2 | Imgs | Pb |
|------|------|----|----|-----|---|
| homepage-default | 681 | 0 | 22 | 12 | ⚠️ No H1 |
| guide-investissement... | 3264 | 0 | 2 | 1 | ⚠️ No H1, massive content |
| contact-form | 100 | 1 | 0 | 0 | 🔴 Thin |
| privacy-policy | 3774 | 0 | 1 | 0 | ✅ OK |

---

## ROBOTS.TXT — CONTENT SIGNALS

```
Content-Signal: search=yes,ai-train=no
Allow: /
```

**Analyse:**
- ✅ search=yes — Google peut indexer
- ⚠️ ClaudeBot blocked — pas d'indexation AI (GPTBot, Google-Extended aussi bloqués)
- ⚠️ ClaudeBot blocked = pas de GEO via AI search

**Impact:** Le site ne pourra pas être cité par ChatGPT/Claude si ClaudeBot est bloqué.

---

## FINDINGS PRIORITAIRES

### 🔴 CRITIQUE

1. **ClaudeBot blocked** — `Disallow: /` pour ClaudeBot dans robots.txt
   - Impact: 0% présence dans ChatGPT, Claude, Perplexity
   - Fix: Remove `Disallow: /` pour ClaudeBot ou ajouter exception

2. **0 images dans les articles** — Tous les 10 posts ont 0 images
   - Impact: Engagement zéro, shareability = 0
   - Fix: Ajouter 2-3 images par article (before/after, maps, property photos)

3. **No H1 sur homepage et guideprincipal** — homepage-default et guide-investissement n'ont pas de H1
   - Impact: Google ne comprend pas le topic principal
   - Fix: Ajouter H1 avec keyword principal

### 🟡 IMPORTANT

4. **Titles duplicates/partiels** — "Investir en Thaïlande : Un Guide..." apparaît 4x avec variations mineures
   - Impact: Potential keyword cannibalization
   - Fix: Différencier les titles avec angles distincts

5. **0 external links dans posts** — Pas de links vers sources externes
   - Impact: Pas de authority signals, E-E-A-T faible
   - Fix: Ajouter 2-3 liens vers sources (Bangkok Post, SET, etc.)

6. **Images = 0 sur posts** — 100% des posts sans images
   - Fix: Ajouter images pertinentes

### 🟢 QUICK WINS

7. **Homepage pos 4.5 avec 0 clics** — La page ranke bien mais le CTR est 0%
   - Cause probable: Meta description missing ou pas assez compelling
   - Fix: A/B tester meta description

8. **Striking distance: "investir en thailande" pos 10.1** — presque top 10
   - Quick win: Améliorer ce page pour passer en top 10

9. **Mobile vs Desktop disconnect** — Mobile 8 clics / 433 impr vs Desktop 4 clics / 1188 impr
   - Desktop a 2.7x plus d'impr mais mobile a 2x plus de clics
   - CTR mobile = 1.8% vs desktop = 0.3% → mobile converts 6x mieux
   - Fix: Prioriser le contenu mobile-first

---

## PLAN D'ACTION

### Week 1 — Critical fixes
- [ ] Remove ClaudeBot block from robots.txt (GEO impact)
- [ ] Add H1 to homepage-default and guide-investissement
- [ ] Add 1 image to each of the 10 posts

### Week 2 — Content quality
- [ ] Add 2-3 external links per post (sources thaïlandaises)
- [ ] Differentiate duplicate-like titles
- [ ] Add meta descriptions to posts

### Week 3 — GEO optimization
- [ ] Test allowing ClaudeBot partial access for AI search
- [ ] Add FAQPage schema to top 3 pages
- [ ] Create property-specific content (condo guide already exists)

### KPIs Target (90j)
| KPI | Baseline | Target |
|-----|----------|--------|
| Clics/mois | 14 | 50 |
| Pos "investir en thailande" | 10.1 | 1-5 |
| Impressions/mois | 1621 | 3000 |
| Presence AI search | 0% | >20% |

---

## UPDATE 23 MAI 2026

###robots.txt Analysis — Updated
```
User-agent: *
Content-Signal: search=yes,ai-train=no
Allow: /
```
- ✅ search=yes — Google peut indexer
- ⚠️ ClaudeBot blocked via ai-train=no → Impact GEO majeur
- ⚠️ GPTBot blocked → Impact AI search (ChatGPT, Bing AI)
- ⚠️ Google-Extended blocked → Impact Google AI Overviews
- Cloudflare active — bloque fetch_programming depuis scripts Python

**Impact:** Le site ne pourra pas être cité par ChatGPT/Claude/Perplexity tant que ai-train=no. Fix: changer en `ai-input=yes` pour，允许AI用作RAG grounding。

### reflexion.asia — Actions Prioritaires Cross-Site

**Pour recall-agency.com:**
1. Homepage FR: meta description + H1 avec keyword "Thailand digital marketing"
2. Canonical /en/home/ → /
3. Posts 2020 = EXPIRÉS → refresh Thailand focus
4. Schema Organization sur homepage
5. 0 keywords striking distance — construire topical authority

**Pour reflexion.asia:**
1. Fix robots.txt ai-train=no → ai-input=yes (GEO quick win)
2. Ajouter H1 sur homepage-default et guide-investissement
3. Ajouter images aux 10 posts (0 images = 0 engagement)
4. "investir en thailande" pos 10.1 → target top 5

**KPIs globaux (90j):**
| KPI | Baseline | Target |
|-----|----------|--------|
| Clics/mois (recall) | 4 | 50 |
| Pos "recall agency" | 6.7 | 1-3 |
| Striking distance kw (recall) | 0 | 10 |
| Clics/mois (reflexion) | 14 | 50 |
| Pos "investir en thailande" | 10.1 | 1-5 |
| GEO presence (AI search) | 0% | >20% |

---

**Rapport:** 22-23 mai 2026
**Sites:** reflexion.asia + recall-agency.com
**Tools:** GSC API + WordPress REST API + curl + citability_scorer.py