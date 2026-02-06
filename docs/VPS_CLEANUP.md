# VPS Cleanup & Maintenance Script

This script helps you clean up your VPS, fix permission issues, and manage disk space.

## Current VPS Status

- **Disk Usage**: 53GB / 96GB (55% used)
- **Reclaimable Docker Images**: 34.92GB (99% of images are unused!)
- **Largest Directory**: neo4j (519MB)
- **Log Files**: Neo4j debug.log (1.9MB)

## Issues Identified

### 1. OpenClaw Permission Problem
- **Issue**: `openclaw/` directory owned by root (from crawl4ai installation)
- **Impact**: Can't access or modify files
- **Container**: Runs as `node` user, but directory is root-owned

### 2. Docker Image Bloat
- **Issue**: 34.92GB of unused Docker images
- **Impact**: Wasting disk space
- **Solution**: Safe cleanup needed

### 3. Start Script Confusion
- **Issue**: Unclear whether to use `sudo` with `start_services.py`
- **Answer**: **NO SUDO NEEDED** for normal operation

---

## Quick Fixes

### Fix 1: OpenClaw Permissions (RECOMMENDED)

```bash
# Fix ownership of openclaw directory
sudo chown -R phil:phil /home/phil/local-ai-packaged/openclaw

# Verify it worked
ls -la /home/phil/local-ai-packaged/openclaw
```

**Why this works**: The OpenClaw container runs as the `node` user inside the container, but it maps to your user (phil) on the host. The directory should be owned by you, not root.

### Fix 2: Clean Up Docker Images (SAFE)

```bash
# Remove unused Docker images (saves ~35GB!)
docker image prune -a

# When prompted, type 'y' to confirm
```

**This is safe because**:
- Only removes images not used by any container
- Running containers are protected
- You can always re-download images if needed

### Fix 3: Start Services Correctly (NO SUDO)

```bash
# Correct way to start (NO SUDO!)
cd /home/phil/local-ai-packaged
python3 start_services.py --profile cpu --environment public

# For GPU (if you have one)
python3 start_services.py --profile gpu-nvidia --environment public
```

**Why NO sudo**:
- Docker is already configured for your user
- Using sudo can create permission problems
- The script doesn't need root access

---

## Comprehensive Cleanup Script

Save this as `/home/phil/cleanup-vps.sh`:

```bash
#!/bin/bash
# VPS Cleanup Script for local-ai-packaged

echo "=== VPS Cleanup Script ==="
echo ""

# Colors for output
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

# Function to print colored output
print_status() {
    echo -e "${GREEN}[✓]${NC} $1"
}

print_warning() {
    echo -e "${YELLOW}[!]${NC} $1"
}

print_error() {
    echo -e "${RED}[✗]${NC} $1"
}

# Check current disk usage
echo "Current Disk Usage:"
df -h / | grep -v Filesystem
echo ""

# 1. Fix OpenClaw Permissions
echo "=== Step 1: Fixing OpenClaw Permissions ==="
if [ -d "/home/phil/local-ai-packaged/openclaw" ]; then
    print_status "Fixing openclaw directory permissions..."
    sudo chown -R phil:phil /home/phil/local-ai-packaged/openclaw
    print_status "OpenClaw permissions fixed!"
else
    print_warning "OpenClaw directory not found, skipping..."
fi
echo ""

# 2. Clean Docker Images
echo "=== Step 2: Docker Image Cleanup ==="
print_status "Current Docker disk usage:"
docker system df
echo ""

read -p "Remove unused Docker images? This will save ~35GB (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removing unused Docker images..."
    docker image prune -a -f
    print_status "Docker images cleaned!"
else
    print_warning "Skipped Docker image cleanup"
fi
echo ""

# 3. Clean Docker Build Cache
echo "=== Step 3: Docker Build Cache ==="
read -p "Remove Docker build cache? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Removing build cache..."
    docker builder prune -a -f
    print_status "Build cache cleaned!"
else
    print_warning "Skipped build cache cleanup"
fi
echo ""

# 4. Clean Old Logs
echo "=== Step 4: Log File Cleanup ==="
print_status "Finding large log files..."
find /home/phil/local-ai-packaged -name "*.log" -type f -size +10M -exec ls -lh {} \; 2>/dev/null

read -p "Truncate large log files? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Truncating log files larger than 10MB..."
    find /home/phil/local-ai-packaged -name "*.log" -type f -size +10M -exec truncate -s 0 {} \; 2>/dev/null
    print_status "Log files truncated!"
else
    print_warning "Skipped log cleanup"
fi
echo ""

# 5. Clean Docker Logs
echo "=== Step 5: Docker Container Logs ==="
read -p "Truncate Docker container logs? (y/n): " -n 1 -r
echo ""
if [[ $REPLY =~ ^[Yy]$ ]]; then
    print_status "Truncating Docker container logs..."
    sudo truncate -s 0 /var/lib/docker/containers/*/*-json.log 2>/dev/null
    print_status "Docker logs truncated!"
else
    print_warning "Skipped Docker log cleanup"
fi
echo ""

# 6. Summary
echo "=== Cleanup Summary ==="
print_status "New disk usage:"
df -h / | grep -v Filesystem
echo ""
print_status "New Docker disk usage:"
docker system df
echo ""

print_status "Cleanup complete!"
echo ""
echo "Recommendations:"
echo "1. Run this script monthly to keep disk usage low"
echo "2. Monitor disk space with: df -h"
echo "3. Check Docker usage with: docker system df"
echo ""
```

