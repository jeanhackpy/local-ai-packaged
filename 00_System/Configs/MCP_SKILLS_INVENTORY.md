# 🧰 INVENTAIRE DES MCP & SKILLS

Recensement de tous les serveurs MCP et Skills disponibles pour les agents IA.
*Dernière mise à jour : 2026-06-06*

---

## 🔌 MCP Locaux (claude_desktop_config.json)

Ces serveurs tournent en local via `npx` au démarrage de Claude Desktop.

| Serveur | Package | Auth | État |
| :--- | :--- | :--- | :--- |
| **cloudflare** | `@cloudflare/mcp-server-cloudflare` | Wrangler OAuth (`npx wrangler login`) | ✅ Actif |
| **google** | `ga4-mcp` | gcloud ADC — `palanthai_oauth_client.json` | ✅ Actif |
| **obsidian** | `@mauricio.wolff/mcp-obsidian` | Local filesystem | ✅ Actif |

### 🔧 Maintenance Auth

**Cloudflare** — token expire régulièrement :
```bash
npx wrangler login
npx @cloudflare/mcp-server-cloudflare init   # met à jour le session_id dans config.json
```

**Google (ga4-mcp)** — si scopes expirés ou "insufficient authentication scopes" :
```bash
gcloud auth application-default login \
  --client-id-file=$HOME/.config/gcloud/palanthai_oauth_client.json \
  --scopes="https://www.googleapis.com/auth/cloud-platform,https://www.googleapis.com/auth/analytics.readonly,https://www.googleapis.com/auth/analytics.edit,https://www.googleapis.com/auth/webmasters,https://www.googleapis.com/auth/indexing"
# puis redémarrer Claude Desktop
```

> ⚠️ Ne PAS utiliser `@googleworkspace/mcp-server-gsc` ou `@googleworkspace/mcp-server-ga4` — ces packages n'existent pas sur npm (404).

---

## 🌐 MCP Cowork (Plugins connectés)

### Data & Analytics
| Serveur | Capacités | Notes |
| :--- | :--- | :--- |
| **google** | GA4 reports, GSC analytics, URL inspection, Sitemaps, Indexing API | Voir propriétés ci-dessous |
| **ahrefs** | Site Explorer, Rank Tracker, Keywords Explorer, GSC, Brand Radar, Social | — |
| **similarweb** | Traffic intel, Lead enrichment, Competitor analysis | — |

### Infrastructure
| Serveur | Capacités |
| :--- | :--- |
| **cloudflare** (plugin) | Workers, KV, R2, D1, Durable Objects, Queues, AI inference, Cron, Zones |
| **supabase** | SQL, Migrations, Edge Functions, Branches, Logs |
| **n8n** | Workflows CRUD, Executions, Data Tables, Credentials |

### Productivity & Knowledge
| Serveur | Capacités |
| :--- | :--- |
| **obsidian** | Read/Write notes, Tags, Frontmatter, Search (vault : SystemMac) |
| **notion** | Pages, Databases, Views, Comments, Search |
| **airtable** | Bases, Tables, Records, Fields |

### Sales & Marketing
| Serveur | Capacités |
| :--- | :--- |
| **apollo** | Lead enrichment, Prospecting ICP, Sequences |
| **similarweb** | Web intelligence, Competitors |

### Engineering
| Serveur | Capacités |
| :--- | :--- |
| **github** | Repos, PRs, Issues, Code search |
| **linear** | Issues, Projects, Cycles |
| **asana** | Tasks, Projects |
| **pagerduty** | Incidents, On-call |
| **datadog** | Logs, Metrics, Monitors |

### Ops / Legal / Finance
| Serveur | Capacités |
| :--- | :--- |
| **slack** | Messages, Channels |
| **gmail** | Email read/search |
| **google-calendar** | Événements, Agenda |
| **box** | Files, Folders |
| **atlassian** | Jira, Confluence |
| **docusign** | Signatures électroniques |
| **ms365** | Office 365 |
| **bigquery** | SQL analytics |

### Product & Design
| Serveur | Capacités |
| :--- | :--- |
| **amplitude** | Product analytics |
| **figma** | Design files |
| **monday** | Project boards |
| **clickup** | Tasks |
| **pendo** | User onboarding |
| **fireflies** | Meeting transcripts |

---

## 📊 Propriétés GA4 & GSC

| Site | GSC | GA4 Property ID |
| :--- | :--- | :--- |
| recall-agency.com | `sc-domain:recall-agency.com` ✅ siteOwner | `250736461` |
| reflexion.asia | `sc-domain:reflexion.asia` ✅ siteOwner | `292681207` |
| reflexion-ai | — | `470602693` |
| patrimonasia.com | — | *(property à créer)* |
| The Little Big Shop | — | `305480195` |

---

## ⚡ Skills Cowork

### Output Formats
| Skill | Déclencheur |
| :--- | :--- |
| `docx` | Word `.docx` |
| `xlsx` | Spreadsheet `.xlsx` |
| `pptx` | Présentation `.pptx` |
| `pdf` | PDF création/extraction |

### Engineering
| Skill | Usage |
| :--- | :--- |
| `engineering:code-review` | Review PR/diff |
| `engineering:system-design` | Architecture decisions |
| `engineering:incident-response` | Production incidents |
| `engineering:documentation` | README, runbooks, API docs |
| `mcp-builder` | Créer un nouveau serveur MCP |
| `crawl4ai` | Web scraping / extraction structurée |

### Data & Analytics
| Skill | Usage |
| :--- | :--- |
| `data:interactive-dashboard-builder` | HTML dashboards Chart.js |
| `data:sql-queries` | SQL multi-dialect |
| `data:data-visualization` | Charts Python (matplotlib, plotly) |
| `data:statistical-analysis` | Stats, outliers, hypothesis testing |

### Sales & Marketing
| Skill | Usage |
| :--- | :--- |
| `apollo:prospect` | ICP → leads enrichis |
| `apollo:enrich-lead` | Enrichissement contact |
| `marketing:seo-audit` | Audit SEO complet |
| `marketing:content-creation` | Blog, social, newsletter |
| `sales:competitive-intelligence` | Battlecards concurrents |

### Productivity
| Skill | Usage |
| :--- | :--- |
| `productivity:memory-management` | CLAUDE.md + memory/ |
| `schedule` | Tâches planifiées (cron) |

---

## 🗂️ Fichiers de Config Clés

| Fichier | Rôle |
| :--- | :--- |
| `~/Library/Application Support/Claude/claude_desktop_config.json` | Config MCP locaux + prefs Claude Desktop |
| `~/.config/gcloud/application_default_credentials.json` | Credentials Google ADC actifs |
| `~/.config/gcloud/palanthai_oauth_client.json` | OAuth client Desktop (project `palanthai` `690339909634`) |
| `~/.wrangler/` | Auth Cloudflare Wrangler |
