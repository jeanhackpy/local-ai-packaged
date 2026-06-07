#!/usr/bin/env bash
# oracle_post_provisioning.sh
# ------------------------------------------------------------------------------
# Idempotent first-boot provisioning for the Palanthai single fat node on
# Oracle Cloud Always Free (A1.Flex 4 OCPU / 24 GB / 200 GB, Ubuntu 24.04).
#
# Copy this ONE file to the fresh VM and run it; it clones the rest:
#   scp oracle_post_provisioning.sh ubuntu@<IP>:~   &&   ssh ubuntu@<IP>
#   sudo bash oracle_post_provisioning.sh
#
# Safe to re-run. Each step is guarded. Nothing destructive by default.
# ------------------------------------------------------------------------------
set -euo pipefail

# ---- Config (override via env) ----
APP_USER="${APP_USER:-$(logname 2>/dev/null || echo ubuntu)}"
APP_HOME="$(getent passwd "$APP_USER" | cut -d: -f6)"
REPO_URL="${REPO_URL:-https://github.com/jeanhackpy/local-ai-packaged.git}"
REPO_DIR="${REPO_DIR:-$APP_HOME/local-ai-packaged}"
SWAP_GB="${SWAP_GB:-4}"
TS_AUTHKEY="${TS_AUTHKEY:-}"          # optional Tailscale auth key (tskey-...)
LOCK_SSH_TO_TAILSCALE="${LOCK_SSH_TO_TAILSCALE:-0}"  # 1 = close public :22 (needs TS up)

log() { echo -e "\033[0;34m[provision]\033[0m $*"; }
ok()  { echo -e "  \033[0;32m✓\033[0m $*"; }
warn(){ echo -e "  \033[1;33m!\033[0m $*"; }
[[ $EUID -eq 0 ]] || { echo "Run with sudo/root."; exit 1; }

# ---- 1. Base packages ----
log "System packages"
export DEBIAN_FRONTEND=noninteractive
apt-get update -qq
apt-get install -y -qq ca-certificates curl git jq ufw fail2ban unattended-upgrades python3 rsync >/dev/null
ok "base packages"

# ---- 2. Swap (ARM images ship none -> OOM protection) ----
log "Swap (${SWAP_GB}G)"
if ! swapon --show | grep -q '/swapfile'; then
  fallocate -l "${SWAP_GB}G" /swapfile || dd if=/dev/zero of=/swapfile bs=1M count=$((SWAP_GB*1024))
  chmod 600 /swapfile && mkswap /swapfile >/dev/null && swapon /swapfile
  grep -q '/swapfile' /etc/fstab || echo '/swapfile none swap sw 0 0' >> /etc/fstab
  ok "swapfile created"
else ok "swap already present"; fi
sysctl -qw vm.swappiness=10
grep -q 'vm.swappiness' /etc/sysctl.conf || echo 'vm.swappiness=10' >> /etc/sysctl.conf

# ---- 3. Docker (skip if cloud-init already installed docker.io) ----
log "Docker engine"
if ! command -v docker >/dev/null 2>&1; then
  curl -fsSL https://get.docker.com | sh >/dev/null
  ok "docker installed"
else ok "docker already present ($(docker --version))"; fi
# Global log rotation — stops a chatty container filling the 200 GB disk.
install -d /etc/docker
if [[ ! -f /etc/docker/daemon.json ]]; then
  cat > /etc/docker/daemon.json <<'JSON'
{
  "log-driver": "json-file",
  "log-opts": { "max-size": "10m", "max-file": "3" },
  "live-restore": true
}
JSON
  systemctl restart docker
  ok "daemon.json log rotation"
else warn "daemon.json exists — left untouched (ensure log-opts set)"; fi
systemctl enable --now docker >/dev/null 2>&1 || true
usermod -aG docker "$APP_USER" || true
# docker compose plugin
docker compose version >/dev/null 2>&1 || apt-get install -y -qq docker-compose-plugin >/dev/null || true

# ---- 4. Tailscale (admin backplane) ----
log "Tailscale"
if ! command -v tailscale >/dev/null 2>&1; then
  curl -fsSL https://tailscale.com/install.sh | sh >/dev/null
fi
if [[ -n "$TS_AUTHKEY" ]]; then
  tailscale up --authkey "$TS_AUTHKEY" --ssh || warn "tailscale up failed — run manually"
  ok "tailscale up"
else warn "no TS_AUTHKEY — run 'tailscale up' manually before locking SSH"; fi

# ---- 5. Firewall (host-level defense in depth; OCI Security List is the real one) ----
log "UFW + fail2ban"
ufw allow 80/tcp  >/dev/null
ufw allow 443/tcp >/dev/null
if [[ "$LOCK_SSH_TO_TAILSCALE" == "1" ]] && tailscale status >/dev/null 2>&1; then
  ufw allow from 100.64.0.0/10 to any port 22 proto tcp >/dev/null
  ufw delete allow OpenSSH >/dev/null 2>&1 || true
  ufw delete allow 22/tcp  >/dev/null 2>&1 || true
  ok "SSH restricted to Tailscale (100.64.0.0/10)"
else
  ufw allow OpenSSH >/dev/null
  warn "SSH left open to the world (fail2ban guards it). Set LOCK_SSH_TO_TAILSCALE=1 once Tailscale is up."
fi
ufw --force enable >/dev/null
systemctl enable --now fail2ban >/dev/null 2>&1 || true
ok "firewall active"

# ---- 6. Repo ----
log "Repository"
if [[ -d "$REPO_DIR/.git" ]]; then
  sudo -u "$APP_USER" git -C "$REPO_DIR" pull --ff-only || warn "git pull skipped"
  ok "repo updated"
else
  sudo -u "$APP_USER" git clone "$REPO_URL" "$REPO_DIR"
  ok "repo cloned -> $REPO_DIR"
fi

# ---- 7. .env check (secrets must be restored, NOT generated, to match the dump) ----
log "Environment file"
if [[ -f "$REPO_DIR/.env" ]]; then
  ok ".env present"
else
  warn ".env MISSING. Restore it from your backup BEFORE starting the stack:"
  warn "  scp secrets/local-ai.env  $APP_USER@<IP>:$REPO_DIR/.env"
  warn "  (must reuse the OLD JWT_SECRET / ANON_KEY / SERVICE_ROLE_KEY for the dump to work)"
fi

cat <<EOF

──────────────────────────────────────────────────────────────────────
Provisioning done. Next (as $APP_USER, NOT root):

  1. Confirm secrets:   grep -E 'JWT_SECRET|ANON_KEY|SERVICE_ROLE_KEY' $REPO_DIR/.env
  2. First boot:        cd $REPO_DIR && python3 start_services.py --profile cpu --environment public
  3. Restore DB dump:   bash restore_supabase_dump.sh <path-to-dump>
  4. Re-lock golden:    ./config-guard.sh lock
  5. (optional) once Tailscale is up:  sudo LOCK_SSH_TO_TAILSCALE=1 bash oracle_post_provisioning.sh

Reminder: ALWAYS --environment public on this box (default 'private' opens all ports).
──────────────────────────────────────────────────────────────────────
EOF