### Make it executable and run:

```bash
# Make executable
chmod +x ~/cleanup-vps.sh

# Run it
./cleanup-vps.sh
```

---

## Automated Log Rotation

To prevent logs from growing too large, add this to your docker-compose.yml for each service:

```yaml
logging:
  driver: "json-file"
  options:
    max-size: "10m"    # Max 10MB per log file
    max-file: "3"      # Keep 3 files (30MB total per container)
```

**Example for OpenClaw**:

```yaml
openclaw:
  image: ghcr.io/openclaw/openclaw:2026.2.2
  # ... other config ...
  logging:
    driver: "json-file"
    options:
      max-size: "10m"
      max-file: "3"
```

---

## Start/Stop Commands Reference

### Starting Services

```bash
# CPU profile (for you!)
python3 start_services.py --profile cpu --environment public

# GPU profile (if you have GPU)
python3 start_services.py --profile gpu-nvidia --environment public

# ❌ WRONG - Don't use sudo!
sudo python3 start_services.py  # This causes permission issues!
```

### Stopping Services

```bash
# Stop all services
docker compose -p localai down

# Stop and remove volumes (⚠️ deletes data!)
docker compose -p localai down -v
```

### Restarting Services

```bash
# Restart all
docker compose -p localai restart

# Restart specific service
docker restart openclaw
```

### Updating Services

```bash
# Stop services
docker compose -p localai -f docker-compose.yml --profile cpu down

# Pull latest images
docker compose -p localai -f docker-compose.yml --profile cpu pull

# Start with new images
python3 start_services.py --profile cpu --environment public
```

---

## Understanding OpenClaw Container Isolation

### Your Question: "Is OpenClaw in the same container or separate?"

**Answer**: OpenClaw runs in its **own separate container**.

**How it works**:

1. **Separate Container**: OpenClaw has its own isolated environment
2. **Shared Docker Socket**: It can create NEW containers via `/var/run/docker.sock`
3. **Volume Mount**: `openclaw/` directory is mounted into the container

**When you installed crawl4ai**:
- OpenClaw created a Python virtual environment INSIDE its container
- The venv was saved to the mounted `openclaw/` directory
- This directory got created with root permissions (bug)
- Now you can't access it without sudo

**The Fix**:
```bash
sudo chown -R phil:phil /home/phil/local-ai-packaged/openclaw
```

This gives you back ownership without breaking OpenClaw's functionality.

---

## Monitoring Disk Usage

### Quick Check

```bash
# Overall disk usage
df -h

# Docker usage
docker system df

# Largest directories
du -sh /home/phil/local-ai-packaged/* | sort -h | tail -10

# Large log files
find /home/phil/local-ai-packaged -name "*.log" -type f -exec du -h {} \; | sort -h | tail -10
```

### Set Up Alerts (Optional)

Add to your crontab to get weekly disk usage reports:

```bash
# Edit crontab
crontab -e

# Add this line (runs every Sunday at 8 AM)
0 8 * * 0 df -h / | mail -s "VPS Disk Usage Report" your-email@example.com
```

---

## Common Issues & Solutions

### Issue: "Permission denied" when accessing openclaw/

```bash
sudo chown -R phil:phil /home/phil/local-ai-packaged/openclaw
```

### Issue: "No space left on device"

```bash
# Clean Docker images
docker image prune -a

# Clean Docker system
docker system prune -a --volumes
```

### Issue: "start_services.py fails with permission error"

```bash
# DON'T use sudo! Instead, add your user to docker group
sudo usermod -aG docker phil

# Log out and back in for changes to take effect
```

### Issue: "Container keeps restarting"

```bash
# Check logs
docker logs container-name

# Check disk space
df -h

# Check memory
free -h
```

---

## Best Practices

> [!IMPORTANT]
> **DO**:
> - ✅ Use `python3 start_services.py` (no sudo)
> - ✅ Run cleanup script monthly
> - ✅ Monitor disk usage weekly
> - ✅ Keep backups before major changes
> - ✅ Use `--profile cpu` for your VPS

> [!WARNING]
> **DON'T**:
> - ❌ Use `sudo` with start_services.py
> - ❌ Delete Docker volumes without backup
> - ❌ Run `docker system prune -a --volumes` without understanding it
> - ❌ Ignore disk space warnings

---

## Quick Reference

| Task | Command |
|------|---------|
| Fix OpenClaw permissions | `sudo chown -R phil:phil openclaw/` |
| Clean Docker images | `docker image prune -a` |
| Start services | `python3 start_services.py --profile cpu --environment public` |
| Stop services | `docker compose -p localai down` |
| Check disk usage | `df -h` |
| Check Docker usage | `docker system df` |
| Run cleanup script | `./cleanup-vps.sh` |
| View container logs | `docker logs container-name` |
