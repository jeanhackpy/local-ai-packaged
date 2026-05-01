---

kanban-plugin: basic

---

## Backlog

- [ ] #agent-claude #priority-critical #type-security [SECURITY] Rotate all exposed credentials (VPS PG, Neo4j, Supabase anon key, 15+ API keys in .env)
- [ ] #agent-claude #priority-critical #type-security [SECURITY] Fix command injection in sync_service.py and start_services.py (subprocess.run shell=True)
- [ ] #agent-claude #priority-high #type-security [SECURITY] Move all hardcoded credentials to .env files
- [ ] #agent-claude #priority-high #type-security [SECURITY] Add .env files to .gitignore / .dockerignore
- [ ] #agent-claude #priority-high #type-security [SECURITY] Implement RLS policies on Supabase (if not already done per 2026-04-03 audit)
- [ ] #agent-claude #priority-medium #type-security [SECURITY] Add retry logic + exponential backoff to wf_extract scripts
- [ ] #agent-claude #priority-medium #type-security [SECURITY] Sanitize all scraped HTML content before storing
- [ ] #agent-claude #priority-medium #type-monitoring Ajuster seuils monitoring selon comportement réel après 1 semaine
- [ ] #agent-claude #priority-low #type-docs Ajouter health checks applicatifs (HTTP endpoints)
- [ ] #agent-claude #priority-low #type-monitoring Intégration Prometheus + Grafana
- [ ] #agent-claude #priority-medium #type-maintenance Optimisation disque (nettoyage Docker, rotation logs)

## In Progress

- [ ] #agent-claude #priority-high #type-docs Créer système synchronisation multi-agents Obsidian

## Review

- [ ] #agent-claude #priority-high #type-monitoring Implémenter monitoring script avec services critiques
- [ ] #agent-claude #priority-high #type-runbook Créer runbook maintenance complet
- [ ] #agent-claude #priority-medium #type-docs Documenter procédures maintenance

## Done

- [x] #agent-claude #priority-high #type-monitoring Exploration complète VPS (2026-01-27)
- [x] #agent-claude #priority-high #type-monitoring Implémenter monitoring script (2026-01-28)
- [x] #agent-claude #priority-high #type-runbook Créer runbook maintenance (2026-01-28)
- [x] #agent-claude #priority-high #type-testing Créer tests unitaires (2026-01-28)
- [x] #agent-claude #priority-medium #type-docs Documenter système complet (2026-01-28)

## Blocked

- [ ] #agent-claude #priority-low #type-infra Déploiement sur VPS (en attente credentials)

---

## Légende

**Tags agents**: `#agent-claude`, `#agent-gemini`, etc.
**Priorités**: `#priority-high`, `#priority-medium`, `#priority-low`
**Types**: `#type-monitoring`, `#type-runbook`, `#type-docs`, `#type-testing`, `#type-infra`, `#type-maintenance`

**Workflow**:
1. Prendre une carte du Backlog
2. Déplacer en "In Progress" avec tag agent
3. Créer journal de travail avec lien vers carte
4. Déplacer en "Review" ou "Done" à la fin
