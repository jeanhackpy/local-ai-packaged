---
type: hub_index
source: notion
notion_id: 333ebffa-e73e-816b-8293-d02bbea32e9d
notion_url: https://www.notion.so/333ebffae73e816b8293d02bbea32e9d
synced: 2026-03-30
tags: [RE, content-hub, notion-sync]
---

# 🔴 RE Content Hub — Index

> Hub central de contenu pour l'écosystème RE. Source de vérité synchronisée depuis Notion.
> Pipeline n8n lit depuis Notion, génère, et publie après approbation.

## Structure

| Fichier | Contenu | Source Notion |
|---|---|---|
| [[01_Brand_Assets]] | Bios, taglines, brand voices x4 entités | Brand Assets page |
| [[02_Content_Calendar_Schema]] | Schéma BDD, statuts, propriétés | Content Calendar DB |
| [[03_Content_Posts]] | Posts actifs (Brief/Draft/Approved) | Content Calendar rows |

## 4 Entités du Système RE

| Entité | Langue | Plateforme principale | Statut |
|---|---|---|---|
| 🔴 REcall Agency | EN | LinkedIn, X | Actif |
| 🔵 REflexion Asia | FR+EN | Facebook, Instagram, LinkedIn | Actif |
| 🟣 PatrimoinAsia | FR | LinkedIn | Coming soon |
| 🟢 JP Personal Brand | EN | LinkedIn, X | Actif |

## Pipeline n8n

- **URL n8n:** https://n8n.recall-agency.com
- **Notion DB ID:** 6d99c74ecd174c7fa3192b098913501b
- **Workflow:** Social Media Multi-Brand (à créer)
- **Statut flow:** Brief → AI Generated → Approved → Scheduled → Published

## Notes Agent IA

- Lire [[01_Brand_Assets]] pour les brand voice prompts avant toute génération
- Le Content Calendar est la source de vérité des posts à produire
- Toujours respecter les règles de capitalisation RE (cf. Brand System Rules)
- Sync Notion → Obsidian : manuel pour l'instant (automatisation n8n prévue)

---
*Dernière sync : 2026-03-30 | Via : Claude Cowork Session*
