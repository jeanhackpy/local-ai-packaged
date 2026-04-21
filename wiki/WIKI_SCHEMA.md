# WIKI_SCHEMA

> Schema pour le LLM agent qui maintient ce wiki. Basé sur le pattern LLM Wiki de Karpathy.

## Domaine

Ce wiki documente les recherches sur :
- **Immobilier Thailandais** : valorisation, tendances, agents, plateformes
- **AI/ML Applied** : blueprints NVIDIA, RAG, agents, data flywheels
- **Tech Stack** : architectures, outils, bonnes pratiques

## Architecture en 3 couches

1. **raw/** — Sources immuables (articles, papers, docs). Le LLM lit mais ne modifie jamais.
2. **wiki/** — Le wiki structuré généré et maintenu par le LLM.
3. **Ce fichier** — Le schema qui guide le comportement du LLM.

## Structure du wiki

```
wiki/
├── index.md           # Catalogue de tout le wiki
├── log.md             # Historique chronologique (ingests, queries, lints)
├── overview.md        # Vue d'ensemble / thesis évolutive
├── concepts/          # Pages concepts (RAG, data flywheel, agentic AI...)
├── entities/          # Pages entités (NVIDIA, FazWaz, Palanthai, Weights & Biases...)
├── sources/           # Résumés des sources ingérées
│   └── [source-slug].md
└── synthesis/         # Analyses transversales, comparaisons
```

## Conventions de nommage

- Fichiers en kebab-case : `real-estate-valuation.md`, `nvidia-blueprints.md`
- Liens en `[[wiki/file-name]]` (Obsidian)
- Frontmatter obligatoire :

```yaml
---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, AI, Thailand]
sources: []
---

## Résumé

[2-3 phrases max]

## Points clés

- ...

## Connexions

- [[entities/nvidia]]
- [[concepts/rag]]
```

## Workflows

### Ingest

1. Lire la source dans `raw/`
2. Créer `wiki/sources/[slug].md` avec résumé structuré
3. Identifier les entities → mettre à jour `wiki/entities/[entity].md`
4. Identifier les concepts → créer/mettre à jour `wiki/concepts/[concept].md`
5. Mettre à jour `wiki/index.md`
6. Ajouter entrée dans `wiki/log.md` :
   ```
   ## [2026-04-05] ingest | [Titre de la source]
   
   - **Fichier source** : `raw/[filename].md`
   - **Entities identifiées** : NVIDIA, FazWaz
   - **Concepts clés** : RAG, data flywheel
   - **Actions** : créé sources/..., mis à jour entities/...
   ```

### Query

1. Lire `wiki/index.md` pour identifier les pages pertinentes
2. Lire les pages concernées
3. Synthétiser une réponse avec citations `[[page]]`
4. Si la réponse est précieuse → créer une nouvelle page dans `wiki/synthesis/`

### Lint (hebdomadaire)

- Contradictions entre pages ?
- Claims dépassés par de nouvelles sources ?
- Pages orphelines (aucun lien entrant) ?
- Concepts mentionnés sans page dédiée ?
- Connexions manquantes ?

## Tips

- Ce wiki sert ton travail sur **Recall Agency**, **Reflexion Asia**, **Patrimonasia**
- Thailande = contexte géographique principal
- Toujours chercher les connexions inter-domaines (AI → immobilier)
