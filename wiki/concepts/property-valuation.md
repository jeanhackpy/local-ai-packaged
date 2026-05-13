---
created: 2026-04-05
updated: 2026-05-14
tags: [concept, property-valuation, computer-vision, deep-learning]
sources: [raw/multi-modal-house-price-prediction.md, raw/gcn-floor-plan-valuation.md, raw/self-supervised-vit-valuation.md, raw/thailand-satellite-valuation.md, raw/building-condition-patch-convnet.md, raw/probabilistic-disaggregation-property-value.md, raw/sub-city-price-index-forecasting.md]
---

## Property Valuation

Estimation de valeur immobilière avec AI/ML.

### Modalités visuelles

| Modalité | Architecture | Use case |
|----------|--------------|----------|
| Photos intérieur | CNN, ViT | Condition, style |
| Satellite/aerial | CNN | Localisation, voisinage |
| Floor plans | GCN | Layout, surface |
| Street view | CNN | Façade, rue |

### Architectures

- **CNN** : ConvNets pour images (ResNet, EfficientNet)
- **ViT** : Vision Transformers (self-supervised)
- **GCN** : Graph Convolutional Networks (floor plans)
- **Siamese networks** : Similarity learning
- **Multi-modal fusion** : Combiner plusieurs inputs

### Methods

- Hedonic pricing models
- AVM (Automated Valuation Models)
- Comparable sales analysis
- Probabilistic disaggregation

### Sources

- [[sources/multi-modal-house-price-prediction]]
- [[sources/gcn-floor-plan-valuation]]
- [[sources/self-supervised-vit-valuation]]
- [[sources/thailand-satellite-valuation]]
- [[sources/building-condition-patch-convnet]]
- [[sources/probabilistic-disaggregation-property-value]]
- [[sources/sub-city-price-index-forecasting]]
- [[sources/zero-shot-neuro-symbolic-architecture]] (GPT-4 zero-shot floor plan generation)

## Connexions

- [[concepts/computer-vision]]
- [[concepts/immobilier-thailand]]
