---
created: 2026-05-14
updated: 2026-05-14
tags: [google, research, geospatial, AI, built-environment, self-supervised, embedding]
sources: [raw/s2vec-google-built-environment.md]
---

## Résumé

S2Vec est un modèle de base Google Research (Earth AI) qui prédit des caractéristiques socio-économiques (revenu, densité, emissions) à partir de l'environnement bâti cartographique, sans labels humains. Utilise masked autoencoding pour apprendre la grammaire spatiale des villes.

## Points clés

- **Input**: Map features (bâtiments, routes, cafes, bus stops) → image pixel
- **Training**: Masked autoencoding — prédit les gaps dans les patches de ville
- **Output**: Embedding spatial = empreinte mathématique pour toute localisation
- **Zero-shot**: Meilleurs résultats sur extrapolation géographique vs satellites
- **Fusion**: S2Vec + satellite = outperforms toutes les modalités seules

## Architecture Earth AI

| Modèle | Focus |
|--------|-------|
| PDFM | Population dynamics |
| RS-MaMMUT | Satellite imagery |
| **S2Vec** | Built environment (map data) |

Map > Satellite: mise à jour plus rapide, coût inférieur, résolution plus fine.

## Connexions

- [[concepts/urban-analysis]] — grammaire spatiale sans labels
- [[concepts/vlm]] — masked autoencoding self-supervised
- [[concepts/property-valuation]] — prédiction revenus/housing
- [[synthesis/thailand-property-intelligence]] — fusion multi-modale (satellite + map)

## Implication pour Palanthai

1. Map data comme complément à satellite pour valuation thaïlandaise
2. Zero-shot transfer → pas besoin de labels pour chaque problème
3. Foundation model remplace hand-crafted indicators
4.潜在的: fusion S2Vec + RS-MaMMUT pour meilleure précision