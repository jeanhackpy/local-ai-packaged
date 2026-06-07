---
type: migration_runbook
tags: [vps, migration, oracle-cloud, docker, backup, runbook, critical]
created: 2026-06-01
status: active
target_window: 2026-06-01 → 2026-06-02
from: Hostinger KVM 2 (2 vCPU / 7.8 GB RAM / 96 GB SSD) — srv857744 (31.97.67.145)
to: Oracle Cloud Free Tier Singapore (4 vCPU / **24 GB RAM** / **200 GB SSD**)
---

# 🚀 Migration Runbook — Hostinger → Oracle Cloud Singapore

> **Mission** : Migrer 100% du stack actuel vers un nouveau VPS Oracle Cloud Free Tier Singapore dans les 24h. Tout doit pouvoir être migré via GitHub + Docker. Ajout de 3 nouveaux services en Docker : **Playwright**, **crawl4ai**, **hermes-agent** (optionnel).

---

## 1. 🎯 Objectifs

### Incompressibles
- ✅ Zéro perte de données DB (53 301 units + 6 646 projets + 145 tables) — **via B2 pg_dump**
- ✅ n8n workflows + credentials préservés (chiffrés dans PostgreSQL)
- ✅ Code + configs via Git (3 repos + vault local)
- ✅ Caddy TLS (auto-regen si hostname OK)
- ✅ Backups B2 fonctionnels sur le nouveau VPS

### Volontairement non migrés (rebuild from scratch sur nouveau VPS)
- ❌ **Qdrant vectors** (45 039 + 200 dans 6 collections) — Phil va refaire l'embedding avec un meilleur modèle
- ❌ **Neo4j graph** — Phil va reconstruire le graph property intelligence
- ➡️ Ces services démarrent **vides** sur le nouveau VPS. Les scripts d'embedding/ingestion repartent depuis le PG (qui lui est restauré).

### Améliorations
- 🆕 **Playwright en Docker** (au lieu de `venv-playwright` sur host)
- 🆕 **crawl4ai en Docker** (au lieu de crawl4ai Python dans venv)
- 🆕 **hermes-agent en Docker** (au lieu de Python venv `~/.hermes/`)
- 🆕 Plus de RAM (24 GB vs 7.8 GB) → pas besoin de memory limits serrés
- 🆕 Plus de disk (200 GB vs 96 GB) → place pour backups locaux + Ollama models + B2 mirror local
- 🆕 Oracle Cloud = pas de coût récurrent

---

## 2. 📋 Pré-migration (Checklist AVANT de toucher au nouveau VPS)

### 2.1 Sauvegarder les secrets et données hors-Git

```bash
# Sur le Mac, créer un dossier migration sécurisé
mkdir -p ~/migration-2026-06-01 && cd ~/migration-2026-06-01

# 1. Env files (CRITIQUES — pas dans git)
scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env ./local-ai.env
scp phil@31.97.67.145:/home/phil/palanthai/config/.env ./palanthai.env
scp phil@31.97.67.145:/home/phil/palanthai/config/google_service_account.json ./
scp phil@31.97.67.145:/home/phil/.config/rclone/rclone.conf ./rclone.conf

# 2. Clés SSH du VPS (pour les remettres dans authorized_keys)
scp phil@31.97.67.145:~/.ssh/authorized_keys ./vps-authorized-keys

# 3. .env.example / .env.bak pour référence
scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env.example ./
scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env.bak.20260326 ./
```

### 2.2 Qdrant — ⏭️ SKIP (rebuild from scratch)

**Pas de snapshot Qdrant** — Phil va reconstruire les embeddings avec un meilleur pipeline sur le nouveau VPS (modèle upgraded probablement, possiblement via crawl4ai + Playwright). Les données sources (units, projects) sont dans PostgreSQL qui sera restauré.

Sur le nouveau VPS, le container Qdrant démarre vide, et on re-pousse les embeddings depuis PG via le pipeline phase3_embedding_graph (qui sera probablement modifié).

### 2.3 Neo4j — ⏭️ SKIP (rebuild from scratch)

