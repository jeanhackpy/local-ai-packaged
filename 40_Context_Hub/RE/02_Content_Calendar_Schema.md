---
type: db_schema
source: notion
notion_id: 6d99c74ecd174c7fa3192b098913501b
notion_db_id: 087c0d63-8786-4650-a93f-c6ee76a82f04
synced: 2026-03-30
tags: [RE, content-calendar, schema, n8n]
---

# 📅 Content Calendar — Schéma & Références

> Base de données Notion centrale. Le pipeline n8n lit les entrées en statut **Brief** et génère le contenu.

## Schéma des Propriétés

| Champ | Type | Valeurs / Notes |
|---|---|---|
| Post Title | title | Titre de la publication |
| Brand | select | REcall Agency, REflexion Asia, PatrimoinAsia, JP Personal |
| Status | select | Brief → Draft → AI Generated → Approved → Scheduled → Published → Archived |
| Pillar | select | AI & PropTech, Behind the Build, Thailand Market, Data Sovereignty, Client Story, Listing |
| Platform | multi_select | LinkedIn, Instagram, Facebook, X/Twitter, Pinterest |
| Language | select | EN, FR, FR+EN |
| Publish Date | date | Date de publication prévue |
| Hook | text | Accroche principale du post |
| CTA | text | Call-to-action |
| Hashtags | text | Hashtags à utiliser |
| Content LinkedIn | text | Contenu adapté LinkedIn |
| Content Instagram | text | Contenu adapté Instagram |
| Content Facebook | text | Contenu adapté Facebook |
| Content X | text | Contenu adapté X/Twitter |
| n8n Run ID | text | ID d'exécution n8n (traçabilité) |
| Published At | date | Date réelle de publication |
| ID | auto_increment | Identifiant unique auto |

## Workflow Statuts

```
Brief → [n8n lit] → AI Generated → [Approval email] → Approved → Scheduled → Published
                                         ↓ (rejet)
                                       Brief (reset)
```

## IDs Notion Clés

```yaml
Content Hub Page:    333ebffa-e73e-816b-8293-d02bbea32e9d
Brand Assets Page:   333ebffa-e73e-81ff-98ba-e5a3a125ebe3
Content Calendar DB: 6d99c74ecd174c7fa3192b098913501b
Data Source ID:      087c0d63-8786-4650-a93f-c6ee76a82f04
```

## Liens Rapides

- [RE Content Hub Notion](https://www.notion.so/333ebffae73e816b8293d02bbea32e9d)
- [Content Calendar](https://www.notion.so/6d99c74ecd174c7fa3192b098913501b)
- [n8n Workflow](https://n8n.recall-agency.com)

---
*Dernière sync : 2026-03-30 | Source : Notion Content Calendar DB*
