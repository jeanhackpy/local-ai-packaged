---
created: 2026-04-05
updated: 2026-04-21
tags: [research, property-valuation, price-forecasting, satellite, sentiment-analysis, dubai]
sources: [raw/sub-city-real-estate-price-index-forecasting-at-weekly-horizons.md]
---

## Résumé

Arat et al. (2026) forecast sub-city property price indices at weekly frequency by combining Sentinel-1 satellite radar with news sentiment. Using 350k+ Dubai Land Department transactions (2015–2025), they construct weekly indices for 19 sub-city regions and show that multimodal models reduce forecast error by 35% at 26–34 week horizons.

## Points clés

- **Horizon-dependent** : Up to 10 weeks, price history alone suffices. Beyond 14 weeks, satellite SAR and news sentiment become critical
- **35% error reduction** : MAE drops from 4.48 to 2.93 at 26–34 week horizons with full multimodal model
- **Nonparametric > deep learning** : In this data regime (350k transactions, weekly granularity), nonparametric learners consistently outperform deep architectures
- **3 data sources** : Regional transaction history + Sentinel-1 SAR backscatter + news sentiment (lexical + embeddings)

## Connexions

- [[concepts/property-valuation]] — direct application to Thai sub-city price indexing
- [[concepts/urban-analysis]] — sub-city spatial granularity
- [[sources/thailand-satellite-valuation]] — satellite imagery for property valuation (different methodology)