**Pas de dump Neo4j** — le graph property intelligence sera reconstruit depuis zéro sur le nouveau VPS. Données sources dans PG restauré.

Le container Neo4j démarre vide. Le pipeline phase3 (ou un nouveau) re-pousse les nodes/relationships depuis PG.

### 2.4 Palanthai extracted data (221 projets + 1176 units)

```bash
rsync -avz --progress phil@31.97.67.145:/home/phil/palanthai/phase1_extraction/backups/extracted/ \
  ~/migration-2026-06-01/extracted/

# Vérifier
ls ~/migration-2026-06-01/extracted/projects | wc -l   # 221
ls ~/migration-2026-06-01/extracted/units | wc -l       # 1176
```

### 2.5 MinIO data (si volumineux)

```bash
# Option A : via mc
ssh phil@31.97.67.145 << 'EOF'
  apt install -y mc 2>/dev/null || true
  mc alias set local http://localhost:9000 minio $(cat /home/phil/local-ai-packaged/.env | grep MINIO_ROOT_PASSWORD | cut -d= -f2)
  mc mirror local/ /tmp/minio-mirror/  # ou B2 destination
EOF

# Option B : direct rsync du volume (peut nécessiter sudo)
ssh phil@31.97.67.145 "sudo tar czf /tmp/minio-volume.tgz -C /var/lib/docker/volumes/localai_minio_storage _data"
scp phil@31.97.67.145:/tmp/minio-volume.tgz ~/migration-2026-06-01/
```

### 2.6 Forcer un dernier backup DB

```bash
ssh phil@31.97.67.145 'bash /home/phil/palanthai/scripts/backup_db.sh daily'
ssh phil@31.97.67.145 'tail -5 /home/phil/palanthai/phase1_extraction/backups/logs/backup.log'
# Doit montrer "Backup complete"
```

### 2.7 Récupérer un dump B2 frais en local (pour restore rapide)

```bash
# Installer rclone sur Mac (une fois)
brew install rclone

# Configurer le remote B2 (copier la conf depuis le VPS)
mkdir -p ~/.config/rclone
cp ~/migration-2026-06-01/rclone.conf ~/.config/rclone/rclone.conf
chmod 600 ~/.config/rclone/rclone.conf

# Test
rclone lsd b2-palanthai:  # doit lister palanthai-backups/

# Récupérer le dernier dump
LATEST=$(rclone lsjson b2-palanthai:palanthai-backups/db/ | jq -r '.[].Path' | sort | tail -1)
echo "Latest dump: $LATEST"
rclone copy "b2-palanthai:palanthai-backups/db/$LATEST" ~/migration-2026-06-01/
```

---

## 3. 🖥️ Provisioning Oracle Cloud Singapore

### 3.1 Créer l'instance

