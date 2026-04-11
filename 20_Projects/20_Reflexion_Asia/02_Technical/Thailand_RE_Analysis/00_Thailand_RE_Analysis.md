---
tags: [palanthai, proptech, thailand, real-estate, analysis, fazwaz, data]
created: 2026-03-26
status: active
type: analysis
---

# 🏙️ Thailand Real Estate Analysis — FazWaz Dataset

> **Source**: FazWaz scraped data · 18,113 listings · March 2026  
> **Purpose**: Identify visa-eligible developer projects for BD outreach + luxury segment scoring for client pitching

---

## 📊 Dataset Overview

| File | Listings | Portfolio Value | Purpose |
|------|----------|----------------|---------|
| Developer freehold 3M+ THB | 838 | ฿12.4B | BD contact list, visa pathway |
| Agent/Owner freehold 3M+ THB | 5,722 | ฿74.5B | Market baseline, resale comparison |
| Luxury 10M+ THB | 5,567 | ฿240B | HNW client matching, luxury scoring |
| Rental 80K+/mo | 6,986 | — | Visa rental pathway |

---

## 🏗️ Developer Ranking — Top 10 BD Targets

| Rank | Project | Province | Units | Portfolio | Avg Price | ROI | Score |
|------|---------|----------|-------|-----------|-----------|-----|-------|
| 1 | Mulberry Grove The Forestias | Samut Prakan | 6 | ฿1,079.7M | ฿179.95M | — | 77.3 |
| 2 | The Residences 38 | Bangkok | 4 | ฿412.6M | ฿103.16M | 5.0% | 40.3 |
| 3 | Layan Verde | Phuket | 5 | ฿144.1M | ฿28.81M | — | 32.7 |
| 4 | InterContinental Residences Asoke | Bangkok | 3 | ฿318.0M | ฿106.0M | — | 31.9 |
| 5 | Grand Solaire Noble | Pattaya | 5 | ฿101.4M | ฿20.29M | — | 30.8 |
| 6 | SCOPE Thonglor | Bangkok | 1 | ฿244.0M | ฿244.0M | — | 29.3 |
| 7 | Cleat Condominium | Krabi | 5 | ฿35.0M | ฿7.0M | — | 27.8 |
| 8 | The River by Raimon Land | Bangkok | 2 | ฿284.2M | ฿142.1M | 4.0% | 27.1 |
| 9 | Marina Living Condo | Phuket | 3 | ฿37.0M | ฿12.33M | **17.0%** | 26.8 |
| 10 | Wan Vayla Na Chaophraya | Bangkok | 4 | ฿109.7M | ฿27.43M | — | 25.6 |

→ Full list: [[Data/developer_contact_list.csv]]

---

## 🗺️ Province BD Priority Matrix

| Province | Projects | Units | Portfolio | Avg Score | Top Project |
|----------|----------|-------|-----------|-----------|-------------|
| **Bangkok** | 247 | 383 | ฿6.3B | 7.4 | The Residences 38 |
| **Phuket** | 120 | 240 | ฿2.9B | 10.4 | Layan Verde |
| **Chon Buri** (Pattaya) | 62 | 114 | ฿1.2B | 9.0 | Grand Solaire Noble |
| Samut Prakan | 8 | 17 | ฿1.2B | **15.9** | Mulberry Grove |
| Krabi | 3 | 9 | ฿64.8M | **15.5** | Cleat Condominium |
| Chiang Mai | 22 | 32 | ฿275.5M | 6.1 | Hillside Plaza |

---

## 🟢 Visa Eligibility — ฿3M Threshold

```
฿3M–5M   : 231 units (27.6%) ← Entry level
฿5M–8M   : 221 units (26.4%)
฿8M–12M  : 148 units (17.7%)
฿12M–20M : 107 units (12.8%)
฿20M+    : 131 units (15.6%)
```

