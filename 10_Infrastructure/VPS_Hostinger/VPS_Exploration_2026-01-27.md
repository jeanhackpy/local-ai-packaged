---
type: vps_exploration
date: '2026-01-27T18:30:00Z'
host: srv857744.hstgr.cloud
vm_id: 857744
status: running
---

# Exploration VPS Hostinger - 27 janvier 2026

## Vue d'ensemble

- **VM ID**: 857744
- **Hostname**: srv857744.hstgr.cloud
- **État**: Running (unlocked)
- **Plan**: KVM 2
- **OS**: Ubuntu 24.04 LTS
- **Créé le**: 2025-06-06T21:31:11Z
- **Data Center**: ID 20
- **Subscription**: AzqKy7UnNXj8B5HdC

## Configuration matérielle

- **CPU**: 2 vCPUs
- **RAM**: 8192 MB (8 GB)
- **Disque**: 102400 MB (100 GB)
- **Bande passante**: 8192000 MB
- **IPv4**: 31.97.67.145 (PTR: srv857744.hstgr.cloud)
- **IPv6**: 2a02:4780:59:3ad7::1 (PTR: srv857744.hstgr.cloud)
- **DNS**: 153.92.2.6 / 1.1.1.1

## Métriques sur 24h (26-27 janvier 2026)

### CPU
- **Moyenne**: ~30% (fluctuations entre 24% et 38%)
- **Pic observé**: 38.75%
- **Tendance**: Stable, pas de saturation
- **Load average 1m**: Non disponible via API (à vérifier localement)

### RAM
- **Utilisation**: Entre 5.1 GB et 6.4 GB sur 8 GB
- **Pic observé**: 6.4 GB (6404812800 bytes)
- **Tendance**: Croissance progressive sur la période
- **Disponible estimé**: ~1.5-2.5 GB (à confirmer localement)

### Disque
- **Utilisation**: Entre 70.3 GB et 71.5 GB sur 100 GB
- **Pic observé**: 76.7 GB (76768288768 bytes)
- **Tendance**: Croissance continue (~1 GB sur 24h)
- **% utilisé**: ~70-77%

### Réseau
- **Trafic entrant**: Variable, pics à ~191 MB et ~85 MB
- **Trafic sortant**: Variable, pics à ~16 MB et ~9 MB
- **Tendance**: Activité normale, pas d'anomalie détectée

### Uptime
- **Dernière valeur**: 77013 secondes (~21.4 heures)
- **Tendance**: Uptime stable, pas de redémarrage récent détecté

## Sécurité

### Monarx Malware Scanner
- **Statut**: Scan en cours
- **Scan démarré**: 2026-01-27T18:27:11Z
- **Scan terminé**: Non (en cours)
- **Fichiers scannés**: 0 (scan en cours)
- **Menaces détectées**: 0
- **Fichiers compromis**: 0
- **Records**: 0

**Note**: Le scan Monarx est actif mais en cours d'exécution. Aucune menace détectée pour l'instant.

## Snapshots & Backups

### Snapshots
- **Snapshot actif**: Aucun (id: 0)
- **Dernier snapshot créé**: 2026-01-17 (supprimé ensuite)

**Recommandation**: Créer un snapshot avant toute maintenance importante.

### Backups
- **Total disponible**: 2 backups
- **Backup #1**:
  - ID: 27378147
  - Date: 2026-01-25T10:36:43Z
  - Taille: 73.8 MB
  - Temps de restauration: 4544 secondes (~1h16)
  - Localisation: sg-nme-vpsbackups
- **Backup #2**:
  - ID: 26888518
  - Date: 2026-01-18T10:46:31Z
  - Taille: 64.6 MB
  - Temps de restauration: 4544 secondes (~1h16)
  - Localisation: sg-nme-vpsbackups

**Note**: Backups automatiques réguliers (environ toutes les semaines). Dernier backup il y a 2 jours.

## Clés SSH

### Clés attachées à la VM
- **Total**: 1 clé
- **Clé #1**:
  - ID: 293357
  - Nom: phil
  - Type: ssh-ed25519
  - Fingerprint: AAAAC3NzaC1lZDI1NTE5AAAAII4+SULBbPEU3eaw7T/p9OXZurIbx5GuhoG7m/9lDd6G

