---
type: migration_runbook_addendum
tags: [vps, migration, oracle-cloud, learnings, secrets, cleanup, critical]
created: 2026-06-05
status: active
supersedes: extends MIGRATION_RUNBOOK_2026-06-01.md
---

# 📚 Migration Runbook — Learnings Addendum (2026-06-05)

> **Supersedes section §2, §3, §6.3 of [[MIGRATION_RUNBOOK_2026-06-01]] with hard-won lessons from the 2026-06-05 pre-migration dry-run.**
> See also: [[oracle/00_README]] for the Terraform + post-provisioning script.

---

## 🆕 §0 — Pre-Flight Checklist (NEW, run BEFORE anything else)

When the old VPS is at high disk usage (>= 80%), the standard runbook will fail. **This section must run first.**

```bash
# 0.1 — Verify disk state
ssh phil@31.97.67.145 'df -h /'

# 0.2 — If disk >= 90%, run the GENTLE cleanup (NOT vps-cleanup.sh — too aggressive)
ssh phil@31.97.67.145 'docker image prune -f'   # Frees ~5 GB (orphan images)
ssh phil@31.97.67.145 'cd /home/phil/palanthai/phase1_extraction/backups/db && \
  ls -t *.dump | tail -n +8 | xargs -r rm -v'  # Keep 7d local (B2 has full 30d)
ssh phil@31.97.67.145 'df -h /'  # Confirm >15 GB free
```

**Do NOT use `vps-cleanup.sh`** — it does `rm -rf ~/.cache/*` which breaks Ollama, Playwright, and pip caches.

---

## 🆕 §2.0 — Push obsidian-leon first (data loss risk)

`obsidian-leon` has an **auto-sync cron** that commits every 2 minutes but doesn't push. Before any migration, **19+ unpushed commits** will accumulate and be lost if the VPS dies first.

```bash
ssh phil@31.97.67.145 'cd /home/phil/obsidian-leon && git push origin main'
# Run this early. Re-check after a few hours.
```

**Better fix (post-migration todo):** add a `git push` to the auto-sync script itself.

---

## 🆕 §2.5 — Tier 1 backup inventory (PROVEN order from 2026-06-05)

This is the exact order that worked. **Skip any step and you'll waste time debugging.**

```bash
mkdir -p ~/migration-2026-06-05 && cd ~/migration-2026-06-05

# Tier 1A — Secrets (always first, smallest)
scp phil@31.97.67.145:/home/phil/local-ai-packaged/.env ./secrets/local-ai.env
scp phil@31.97.67.145:/home/phil/palanthai/config/.env ./secrets/palanthai.env
scp phil@31.97.67.145:/home/phil/palanthai/config/google_service_account.json ./secrets/
scp phil@31.97.67.145:/home/phil/.config/rclone/rclone.conf ./secrets/

# Tier 1B — Hermes state (2.7 GB, has live API keys in config.yaml)
rsync -avz --progress --exclude='*.lock' --exclude='*.pid' \
  --exclude='__pycache__' --exclude='logs/' \
  phil@31.97.67.145:/home/phil/.hermes/ \
  ./hermes/

# Tier 1C — Palanthai extracted data (the actual moisson)
rsync -avz --progress \
  phil@31.97.67.145:/home/phil/palanthai/phase1_extraction/backups/extracted/ \
  ./extracted/

# Tier 1D — n8n workflow JSON exports (gitignored, but small)
scp -r phil@31.97.67.145:/home/phil/local-ai-packaged/n8n/backup ./n8n-backup/

# Tier 1E — DB dumps (VPS local copies)
rsync -avz --progress \
  phil@31.97.67.145:/home/phil/palanthai/phase1_extraction/backups/db/ \
  ./db-dumps/
```

Total: **~7.7 GB** on Mac. Adjust `~/migration-2026-06-05` if you want a different name.

---

## 🆕 §2.6 — rclone on Mac + B2 paranoia backup

```bash
brew install rclone
mkdir -p ~/.config/rclone
cp ~/migration-2026-06-05/secrets/rclone.conf ~/.config/rclone/rclone.conf
chmod 600 ~/.config/rclone/rclone.conf
rclone lsd b2-palanthai:
rclone copy b2-palanthai:palanthai-backups/db/ ~/migration-2026-06-05/b2-db-dumps/ --progress
# 15 dumps, ~4.6 GB, takes ~2 min on 50 Mbps
```

---

## 🚨 §SECRETS — 3 API keys to rotate IMMEDIATELY (independent of migration)

These were observed in cleartext during the 2026-06-05 audit (visible in shell history and config files):

| Secret | Location | Action |
|---|---|---|
| **Backblaze B2** `0035d8a63a2ce193f09f960a36ea91262c35afb787` | `~/.config/rclone/rclone.conf` | Backblaze B2 → App Keys → **rotate** |
| **NVIDIA** `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` | `~/.hermes/config.yaml` | build.nvidia.com → **regenerate** |
| **OpenRouter** `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` | `~/.hermes/config.yaml` | openrouter.ai → **regenerate** |

The B2 key was already flagged in [[VPS_Security_Audit_2026-05-01]]. The 2 Hermes keys are **NEW findings** — add to that audit.

After rotation, update:
- `local-ai-packaged/.env` (B2: `B2_APPLICATION_KEY`)
- `palanthai/config/.env` (B2: same)
- `~/.hermes/config.yaml` (NVIDIA, OpenRouter)
- `~/.config/rclone/rclone.conf` (B2)
- And re-run `oracle_post_provisioning.sh` to propagate to the new VPS.

---

## 🆕 §3.0 — Oracle Cloud provisioning: the REAL playbook

The original §3 covered theory. Here's what actually works in practice (validated 2026-06-05).