**Key insight**: 54% of developer stock sits in the ฿3M–8M entry/mid band — perfect for UAE expat visa pitch

---

## 💎 Luxury Segment — Top 10 (10M+ THB)

| Rank | Project | Province | Type | Units | Avg Price | ROI | Score |
|------|---------|----------|------|-------|-----------|-----|-------|
| 1 | Laguna Park | Phuket | Villa/Town | 32 | ฿22.8M | 8.4% | 27.3 |
| 2 | Land and Houses Park | Phuket | House/Villa | 24 | ฿19.1M | 6.6% | 20.3 |
| 3 | Nantawan Rama 9 | Bangkok | House/Villa | 19 | ฿61.8M | 7.9% | 17.0 |
| 4 | The City Bangna | Samut Prakan | House | 19 | ฿25.9M | 8.4% | 16.8 |
| 5 | Botanica Foresta | Phuket | Villa | 16 | ฿47.5M | 8.8% | 14.6 |
| 6 | Botanica Modern Loft II | Phuket | Villa | 15 | ฿26.2M | **9.1%** | 13.7 |
| 7 | Centro Bangna | Samut Prakan | House | 13 | ฿16.6M | **9.2%** | 12.0 |
| 8 | Asherah Villas Phuket | Phuket | Villa | 12 | ฿28.3M | **10.9%** | 11.8 |
| 9 | Mooban Wangtan | Chiang Mai | Villa | 13 | ฿22.7M | 7.5% | 11.6 |
| 10 | Supalai Lake Ville | Phuket | House/Villa | 12 | ฿15.0M | **9.7%** | 11.3 |

---

## 📈 Key Cross-Dataset Findings

### Developer vs Agent Price Premium
| Province | Dev ฿/SqM | Agent ฿/SqM | Premium |
|----------|-----------|-------------|---------|
| Pathum Thani | ฿133,950 | ฿51,350 | **+161%** |
| Samut Prakan | ฿195,000 | ฿95,100 | **+105%** |
| Krabi | ฿101,000 | ฿51,200 | **+97%** |
| Bangkok | ฿173,000 | ฿152,000 | +13.8% |
| Phuket | ฿146,000 | ฿131,000 | +11.5% |

### ROI by Province (Developer)
- 🥇 **Phuket**: 9.0% median → Top pitch for income investors
- 🥈 Chon Buri / Prachuap KK: 6.0%
- Bangkok: 5.0% (volume market, stable)

---

## 🔄 Flywheel Content Angles

1. **"Bangkok #1 for Thailand LTR Visa"** → Infographic + Lead Magnet (UAE expats)
2. **"Developer Premium +161%"** → Blog FAQ (buyer education, differentiation)
3. **"Phuket 9% ROI champion"** → Email campaign (income investors)
4. **"฿3M Visa Guide"** → Landing page / gated PDF (high intent)
5. **"Phuket Luxury ฿240B market"** → Premium report (HNW/UHNW)
6. **"250 off-plan units"** → Newsletter (early investors)

---

## 📁 Files

- [[Thailand_PropTech_Dashboard.html]] — Interactive dashboard (6 tabs)
- [[Data/developer_contact_list.csv]] — 494 projects BD list
- [[Data/developer_ranking_full.csv]] — Full ranking with all metrics
- [[Data/province_bd_summary.csv]] — Province-level BD summary
- [[Script.py/thailand_real_estate_analysis.py]] — Full analysis pipeline

---

## 🤖 Developer Outreach Template

**Subject**: Data insight on [Project Name] + growth opportunity

> "Our analysis of 18,000+ Thailand listings identified **[Project]** as top [X]% performer in [Province] by business volume.  
> Key: [X] visa-eligible units · [ROI]% yield · [SqM] avg footprint.  
> We help developers capture UAE expat investors through AI-powered marketing — 20 min call?"

---

*Generated by Claude PM Assistant · FazWaz Analysis Pipeline · 2026-03-26*
