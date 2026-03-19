---
type: vps_action_plan
date: '2026-01-27T18:35:00Z'
status: draft
---

# Plan d'Action - Monitoring & Maintenance VPS Hostinger

## Contexte

Basé sur l'exploration complète du VPS `srv857744.hstgr.cloud` effectuée le 27 janvier 2026.

**État actuel**: VM stable, métriques dans les limites acceptables, mais croissance disque et RAM élevée à surveiller.

## Objectifs

1. Mettre en place un monitoring automatisé (CPU/RAM/disk/services)
2. Configurer des alertes Slack/Discord
3. Documenter un runbook de maintenance complet
4. Automatiser les snapshots avant maintenance

## Architecture proposée

### 1. Script de monitoring Python

**Emplacement**: `/Users/phil/Documents/AppsData/AgentManager_Cursor/monitor.py`

**Fonctionnalités**:
- Collecte métriques locales (CPU, RAM, disk) via `psutil`
- Évaluation des seuils (warning/critical)
- Envoi d'alertes Slack/Discord via webhook
- Optionnel: Vérification état VM via Hostinger API

**Seuils recommandés** (basés sur l'analyse):
- **CPU**: Warning > 70%, Critical > 90%
- **RAM available**: Warning < 1 GB, Critical < 512 MB
- **Disk**: Warning > 80%, Critical > 90%

**Fréquence**: Toutes les 5 minutes (cron)

### 2. Intégration Hostinger MCP

**Avantages**:
- Pas besoin de gérer tokens API dans le script
- Accès direct via outils MCP depuis Cursor
- Automatisation possible via scripts Python appelant MCP

**Utilisation**:
- Vérification état VM avant maintenance
- Création snapshots programmés
- Récupération métriques historiques
- Gestion backups

### 3. Runbook de maintenance

**Structure**:
1. **Pré-maintenance**:
   - Vérifier état VM (via MCP)
   - Créer snapshot (via MCP)
   - Vérifier Monarx status
   - Vérifier clés SSH

2. **Maintenance**:
   - Audit RAM (processus gourmands)
   - Audit disque (Docker, logs, données)
   - Nettoyage ciblé
   - Optimisation CPU si nécessaire

3. **Post-maintenance**:
   - Vérifications système
   - Vérification snapshot créé
   - Option rollback si problème

### 4. Logs Obsidian

**Structure**:
- `Infra/VPS_Hostinger/VPS_Exploration_YYYY-MM-DD.md` - Explorations périodiques
- `Infra/VPS_Hostinger/logs/YYYYMMDD_HHMM_maintenance-<nom>.md` - Logs de maintenance
- `Infra/VPS_Hostinger/monitoring/YYYY-WW.md` - Résumés hebdomadaires

## Prochaines étapes immédiates

1. ✅ Exploration complète VPS (fait) → [[VPS_Exploration_2026-01-27]]
2. ✅ Créer le script de monitoring Python → [[Journal_Travail_2026-01-28]]
3. ✅ Configurer les webhooks Slack/Discord → [[Journal_Travail_2026-01-28]]
4. ✅ Tester le monitoring avec seuils réels → [[Journal_Travail_2026-01-28]]
5. ✅ Documenter le runbook complet → [[Journal_Travail_2026-01-28]]
6. ✅ Automatiser les logs Obsidian → [[Journal_Travail_2026-01-28]], [[Kanban_Travail]], [[TODO]]

**Suivi actuel**: Voir [[Kanban_Travail]] pour l'état des tâches et [[TODO]] pour la liste complète.

## Métriques de référence (27 jan 2026)

- **CPU moyen**: ~30% (pic 38.75%)
- **RAM utilisée**: 5.1-6.4 GB / 8 GB
- **Disk utilisé**: 70-77 GB / 100 GB (~70-77%)
- **Croissance disque**: ~1 GB / 24h
- **Uptime**: Stable (~21h)

## Seuils ajustés selon réalité

Basés sur les métriques observées:
- **CPU**: Warning > 50% (actuellement ~30%), Critical > 80%
- **RAM**: Warning < 1.5 GB available, Critical < 800 MB
- **Disk**: Warning > 85% (actuellement ~77%), Critical > 92%

---

*Plan créé le 2026-01-27T18:35:00Z*
*Basé sur exploration Hostinger API MCP*