### Clés disponibles dans le compte
- **Total**: 1 clé (même clé que celle attachée)

**Note**: Une seule clé SSH configurée. Considérer l'ajout d'une clé de secours.

## Historique des actions récentes

**Total**: 78 actions au total (dernières 15 affichées)

### Actions récentes (dernières 48h)

1. **2026-01-26 20:39** - `ct_backup_restore` - Success (12 min)
2. **2026-01-26 20:05** - `ct_restart` - Success (8 sec)
3. **2026-01-26 19:29** - `ct_restart` - Success (9 sec)
4. **2026-01-26 18:50** - `ct_disk_cleanup` - Success (2 sec)
5. **2026-01-26 17:47** - `ct_restart` - Success (10 sec)

### Actions hebdomadaires

- **Backups créés**: 2 (25 jan, 18 jan)
- **Restarts**: Plusieurs (26 jan: 3x, 22 jan: 1x)
- **Disk cleanup**: Régulier (26 jan, 20 jan, 17 jan)
- **Snapshots**: Créés et supprimés le 17 jan

**Observations**:
- Activité de maintenance régulière (cleanup, restarts)
- Restauration de backup récente (26 jan)
- Pas de snapshot actif (tous supprimés)

## Analyse & Recommandations

### Points positifs

1. ✅ VM en état stable (running, unlocked)
2. ✅ Métriques CPU/RAM dans des limites acceptables
3. ✅ Backups automatiques réguliers
4. ✅ Monarx scanner actif
5. ✅ Historique d'actions montre maintenance proactive

### Points d'attention

1. ⚠️ **Disque**: Croissance continue (~1 GB/24h), actuellement à ~70-77%
   - **Action**: Surveiller la croissance, prévoir nettoyage si > 80%
   - **Recommandation**: Analyser les plus gros consommateurs (Docker, logs, données applicatives)

2. ⚠️ **RAM**: Utilisation élevée (6.4 GB / 8 GB max)
   - **Action**: Monitorer la disponibilité réelle (cache vs utilisé)
   - **Recommandation**: Vérifier si swap est configuré, considérer optimisation des services

3. ⚠️ **Snapshots**: Aucun snapshot actif
   - **Action**: Créer un snapshot avant maintenance importante
   - **Recommandation**: Intégrer snapshot dans le runbook de maintenance

4. ⚠️ **SSH Keys**: Une seule clé configurée
   - **Action**: Considérer l'ajout d'une clé de secours
   - **Recommandation**: Ajouter une clé de backup dans le compte Hostinger

5. ⚠️ **Monarx**: Scan en cours mais résultats non disponibles
   - **Action**: Attendre la fin du scan pour obtenir les métriques complètes
   - **Recommandation**: Vérifier périodiquement les résultats de scan

### Prochaines étapes

1. **Court terme** (cette semaine):
   - Finaliser l'analyse du scan Monarx
   - Créer un snapshot de précaution
   - Analyser l'occupation disque détaillée (via SSH)

2. **Moyen terme** (ce mois):
   - ✅ Mettre en place le monitoring automatisé (CPU/RAM/disk) → [[Journal_Travail_2026-01-28]]
   - ✅ Configurer les alertes Slack/Discord → [[Journal_Travail_2026-01-28]]
   - ✅ Documenter le runbook de maintenance complet → [[Journal_Travail_2026-01-28]]

3. **Long terme** (trimestre):
   - Optimiser l'utilisation disque (rotation logs, cleanup Docker)
   - Ajouter une clé SSH de secours
   - Automatiser les snapshots avant maintenance

## Données brutes API

### VM Details
```json
{
  "id": 857744,
  "state": "running",
  "actions_lock": "unlocked",
  "cpus": 2,
  "memory": 8192,
  "disk": 102400,
  "hostname": "srv857744.hstgr.cloud"
}
```

### Métriques (échantillon)
- CPU: 24-38% sur 24h
- RAM: 5.1-6.4 GB utilisés
- Disk: 70-77 GB utilisés
- Uptime: ~21h

### Backups
- 2 backups disponibles (25 jan, 18 jan)
- Taille: 64-74 MB
- Temps de restauration: ~1h16

---

*Note créée automatiquement via exploration Hostinger API MCP*
*Date: 2026-01-27T18:30:00Z*
