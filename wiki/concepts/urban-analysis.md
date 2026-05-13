---
created: 2026-04-21
updated: 2026-05-14
tags: [concept, urban-analysis, spatial-analysis, GIS, real-estate]
sources: [raw/rotterdam-spatial-analysis.md, raw/sub-city-price-index-forecasting.md, raw/online-advertising-spatial-interactions.md, raw/s2vec-google-built-environment.md]
---

## Urban Analysis

Spatial analysis techniques applied to property markets: street-level conditions, sub-city price indices, and spatial spillovers in real estate valuation.

### Street-Level Conditions

Utility-based spatial analysis framework applied to residential street-level conditions (Rotterdam case study). Captures micro-location factors that affect property value: street quality, amenities, walkability, noise.

### Sub-City Price Indexing

Weekly price index forecasting at sub-city granularity using:
- **Satellite radar imagery** — physical changes to neighborhoods over time
- **News sentiment** — media attention as a leading indicator of price movements
- Combines remote sensing + NLP for granular, frequent price signals

### Spatial Interactions in Advertising

Game-theoretic model of online advertising with spatial externalities. In property: a listing's price and quality affect neighboring properties' valuations (positive: amenities; negative: shadow, traffic).

### S2Vec — Built Environment Embeddings

Google Research (2025) foundation model for geospatial prediction from map data:
- **Masked autoencoding** sur environnement bâti (buildings, roads, parks, businesses)
- **No labels** — modèle apprend la grammaire spatiale des villes auto
- **Zero-shot extrapolation** — best performer sur prediction socio-économique pour regions unseen
- **Fusion with satellite** — S2Vec + RS-MaMMUT = outperforms all single-modality approaches

Architecture Earth AI: PDFM (population) + RS-MaMMUT (satellite) + S2Vec (built environment). Map data > satellite: faster updates, lower cost, finer resolution. Satellite sees rooftops; S2Vec knows 3 cafes, pharmacy, bus stop underneath.

## Sources

- [[sources/rotterdam-spatial-analysis]]
- [[sources/s2vec-google-built-environment]] (S2Vec: map-based zero-shot prediction)
- [[sources/sub-city-price-index-forecasting]]
- [[sources/online-advertising-spatial-interactions]]

## Connexions

- [[concepts/property-valuation]] — spatial features as inputs to valuation models
- [[concepts/immobilier-thailand]] — applies to Bangkok condo micro-markets
- [[concepts/computer-vision]] — satellite imagery analysis
