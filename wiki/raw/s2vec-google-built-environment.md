---
created: 2026-05-14
tags: [google, research, geospatial, AI, built-environment, self-supervised, embedding]
source: https://arxiv.org/abs/2505.00000 (Earth AI initiative)
---

# S2Vec — Google Research

## Source Document

S2Vec est un modèle de base publiés par Google Research (mai 2025) dans le cadre de l'initiative Earth AI. Il prédit des caractéristiques socio-économiques d'un quartier (revenu médian, densité de population, émissions de carbone) en analysant l'environnement bâti via des données cartographiques, sans aucun label humain.

## Key Concepts Extracted

- [[Self-supervised learning]] sur environnement bâti
- [[Masked autoencoding]] pour apprendre la grammaire spatiale des villes
- [[Zero-shot geographic extrapolation]]
- [[Multi-modal fusion]] (S2Vec + satellite imagery)
- [[Foundation models]] pour géospatial (PDFM, RS-MaMMUT, S2Vec)
- [[Urban analysis]] sans labels
- [[Embedding-based prediction]] transfer across tasks

## Architecture

### Input
- Map features: bâtiments, routes, parks, businesses → convertis en image pixel
- 3 cafes + 1 park dans une grille → valeurs de pixels
- Training data: map data, NOT satellite pixels

### Training Method
- Masked autoencoding: montrer un patch de ville avec des chunks manquants → modèle apprend à compléter
- Exemple: high-rises + subway station → prédit grocery store
- Millions de fois à travers le globe → apprend la "deep spatial grammar" des villes
- Aucun label humain ("financial district", "suburban residential")

### Output
- Embedding: string de nombres = empreinte mathématique pour toute localisation sur Terre
- Feed into prediction task → estimate population density, median income, carbon emissions

## Results

| Benchmark | Performance |
|-----------|-------------|
| Zero-shot geographic extrapolation | Meilleur modèle individuel |
| RS-MaMMUT (satellite baseline) | Matched or beat |
| GEOCLIP | Outperformed sur prédiction socio-économique |
| S2Vec + satellite embeddings | Best overall (fusion) |
| Built environment alone | Insufficient pour environnement (vegetation, terrain, transport) |

## Earth AI Pipeline

3 foundation models en parallèle:
1. **PDFM** — population dynamics
2. **RS-MaMMUT** — satellite imagery
3. **S2Vec** — built environment

Stack them → système qui lit un quartier comme un local.

## Implications

### Why map > satellite
- Updates faster
- Lower cost to process
- Covers built infrastructure at resolution satellite can't match
- Satellite sees rooftops; S2Vec knows 3 cafes, pharmacy, bus stop underneath

### For Palanthai / Thai real estate
- Map data could supplement satellite valuation
- Zero-shot transfer → pas besoin de labels thaï pour chaque problème
- Foundation model approach replaces hand-crafted indicators
- Fusion avec `thailand-satellite-valuation.md` research

## Related Sources

- [[sources/architecture-of-trust-real-estate]] (trust, uncertainty)
- [[sources/multi-modal-house-price-prediction]] (multi-modal fusion)
- [[sources/sub-city-price-index-forecasting]] (spatial prediction)
- [[concepts/urban-analysis]] (grille d'analyse urbain sans labels)
- [[concepts/vlm]] (self-supervised, masked autoencoding technique)
- [[synthesis/thailand-property-intelligence]] (Phase 3 includes satellite, could extend to map fusion)