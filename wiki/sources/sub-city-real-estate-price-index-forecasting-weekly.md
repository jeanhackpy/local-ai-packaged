---
created: 2026-05-14
updated: 2026-05-14
tags: [real-estate, price-forecasting, satellite-imagery, SAR, sentiment-analysis, multimodal, Dubai]
sources: [raw/Sub-City-Real-Estate-Price-Index-Forecasting-at-Weekly-Horizons.md]
author: Baris Arat, Hasan Fehmi Ates, Emre Sefer
---

# Sub-City Real Estate Price Index Forecasting

## Summary

ArXiv paper (2602.18572) examining whether sub-city price indices can be forecasted at weekly frequency by combining satellite radar (SAR) with news sentiment. Uses 350,000+ Dubai Land Department transactions (2015-2025) to construct weekly indices for 19 sub-city regions.

## Key Concepts

- **Satellite radar (SAR)** as physical development signal
- **News sentiment** lexical tone + semantic embeddings
- **Weekly forecasting** horizon 2-34 weeks
- **Horizon-dependent results**: price history up to 10 weeks, SAR+sentinel beyond 14 weeks
- **35% MAE reduction** at 26-34 week horizons with multimodal approach
- Nonparametric learners outperform deep architectures in this regime

## Connections

- [[concepts/property-valuation]] — Price index methodologies
- [[concepts/remote-sensing]] — Satellite imagery for real estate
- [[concepts/sentiment-analysis]] — Market sentiment extraction
- [[concepts/time-series-forecasting]] — Temporal prediction models