# Clippings Wiki

> Base de connaissances personnelles sur l'immobilier thaïlandais et l'AI/ML appliquée.
> Basé sur le [LLM Wiki pattern](https://gist.github.com/karpathy/442a6bf555914893e9891c11519de94f) de Andrej Karpathy.

## Stats

- **raw/** : 51 sources originales
- **wiki/sources/** : 43 sources ingérées
- **wiki/concepts/** : 8 concepts
- **wiki/entities/** : 2 entities

---

## Architecture 3 couches

```
Clippings/
├── raw/                    # Sources immuables (articles, papers)
├── wiki/                   # Wiki structuré (LLM-generated)
│   ├── index.md           # Catalogue
│   ├── log.md            # Historique
│   ├── overview.md       # Vue d'ensemble
│   ├── sources/           # Résumés des sources
│   ├── concepts/          # Pages concepts
│   ├── entities/          # Pages entities
│   └── synthesis/         # Analyses transversales
├── WIKI_SCHEMA.md         # Schema pour le LLM agent
└── README.md              # Ce fichier
```

---

## Workflow

### 1. Ingest (ajouter une source)

1. Ajouter le fichier dans `raw/`
2. Dire au LLM : "Ingest raw/[fichier].md selon WIKI_SCHEMA.md"
3. Le LLM va :
   - Créer `wiki/sources/[slug].md`
   - Mettre à jour les pages entities/concepts pertinentes
   - Ajouter entrée dans `wiki/log.md`
   - Mettre à jour `wiki/index.md`

### 2. Query (poser une question)

1. Dire au LLM : "Réponds à ma question en utilisant le wiki"
2. Le LLM lit `wiki/index.md` → pages pertinentes
3. Synthétise avec citations `[[page]]`
4. Si la réponse est précieuse → créer `wiki/synthesis/[slug].md`

### 3. Lint (health check)

Périodiquement : "Lint le wiki selon WIKI_SCHEMA.md"

Vérifie :
- Contradictions entre pages
- Claims dépassés
- Pages orphelines (aucun lien)
- Concepts sans page dédiée
- Cross-references manquantes

---

## Conventions

### Nommage
- Fichiers en kebab-case
- Liens en `[[wiki/file-name]]` (Obsidian)

### Frontmatter (obligatoire)
```yaml
---
created: 2026-04-05
updated: 2026-04-05
tags: [concept, AI]
sources: [raw/filename.md]
---
```

### Structure d'une page source
```markdown
## Résumé
[2-3 phrases]

## Points clés
- ...

## Connexions
- [[entities/...]]
- [[concepts/...]]
```

---

## Commandes utiles

```bash
# Stats
ls raw/ | wc -l
ls wiki/sources/ | wc -l

# Dernières entrées log
grep "^## \[" wiki/log.md | tail -5

# Toutes les sources
ls wiki/sources/

# Tous les concepts
ls wiki/concepts/
```

---

## Thèmes couverts

### Immobilier Thailand
- [[concepts/immobilier-thailand]]
- [[concepts/property-valuation]]
- [[entities/fazwaz]]

### AI/ML
- [[concepts/agentic-ai]]
- [[concepts/rag]]
- [[concepts/data-flywheel]]
- [[concepts/computer-vision]]

### Divers
- [[concepts/trust]]
- [[concepts/digital-twins]]

---

## Pour commencer

1. Ouvre Obsidian sur ce vault
2. Ouvre Claude Code sur le même dossier
3. Dis : "Ingest les sources restantes et construis le wiki selon WIKI_SCHEMA.md"