### §3.0.1 — Capacity hunting

`oci_hunter.sh` is the proven strategy. It runs on your Mac, polls every 2 min, and creates a 1 OCPU instance first (easier to land) then upgrades to 4 OCPU.

```bash
# Already running (PID 68377 as of 2026-06-05 13:49)
/Users/phil/Scripts/oci_hunter.sh
tail -f /tmp/oci_out.json  # or check macOS notifications
```

**If AD-1 stays full after 24h**, edit `oci_hunter.sh` line 10 to:
- `AD_NAME="JCSA:AP-SINGAPORE-1-AD-2"`  or
- `AD_NAME="JCSA:AP-SINGAPORE-1-AD-3"`

### §3.0.2 — After instance is up: Terraform + post-provisioning

**Don't run `terraform apply` for the first instance** — capacity is full. Use Terraform only AFTER oci_hunter succeeds, to make it reproducible.

```bash
# Once oci_hunter succeeds, you have an instance OCID + public IP

# A) Import to Terraform (state ownership)
cd /Users/phil/Documents/Factory/COMMAND&CONTROL/10_Infrastructure/VPS_Hostinger/oracle
cp terraform.tfvars.example terraform.tfvars
# Edit terraform.tfvars → tenancy_ocid
export TF_VAR_tenancy_ocid="ocid1.tenancy.oc1..aaa..."
terraform init
terraform import oci_core_instance.palanthai <INSTANCE_OCID>
terraform output

# B) Run post-provisioning (does the rest)
bash oracle_post_provisioning.sh <PUBLIC_IP>
```

The script handles: user creation, packages, Tailscale, UFW, fail2ban, repo clones, secrets restore, DB restore, Docker stack start.

---

## 🆕 §3.1 — 5 Oracle Cloud pitfalls (NEW)

Documented after reading 6h of oci_hunter logs + OCI docs:

1. **"Out of host capacity"** — handled by oci_hunter. Don't give up after 1h.
2. **Boot volume default = 47 GB** (NOT 200) — Terraform spec is correct (`boot_volume_size_in_gbs = 200`). Console users must resize after launch.
3. **`ubuntu` user is NOT sudo by default** on Oracle's Ubuntu images. The `oracle_post_provisioning.sh` script fixes this in step 1.
4. **2 firewalls** (VCN Security List + UFW). Both need configuration. Terraform handles VCN. Script handles UFW.
5. **Reserved Public IP ≠ Ephemeral** — Terraform `assign_public_ip = true` gives a Reserved IP (free, stable). Ephemeral IPs change on reboot.

---

## 🆕 §6.3.1 — Hermes specifics (UPDATE)

Hermes state is **2.7 GB** (not negligible). Critical findings:

- `~/.hermes/config.yaml` contains **plaintext API keys** (NVIDIA, OpenRouter). **ROTATE THESE.**
- `~/.hermes/state.db` (44 MB) — sessions/memories. Must be restored for Hermes to remember context.
- `~/.hermes/hermes-agent/` (2.2 GB) — the agent code + plugins. Mostly re-installable, but plugins need restoring.
- The state-snapshots/ (47 MB) — automatic snapshots, useful as a rollback.

**Decision (confirmed 2026-06-05):** restore everything via rsync, then rebuild the Python venv manually on the new VPS.

```bash
# On the new VPS, after rsync restore
cd ~/.hermes && python3 -m venv venv
source venv/bin/activate
pip install -r hermes-agent/requirements.txt
nohup venv/bin/python3 hermes-agent/hermes_cli/main.py gateway run --replace &
```

---

## ✅ §13 — Post-migration verification checklist (NEW)

Once `oracle_post_provisioning.sh` finishes, verify in this order:

- [ ] SSH: `ssh phil@<ORACLE_IP>` (no password, key-based)
- [ ] Docker: `docker ps` — all 19 containers Up
- [ ] Caddy TLS: `docker logs caddy | grep "obtained certificate"` — all 3 hostnames
- [ ] n8n: `curl -I https://n8n.recall-agency.com` — 200 OK
- [ ] Supabase: `curl -I https://supabase.recall-agency.com` — 200 OK
- [ ] PG row counts: `docker exec supabase-db psql -U postgres -d postgres -c "SELECT count(*) FROM replica_unit"` → ~53 301
- [ ] Qdrant: starts EMPTY (rebuild from PG, as planned)
- [ ] Neo4j: starts EMPTY (rebuild from PG, as planned)
- [ ] Hermes: `curl -I http://100.x.x.x:9119` (Tailscale IP) — 200 OK
- [ ] Palanthai API: `curl -s http://<ORACLE_IP>:8765/health` — `{"status":"healthy"}`
- [ ] B2 backup cron: `crontab -l | grep backup_db` and check `/home/phil/palanthai/phase1_extraction/backups/logs/backup.log`
- [ ] Tailscale: `tailscale status` — connected
- [ ] Fail2ban: `sudo fail2ban-client status sshd` — 1 jail active

---

## 📂 §14 — Related artifacts (NEW)

| Artifact | Path |
|---|---|
| Terraform (VCN + compute) | `oracle/provider.tf`, `variables.tf`, `vcn.tf`, `compute.tf`, `outputs.tf` |
| Terraform template | `oracle/terraform.tfvars.example` |
| Post-provisioning script | `oracle/oracle_post_provisioning.sh` |
| oci_hunter script | `/Users/phil/Scripts/oci_hunter.sh` (on Mac) |
| Migration data | `~/migration-2026-06-05/` (on Mac, 7.7 GB) |
| Original runbook | [[MIGRATION_RUNBOOK_2026-06-01]] (superseded by this file) |

---

*Learnings addendum 2026-06-05 | Created after first successful pre-migration dry-run. Use as the authoritative source going forward.*