1. Console Oracle Cloud → Compute → Instances → Create Instance
2. **Image** : Ubuntu 24.04 LTS (ou 22.04 pour compat)
3. **Shape** : `VM.Standard.A1.Flex` (4 OCPU / 24 GB RAM — **toujours le free tier eligible**)
4. **Boot volume** : 200 GB (max free tier)
5. **Networking** : VCN + subnet public, assigner IP publique
6. **SSH key** : upload ta clé publique `~/.ssh/id_ed25519.pub`
7. **User data** : (rien pour l'instant)

### 3.2 Premier accès + setup de base

```bash
# Connexion initiale (IP publique fournie par Oracle)
ssh ubuntu@<ORACLE_IP>

# Mettre à jour
sudo apt update && sudo apt upgrade -y

# Installer les outils de base
sudo apt install -y \
  git curl wget vim htop ncdu \
  docker.io docker-compose-plugin \
  rclone \
  build-essential python3.12 python3.12-venv python3-pip \
  ufw fail2ban unattended-upgrades \
  jq unzip

# Ajouter l'utilisateur 'phil' (reproduire l'ancien user)
sudo useradd -m -s /bin/bash phil
sudo usermod -aG docker phil
sudo usermod -aG sudo phil

# Copier la clé SSH
sudo mkdir -p /home/phil/.ssh
sudo cp ~/.ssh/authorized_keys /home/phil/.ssh/
sudo chown -R phil:phil /home/phil/.ssh
sudo chmod 700 /home/phil/.ssh && sudo chmod 600 /home/phil/.ssh/authorized_keys

# Reconnecter en tant que phil
ssh phil@<ORACLE_IP>
```

### 3.3 Firewall Oracle + iptables

```bash
# Ports à ouvrir (dans Oracle VCN Security List + iptables local)
sudo ufw allow OpenSSH
sudo ufw allow 80/tcp
sudo ufw allow 443/tcp
# NE PAS ouvrir publiquement : 5432, 5678, 6333, 7473, 7474, 7687, 8081, 11434, 8765
# → utiliser un VPN ou Tailscale pour y accéder
sudo ufw enable
sudo ufw status

# Activer fail2ban
sudo systemctl enable --now fail2ban
```

### 3.4 Tailscale (accès privé)

```bash
curl -fsSL https://tailscale.com/install.sh | sh
sudo tailscale up
sudo tailscale ip -4  # noter la nouvelle IP Tailscale (sera différente de 100.78.110.61)
```

---

## 4. 📦 Setup des repos + secrets

### 4.1 Cloner les 4 repos

```bash
sudo -u phil -i
mkdir -p ~/repos && cd ~/repos

git clone https://github.com/jeanhackpy/palanthai.git
git clone https://github.com/jeanhackpy/local-ai-packaged.git
git clone https://github.com/jeanhackpy/obsidian-leon.git
# (SystemMac reste sur Mac, pas besoin de cloner ici)

cd ~/repos/local-ai-packaged
git log --oneline -3  # vérifier dernier commit cohérent
```

### 4.2 Remettre le `.env` complet

```bash
# Depuis le Mac
scp ~/migration-2026-06-01/local-ai.env phil@<ORACLE_IP>:/home/phil/repos/local-ai-packaged/.env
scp ~/migration-2026-06-01/palanthai.env phil@<ORACLE_IP>:/home/phil/repos/palanthai/config/.env
scp ~/migration-2026-06-01/google_service_account.json phil@<ORACLE_IP>:/home/phil/repos/palanthai/config/

# rclone config
scp ~/migration-2026-06-01/rclone.conf phil@<ORACLE_IP>:/home/phil/.config/rclone/rclone.conf
ssh phil@<ORACLE_IP> 'chmod 600 /home/phil/.config/rclone/rclone.conf'
```

### 4.3 Vérifier que le `.env` est complet

```bash
ssh phil@<ORACLE_IP> 'cd /home/phil/repos/local-ai-packaged && \
  grep -oE "^[A-Z_][A-Z0-9_]*=" .env | sort -u | wc -l'
# Doit afficher ~40 clés

ssh phil@<ORACLE_IP> 'cd /home/phil/repos/palanthai && \
  grep -oE "^[A-Z_][A-Z0-9_]*=" config/.env | sort -u | wc -l'
# Doit afficher 20 clés
```

---

## 5. 🐳 Setup Docker + nouvelle stack

### 5.1 Cloner supabase (via start_services.py)

```bash
ssh phil@<ORACLE_IP> << 'EOF'
  cd /home/phil/repos/local-ai-packaged
  # start_services.py clone supabase si manquant + merge .env
  python3 start_services.py --profile gpu  # ou pas de profile
EOF
```

### 5.2 Neo4j — ⏭️ SKIP (démarre vide)

Neo4j démarre avec un graph vide. Le pipeline de reconstruction (à définir) re-pousse les nodes/relationships depuis PostgreSQL. Prévoir dans la todo post-migration :
- Définir le schéma cible (nodes, relationships, properties)
- Script d'ingestion depuis `replica_projects_live` + `replica_unit` + `unit_features`
- Validation (counts, sanity checks)

### 5.3 Premier lancement de la stack de base

```bash
ssh phil@<ORACLE_IP> << 'EOF'
  cd /home/phil/repos/local-ai-packaged
  docker compose up -d
  
  # Vérifier que tout monte
  sleep 30
  docker ps --format "table {{.Names}}\t{{.Status}}\t{{.Ports}}"
  
  # Doit voir : caddy, qdrant, n8n, neo4j, minio, redis, searxng, 
  #              ollama-cpu, supabase-db, supabase-auth, supabase-rest,
  #              supabase-studio, supabase-storage, supabase-kong,
  #              supabase-pooler, supabase-imgproxy, supabase-edge-functions,
  #              realtime, supabase-meta
EOF
```

### 5.4 Qdrant — ⏭️ SKIP (démarre vide)

Qdrant démarre sans aucune collection. Prévoir dans la todo post-migration :
- Définir la nouvelle stratégie d'embedding (modèle upgraded probable — ex: BGE-M3 via Ollama Cloud, ou nouveau modèle via crawl4ai)
- Recréer les collections avec les nouvelles dimensions (768 → 1024 ?)
- Re-pousser les embeddings depuis PG (53 301 units + 6 646 projects) via le pipeline phase3
- **Coût estimé** : 30-60 min de calcul sur le nouveau VPS (24 GB RAM permet de charger des modèles plus gros)

### 5.5 Restaurer la DB PostgreSQL depuis B2 (ou dump local)

```bash
# Option A : depuis le dump local (plus rapide)
scp ~/migration-2026-06-01/palanthai_*.dump phil@<ORACLE_IP>:/tmp/latest.dump

# Option B : depuis B2
ssh phil@<ORACLE_IP> << 'EOF'
  rclone copy b2-palanthai:palanthai-backups/db/ /tmp/db-dumps/ --progress
  LATEST=$(ls -t /tmp/db-dumps/*.dump | head -1)
  echo "Using: $LATEST"
  
  # Restore
  docker exec -i supabase-db pg_restore -U postgres -d postgres --clean --if-exists < "$LATEST"
EOF
```

### 5.6 Setup MinIO data restore

```bash
scp ~/migration-2026-06-01/minio-volume.tgz phil@<ORACLE_IP>:/tmp/
ssh phil@<ORACLE_IP> << 'EOF'
  # Stop MinIO
  cd /home/phil/repos/local-ai-packaged
  docker compose stop minio
  
  # Extract dans le volume
  MINIO_VOL=$(docker volume inspect --format '{{.Mountpoint}}' local-ai-packaged_minio_storage)
  sudo tar xzf /tmp/minio-volume.tgz -C "$MINIO_VOL"
  
  # Restart
  docker compose start minio
EOF
```

### 5.7 Setup du backup cron sur le nouveau VPS

```bash
ssh phil@<ORACLE_IP> << 'EOF'
  # Copier le script backup_db.sh depuis palanthai (déjà dans git)
  ls -la /home/phil/repos/palanthai/scripts/backup_db.sh
  
  # Ajouter au crontab
  (crontab -l 2>/dev/null; echo "0 3 * * * /home/phil/repos/palanthai/scripts/backup_db.sh daily") | crontab -
  
  # Editer le script pour pointer vers /home/phil/repos/palanthai au lieu de /home/phil/palanthai
  # (le script référence /home/phil/palanthai/phase1_extraction/backups)
  # Option : symlink
  sudo ln -s /home/phil/repos/palanthai /home/phil/palanthai
  sudo chown -h phil:phil /home/phil/palanthai
EOF
```

---

## 6. 🆕 Ajout des nouveaux services Docker

### 6.1 Playwright (Docker)

**Pourquoi en Docker :** actuellement `venv-playwright` sur host (153 MB) — on le déplace pour reproductibilité.

```yaml
# Ajouter à /home/phil/repos/local-ai-packaged/docker-compose.override.private.yml
services:
  playwright:
    image: mcr.microsoft.com/playwright:v1.49.0-jammy
    container_name: playwright
    restart: unless-stopped
    working_dir: /home/pwuser
    user: pwuser
    volumes:
      - ./shared/pipelines:/home/pwuser/scripts:ro
      - playwright-cache:/ms-playwright
    networks:
      - default
    deploy:
      resources:
        limits:
          memory: 2g
    # Lancement interactif : docker exec -it playwright bash
    stdin_open: true
    tty: true
    command: ["sleep", "infinity"]

volumes:
  playwright-cache:
```

Setup :
```bash
# Sur le nouveau VPS
cd /home/phil/repos/local-ai-packaged
docker compose up -d playwright
docker exec -it playwright bash
# dans le container :
# npx playwright install chromium
# ou apt install + browsers
```

### 6.2 crawl4ai (Docker)

**Pourquoi en Docker :** actuellement en subprocess Python dans venv. Docker = isolation + API stable.

```yaml
# Ajouter à docker-compose.override.private.yml
services:
  crawl4ai:
    image: unclecode/crawl4ai:0.6.0  # ou latest
    container_name: crawl4ai
    restart: unless-stopped
    expose:
      - 11235/tcp
    environment:
      - CRAWL4AI_API_TOKEN=${CRAWL4AI_API_TOKEN:-}
    volumes:
      - crawl4ai-data:/app/data
    deploy:
      resources:
        limits:
          memory: 1g

volumes:
  crawl4ai-data:
```

Setup :
```bash
docker compose up -d crawl4ai
# Vérifier
curl -s http://localhost:11235/health
# Doit exposer une API REST pour les jobs de crawl
```

Connexion depuis n8n : `http://crawl4ai:11235` (Docker DNS interne).

### 6.3 hermes-agent (Docker, optionnel)

**Décision à prendre :** le run actuel de Hermes est `python3 /home/phil/.hermes/hermes-agent/hermes_cli/main.py gateway run --replace` (PID 968). C'est un process Python complexe avec venv, plugins, state SQLite.

**Option A — Garder sur host (recommandé pour la 1ère itération) :**
```bash
# Sur le nouveau VPS
cd /home/phil
# Restaurer le dossier .hermes (pas dans git !)
scp -r phil@31.97.67.145:/home/phil/.hermes /home/phil/
# Reconstruire le venv hermes (si pas dans git)
cd /home/phil/.hermes && python3 -m venv venv && venv/bin/pip install -r requirements.txt
# Lancer
nohup /home/phil/.hermes/venv/bin/python3 /home/phil/.hermes/hermes-agent/hermes_cli/main.py gateway run --replace &
```

**Option B — Dockeriser (à faire dans un 2ème temps) :**

```yaml
services:
  hermes:
    build:
      context: ./hermes
      dockerfile: Dockerfile
    container_name: hermes
    restart: unless-stopped
    volumes:
      - hermes-data:/app/data
      - hermes-memories:/app/memories
      - hermes-cache:/app/cache
    ports:
      - 9119:9119
    environment:
      - HERMES_DASHBOARD_BIND=0.0.0.0
    deploy:
      resources:
        limits:
          memory: 2g

volumes:
  hermes-data:
  hermes-memories:
  hermes-cache:
```

**Ma recommandation :** Option A pour la migration immédiate (réutiliser le state existant), Option B dans les 2 semaines qui suivent.

---

## 7. 🔄 DNS + Caddy + TLS

### 7.1 Mettre à jour les DNS

Dans ton registrar (Cloudflare probable ?) :
```
n8n.recall-agency.com       A   <ORACLE_IP>
supabase.recall-agency.com  A   <ORACLE_IP>
neo4j.recall-agency.com     A   <ORACLE_IP>
```

Attendre la propagation (5-30 min).

### 7.2 Vérifier que Caddy obtient les certs

```bash
ssh phil@<ORACLE_IP> << 'EOF'
  docker logs caddy --tail 30
  # Doit montrer "obtained certificate" pour chaque hostname
  
  # Test depuis l'extérieur
  curl -I https://n8n.recall-agency.com
  curl -I https://supabase.recall-agency.com
EOF
```

---

## 8. 🚀 Lancer Palanthai API sur le nouveau VPS

```bash
ssh phil@<ORACLE_IP> << 'EOF'
  cd /home/phil/repos/palanthai
  python3 -m venv venv
  source venv/bin/activate
  pip install -r requirements.lock.txt  # ou pip install palanthai deps
  # (Phase 1 venv séparé si besoin : cd phase1_extraction && python3 -m venv venv && ...)
  
  # Tester le start
  bash start_api.sh
  sleep 5
  curl -s http://localhost:8765/health
  tail -20 api.log
EOF
```

---

## 9. 🛡️ Sécurité post-migration

Sur le nouveau VPS :

1. **Changer les mots de passe** (DB PG, Neo4j, MinIO, n8n) — opportunité de rotation
2. **Activer `fail2ban`** : `sudo systemctl enable --now fail2ban`
3. **Tailscale** : déjà actif
4. **UFW** : déjà actif, vérifier
5. **Désactiver le port SSH password** : `sudo nano /etc/ssh/sshd_config` → `PasswordAuthentication no`
6. **Audit** : re-lire le [[VPS_Security_Audit_2026-05-01]] et fixer ce qui n'a pas été fait

---

## 10. ❌ Cleanup post-migration sur l'ancien VPS

Une fois que TOUT marche sur Oracle :

1. **Vérifier une dernière fois** que :
   - DB accessible via n8n
   - Qdrant queries fonctionnent
   - Palanthai API répond
   - Backups B2 tournent
   - Tous les workflows n8n s'exécutent

2. **Éteindre l'ancien VPS** : ne PAS le supprimer tout de suite (garder 7 jours pour rollback)
   - Via panel Hostinger → Stop instance
   - OU via SSH : `sudo shutdown -h now`

3. **Documenter** les changements dans le wiki / changelog

---

## 11. 📊 Inventaire final des ressources

| Resource | Hostinger (old) | Oracle Cloud (new) |
|---|---|---|
| vCPU | 2 | 4 (OCPU = 1 vCPU) |
| RAM | 7.8 GB | **24 GB** |
| Disk | 96 GB (87% used) | **200 GB** |
| Bandwidth | 1 TB/mois (?) | 10 TB/mois (free) |
| Coût | ~5-10€/mois | 0 € |
| Provider lock-in | Non | Faible (OCI) |

### Allocation RAM recommandée (24 GB total)

| Service | Limit Docker | Notes |
|---|---|---|
| Palanthai API (host) | 2 GB | Python + venv |
| HERMES (host ou docker) | 2 GB |  |
| n8n | 1 GB |  |
| Qdrant | 2 GB | pourra indexer 100k+ vectors |
| Neo4j | 2 GB |  |
| Supabase (PostgreSQL) | 2 GB |  |
| Supabase Studio | 1 GB |  |
| Supabase Kong | 256 MB |  |
| Supabase Storage | 512 MB |  |
| Supabase Realtime | 256 MB |  |
| Supabase Auth | 128 MB |  |
| Supabase Meta | 128 MB |  |
| Supabase Imgproxy | 256 MB |  |
| Supabase Edge | 256 MB |  |
| Caddy | 128 MB |  |
| MinIO | 512 MB |  |
| Valkey/Redis | 512 MB |  |
| Ollama | 4 GB (CPU mode) | modèles ~2-3 GB loaded |
| SearXNG | 256 MB |  |
| **Playwright (NEW)** | 2 GB | Chromium headless |
| **Crawl4ai (NEW)** | 1 GB | API REST |
| **OS + buffers** | 2-3 GB |  |
| **Total** | ~24 GB | ✅ |

---

## 12. 📚 Documents liés

- [[VPS_BACKUP_INFRASTRUCTURE]] — état détaillé des backups
- [[VPS_ACCESS_REFERENCE]] — accès SSH et services
- [[VPS_SERVICE_MAP]] — inventaire détaillé
- [[VPS_INFRASTRUCTURE_REFERENCE]] — référence complète
- [[VPS_ARCHITECTURE_DIAGRAM]] — diagrammes Mermaid
- [[Network_Architecture]] — réseau et routage
- [[VPS_Security_Audit_2026-05-01]] — findings sécurité à fixer

---

*Runbook créé le 2026-06-01 | Status : ✅ Prêt pour exécution*
*Une fois migration terminée, créer un post-mortem et mettre à jour toute la doc pour refléter le nouvel environnement Oracle Cloud.*
