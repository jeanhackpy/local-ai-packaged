# VPS Maintenance Guide

Complete guide for maintaining your local-ai-packaged deployment on a VPS, including daily operations, backups, updates, and troubleshooting.

## Table of Contents

- [Daily Operations](#daily-operations)
- [Service Management](#service-management)
- [Monitoring & Logs](#monitoring--logs)
- [Backup Procedures](#backup-procedures)
- [Update Workflows](#update-workflows)
- [Rollback Procedures](#rollback-procedures)
- [Disk Space Management](#disk-space-management)
- [Security Best Practices](#security-best-practices)
- [Troubleshooting](#troubleshooting)

---

## Daily Operations

### Quick Health Check

```bash
# Check all running containers
docker ps

# Check container resource usage
docker stats --no-stream

# Check disk space
df -h

# Check Docker disk usage
docker system df
```

### Accessing Services

| Service | Local Access | Production Access |
|---------|-------------|-------------------|
| n8n | http://localhost:5678 | https://n8n.recall-agency.com |
| Open WebUI | http://localhost:3000 | https://openwebui.recall-agency.com |
| Supabase | http://localhost:8000 | http://YOUR_VPS_IP:8000 |
| Qdrant | http://localhost:6333 | http://YOUR_VPS_IP:6333 |
| Neo4j | http://localhost:7474 | http://YOUR_VPS_IP:7474 |
| OpenClaw | http://localhost:18789 | http://YOUR_VPS_IP:18789 |

---

## Service Management

### Starting Services

```bash
# Start all services (use your GPU profile)
cd /home/phil/local-ai-packaged
python3 start_services.py --profile gpu-nvidia --environment public

# Or for CPU only
python3 start_services.py --profile cpu --environment public
```

### Stopping Services

```bash
# Stop all services
docker compose -p localai down

# Stop specific service
docker stop container-name

# Stop and remove all containers, networks, volumes
docker compose -p localai down -v  # ⚠️ This deletes volumes!
```

### Restarting Services

```bash
# Restart all services
docker compose -p localai restart

# Restart specific service
docker restart container-name

# Restart after config changes
docker compose -p localai up -d --force-recreate
```

### Viewing Service Status

```bash
# List all containers in the project
docker compose -p localai ps

# Check if a specific container is running
docker ps | grep container-name

# View container details
docker inspect container-name
```

---

## Monitoring & Logs

### Viewing Logs

```bash
# View logs for all services
docker compose -p localai logs

# Follow logs in real-time
docker compose -p localai logs -f

# View logs for specific service
docker logs container-name

# Follow logs for specific service
docker logs -f container-name

# View last 100 lines
docker logs --tail 100 container-name

# View logs with timestamps
docker logs -t container-name
```

### Monitoring Resources

```bash
# Real-time resource usage
docker stats

# Check memory usage
free -h

# Check CPU usage
top
# or
htop  # if installed

# Check network connections
netstat -tulpn | grep LISTEN
```

### Disk Usage

```bash
# Check overall disk usage
df -h

# Check Docker disk usage
docker system df

# Check size of specific directories
du -sh /home/phil/local-ai-packaged/*

# Find large files
find /home/phil/local-ai-packaged -type f -size +100M -exec ls -lh {} \;
```

---

## Backup Procedures

### What to Backup

1. **Configuration files** (.env, docker-compose.yml, Caddyfile)
2. **Database data** (Supabase/Postgres, Neo4j)
3. **Docker volumes** (n8n, Ollama models, Qdrant)
4. **Custom workflows** (n8n workflows)

### Backup Configuration Files

```bash
# Create backup directory
mkdir -p ~/backups/$(date +%Y-%m-%d)

# Backup configuration files
cd /home/phil/local-ai-packaged
cp .env ~/backups/$(date +%Y-%m-%d)/
cp docker-compose.yml ~/backups/$(date +%Y-%m-%d)/
cp Caddyfile ~/backups/$(date +%Y-%m-%d)/
cp -r caddy-addon ~/backups/$(date +%Y-%m-%d)/

# Create a tarball
tar -czf ~/backups/config-$(date +%Y-%m-%d).tar.gz \
  .env docker-compose*.yml Caddyfile caddy-addon/
```

### Backup Docker Volumes

```bash
# List all volumes
docker volume ls

# Backup n8n data
docker run --rm \
  -v localai_n8n_storage:/data \
  -v ~/backups:/backup \
  alpine tar -czf /backup/n8n-$(date +%Y-%m-%d).tar.gz -C /data .

# Backup Ollama models
docker run --rm \
  -v localai_ollama_storage:/data \
  -v ~/backups:/backup \
  alpine tar -czf /backup/ollama-$(date +%Y-%m-%d).tar.gz -C /data .

# Backup Qdrant data
docker run --rm \
  -v localai_qdrant_storage:/data \
  -v ~/backups:/backup \
  alpine tar -czf /backup/qdrant-$(date +%Y-%m-%d).tar.gz -C /data .
```

### Backup Supabase Database

```bash
# Backup Postgres database
docker exec -t db pg_dumpall -c -U postgres > ~/backups/supabase-$(date +%Y-%m-%d).sql

# Compress the backup
gzip ~/backups/supabase-$(date +%Y-%m-%d).sql
```

### Automated Backup Script

Create a backup script at `/home/phil/backup-local-ai.sh`:

```bash
#!/bin/bash
BACKUP_DIR=~/backups/$(date +%Y-%m-%d)
mkdir -p $BACKUP_DIR

cd /home/phil/local-ai-packaged

# Backup configs
tar -czf $BACKUP_DIR/config.tar.gz .env docker-compose*.yml Caddyfile caddy-addon/

# Backup database
docker exec -t db pg_dumpall -c -U postgres | gzip > $BACKUP_DIR/supabase.sql.gz

# Backup n8n
docker run --rm -v localai_n8n_storage:/data -v $BACKUP_DIR:/backup alpine tar -czf /backup/n8n.tar.gz -C /data .

echo "Backup completed: $BACKUP_DIR"

# Keep only last 7 days of backups
find ~/backups -type d -mtime +7 -exec rm -rf {} +
```

Make it executable and run:
```bash
chmod +x ~/backup-local-ai.sh
./backup-local-ai.sh
```

---

## Update Workflows

### Updating the Repository

```bash
cd /home/phil/local-ai-packaged

# Check current status
git status

# Stash any local changes
git stash

# Pull latest changes
git pull origin main

# Apply your stashed changes back
git stash pop

# If there are conflicts, resolve them manually
```

### Updating Docker Images

```bash
# Pull latest images
docker compose -p localai pull

# Restart services with new images
docker compose -p localai up -d

# Or use the start script
python3 start_services.py --profile gpu-nvidia --environment public
```

### Updating Specific Services

```bash
# Update only n8n
docker compose -p localai pull n8n
docker compose -p localai up -d n8n

# Update Ollama
docker compose -p localai pull ollama-gpu
docker compose -p localai up -d ollama-gpu

# Update OpenClaw to latest version
# Edit docker-compose.yml and change:
# image: ghcr.io/openclaw/openclaw:2026.2.4
docker compose -p localai up -d openclaw
```

---

## Rollback Procedures

### Rolling Back Code Changes

```bash
cd /home/phil/local-ai-packaged

# View recent commits
git log --oneline -10

# Rollback to a specific commit (creates new commit)
git revert COMMIT_HASH

# Or reset to a previous commit (⚠️ loses changes)
git reset --hard COMMIT_HASH

# Restart services
python3 start_services.py --profile gpu-nvidia --environment public
```

### Rolling Back Docker Images

```bash
# List image history
docker images | grep openclaw

# Use a specific version
# Edit docker-compose.yml and specify the old version:
# image: ghcr.io/openclaw/openclaw:2026.2.2

# Restart with old version
docker compose -p localai up -d openclaw
```

### Restoring from Backup

```bash
# Stop services
docker compose -p localai down

# Restore configuration
cd /home/phil/local-ai-packaged
tar -xzf ~/backups/2026-02-05/config.tar.gz

# Restore database
gunzip < ~/backups/2026-02-05/supabase.sql.gz | docker exec -i db psql -U postgres

# Restore n8n data
docker run --rm \
  -v localai_n8n_storage:/data \
  -v ~/backups/2026-02-05:/backup \
  alpine sh -c "cd /data && tar -xzf /backup/n8n.tar.gz"

# Restart services
python3 start_services.py --profile gpu-nvidia --environment public
```

---

## Disk Space Management

### Cleaning Docker Resources

```bash
# Remove unused containers, networks, images
docker system prune -a

# Remove unused volumes (⚠️ be careful!)
docker volume prune

# Remove specific stopped container
docker rm container-name

# Remove specific image
docker rmi image-name
```

### Cleaning Logs

```bash
# Limit Docker log sizes (add to docker-compose.yml)
logging:
  driver: "json-file"
  options:
    max-size: "10m"
    max-file: "3"

# Manually clean logs
truncate -s 0 /var/lib/docker/containers/*/*-json.log
```

### Finding Large Files

```bash
# Find files larger than 1GB
find /home/phil -type f -size +1G -exec ls -lh {} \;

# Check Docker directory size
sudo du -sh /var/lib/docker

# Check volume sizes
docker system df -v
```

---

## Security Best Practices

### Firewall Configuration

```bash
# Enable firewall
sudo ufw enable

# Allow only necessary ports
sudo ufw allow 80/tcp    # HTTP
sudo ufw allow 443/tcp   # HTTPS
sudo ufw allow 22/tcp    # SSH

# Check firewall status
sudo ufw status
```

### Securing Environment Variables

```bash
# Set proper permissions on .env
chmod 600 /home/phil/local-ai-packaged/.env

# Never commit .env to Git
# Make sure .env is in .gitignore
grep -q "^\.env$" .gitignore || echo ".env" >> .gitignore
```

### Regular Updates

```bash
# Update system packages
sudo apt update && sudo apt upgrade -y

# Update Docker
sudo apt install docker-ce docker-ce-cli containerd.io

# Reboot if kernel was updated
sudo reboot
```

### Monitoring Failed Login Attempts

```bash
# Check auth logs
sudo tail -f /var/log/auth.log

# Install fail2ban for automatic blocking
sudo apt install fail2ban
sudo systemctl enable fail2ban
sudo systemctl start fail2ban
```

---

## Troubleshooting

### Container Won't Start

```bash
# Check logs
docker logs container-name

# Check if port is already in use
sudo netstat -tulpn | grep :PORT

# Remove and recreate container
docker compose -p localai up -d --force-recreate container-name
```

### Out of Disk Space

```bash
# Check disk usage
df -h

# Clean Docker
docker system prune -a --volumes

# Remove old backups
rm -rf ~/backups/old-date

# Check large files
du -sh /home/phil/* | sort -h
```

### Service Not Accessible

```bash
# Check if container is running
docker ps | grep service-name

# Check container logs
docker logs service-name

# Check Caddy logs
docker logs caddy

# Test port locally
curl http://localhost:PORT

# Check firewall
sudo ufw status
```

### Database Connection Issues

```bash
# Check if database is running
docker ps | grep db

# Check database logs
docker logs db

# Test connection
docker exec -it db psql -U postgres

# Restart database
docker restart db
```

### High Memory Usage

```bash
# Check which container is using memory
docker stats --no-stream

# Restart heavy containers
docker restart container-name

# Adjust memory limits in docker-compose.yml
deploy:
  resources:
    limits:
      memory: 2G
```

---

## Quick Reference Commands

| Task | Command |
|------|---------|
| Start all services | `python3 start_services.py --profile gpu-nvidia --environment public` |
| Stop all services | `docker compose -p localai down` |
| View logs | `docker compose -p localai logs -f` |
| Check status | `docker compose -p localai ps` |
| Backup configs | `tar -czf backup.tar.gz .env docker-compose.yml Caddyfile` |
| Update images | `docker compose -p localai pull && docker compose -p localai up -d` |
| Clean Docker | `docker system prune -a` |
| Check disk space | `docker system df` |
| Restart service | `docker restart container-name` |

---

## Emergency Contacts & Resources

- **Local AI Community**: https://thinktank.ottomator.ai/c/local-ai/18
- **GitHub Issues**: https://github.com/jeanhackpy/local-ai-packaged/issues
- **Docker Documentation**: https://docs.docker.com/
- **Your Git Workflow Guide**: [GIT_WORKFLOW.md](./GIT_WORKFLOW.md)
