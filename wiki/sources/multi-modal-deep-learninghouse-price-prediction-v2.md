---
created: 2026-04-05
updated: 2026-04-21
tags: [research, property-valuation, multi-modal, deep-learning, house-price]
sources: [raw/multi-modal-deep-learninghouse-price-prediction.md]
---

## Résumé

Hasan et al. (2024) approach multi-modal house price prediction by learning a joint embedding that combines raw attributes (house characteristics), text (listing descriptions), images (property photos), and geo-spatial data (neighborhood context). The joint embedding significantly outperforms single-modality models on price prediction accuracy.

## Points clés

- **Joint embedding** : Text + images + geo-spatial + attributes combined into a unified vector representation
- **Multi-modal superiority** : Significant accuracy gains over attribute-only or single-modality models
- **Real estate specific** : Applied to actual property listings, not synthetic data
- **Generalizable** : Framework applicable across markets (validated on Thai data in Palanthai context)

## Connexions

- [[concepts/property-valuation]] — core methodology for multi-modal valuation
- [[sources/multi-modal-house-price-prediction]] — already ingested; this is the same paper under different filename
- [[sources/visual-modalities-missing-data]] — handles missing modalities in the multi-modal pipeline
- [[sources/self-supervised-vit-valuation]] — self-supervised pre-training reduces labeled data dependency
