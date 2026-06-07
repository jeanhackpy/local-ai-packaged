---

kanban-plugin: basic

---

## Backlog
- [ ] Créer staging subdomain via Hostinger hPanel (staging.recall-agency.com)
- [ ] Ajouter credential WP dans n8n: "WordPress recall-agency.com" (HTTP Basic Auth, user: ttnl)
- [ ] Vérifier que Bearer Auth account dans n8n pointe vers OpenRouter API key
- [ ] Finaliser logo REcall (Minimalisme Apple) — pour remplacer le texte "REcall" dans la nav
- [ ] Implémenter geo-seo-claude full audit: /geo audit https://recall-agency.com
- [ ] Page /services/ dédiée pour chaque service (AI Analytics, PropTech, Cybersecurity, Automation)
- [ ] Setup Google Search Console OAuth pour n8n (gsc_client.py)

## In Progress
- [ ] Déployer theme v3 en staging: `bash DEPLOY.sh staging` (voir recall-agency-v2-theme/DEPLOY.sh)

## Done
- [x] Définition de la Brand Voice v1
- [x] Analyse Titleman.ai + Gap Analysis (05_Strategy_REBRANDING_report.md)
- [x] Audit SEO/GEO initial (SEO_GEO_Skills_Test_Report.md)
- [x] Theme v3 redesign: style.css + front-page.php + functions.php + customscript.js
  - Structure titleman.ai: Hero → Marquee → Services → Stats → Solutions tabs → Features → CTA
  - Positioning: "Intelligence Layer for Real Estate" (quiet dominance, not agentic hype)
  - Schema markup Organization + Service + Article dans functions.php
  - llms.txt endpoint pour AI crawlers
  - Security headers
- [x] n8n workflow créé: REcall Blog Rewriter — Weekly 2026
  - URL: https://n8n.recall-agency.com/workflow/uTRcoXaKKeUjAxdS
  - Trigger: Every Monday 8am + Manual
  - Flow: Fetch 5 posts → OpenRouter AI rewrite (Thailand 2026 focus) → WP REST API update
  - Modèle: google/gemma-3-27b-it:free (OpenRouter)
- [x] SEO fixes script: recall-agency-v2-theme/SEO_FIXES.sh
  - Meta descriptions préparées pour 5 posts
  - Instructions robots.txt AI crawlers
  - Instructions title tag homepage

## Session Journal
- **Date**: 2026-06-02
- **Session**: Rebrand & Redesign recall-agency.com — Business Plan 2026
- **Positioning décidé**: Titleman.ai style — "Intelligence Layer for Real Estate"
- **Staging**: Non configuré — à créer via Hostinger hPanel
- **Credentials n8n manquants**: WordPress recall-agency.com (HTTP Basic Auth)
