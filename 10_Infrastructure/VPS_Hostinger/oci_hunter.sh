#!/usr/bin/env bash
# oci_hunter.sh — PHASE 1: land an Always-Free A1.Flex at 1 OCPU / 6 GB.
# ------------------------------------------------------------------------------
# Pure free tier (no PAYG). Grabs the smallest shape that still claims the full
# 200 GB boot volume, so you get a foothold fast. Expansion to 4 OCPU / 24 GB is
# a SEPARATE step once you've landed:  ./oci_resize.sh
#
# Gentle, proven cadence (120-140 s/attempt, 300 s cooldown on 429) — fast enough
# to catch capacity windows, slow enough not to trip OCI throttling.
#
# Run from the Terraform dir (auto-reads subnet) after creating the network:
#   terraform apply -target=oci_core_subnet.palanthai_subnet
#   SUBNET_OCID=$(terraform output -raw subnet_id) ./oci_hunter.sh
#
# Stop with Ctrl-C. Re-runnable: exits early if the instance already exists.
# ------------------------------------------------------------------------------
set -uo pipefail   # NOT -e: we catch launch failures and retry.

# ---------- Config (override via env) ----------
COMPARTMENT_OCID="${COMPARTMENT_OCID:-${TF_VAR_tenancy_ocid:-ocid1.tenancy.oc1..aaaaaaaa47hlmpxbk2jn4gukwtz7mihmkhtiounqjy3ytltfq4dggwmjzsbq}}"
IMAGE_OCID="${IMAGE_OCID:-ocid1.image.oc1.ap-singapore-1.aaaaaaaaihkypxmfxzeyjevj3eutgzlnqjazicn27goya2lpr3mdmg5to2tq}"
SUBNET_OCID="${SUBNET_OCID:-}"        # from `terraform output -raw subnet_id` (regional subnet, AD-agnostic)
SSH_KEY="${SSH_KEY:-$HOME/.ssh/id_ed25519.pub}"
DISPLAY_NAME="${DISPLAY_NAME:-palanthai-oracle}"   # matches the Terraform instance name (clean import)
SHAPE="${SHAPE:-VM.Standard.A1.Flex}"
OCPUS="${OCPUS:-1}"                   # Phase 1: small = easier to land
MEMORY="${MEMORY:-6}"
BOOT_GB="${BOOT_GB:-200}"             # full free disk, claimed now regardless of OCPU
ADS="${ADS:-JCSA:AP-SINGAPORE-1-AD-1 JCSA:AP-SINGAPORE-1-AD-2 JCSA:AP-SINGAPORE-1-AD-3}"
MIN_WAIT="${MIN_WAIT:-120}"           # per-attempt backoff (proven rhythm)
MAX_WAIT="${MAX_WAIT:-140}"
RATE_LIMIT_COOLDOWN="${RATE_LIMIT_COOLDOWN:-300}"   # 429 -> 5 min
LOG="${LOG:-/tmp/oci_hunter.log}"

# ---------- Helpers ----------
ts()  { date -u +%Y-%m-%dT%H:%M:%SZ; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }
alert() {
  command -v osascript >/dev/null 2>&1 && osascript -e "display notification \"$1\" with title \"OCI Hunter\" sound name \"Glass\"" 2>/dev/null || true
  command -v say       >/dev/null 2>&1 && say "$2" 2>/dev/null &
  printf '\a'
}
die() { log "FATAL: $*"; alert "Hunter stopped" "Hunter stopped."; exit 1; }

command -v oci >/dev/null 2>&1 || die "oci CLI not found (brew install oci-cli; oci setup config)"
command -v jq  >/dev/null 2>&1 || die "jq not found (brew install jq)"
[[ -f "$SSH_KEY" ]] || die "SSH public key not found: $SSH_KEY"

# Resolve subnet: env -> terraform output -> fail (must be the CURRENT VCN's subnet).
if [[ -z "$SUBNET_OCID" ]]; then
  SUBNET_OCID="$(terraform output -raw subnet_id 2>/dev/null || true)"
fi
[[ -n "$SUBNET_OCID" ]] || die "no SUBNET_OCID (run: terraform apply -target=oci_core_subnet.palanthai_subnet, then export SUBNET_OCID=\$(terraform output -raw subnet_id))"

# ---------- Duplicate guard (over-quota => Oracle disables ALL your A1) ----------
existing="$(oci compute instance list -c "$COMPARTMENT_OCID" --display-name "$DISPLAY_NAME" \
            --query "data[?\"lifecycle-state\"=='RUNNING' || \"lifecycle-state\"=='PROVISIONING'].id | [0]" \
            --raw-output 2>/dev/null || true)"
if [[ -n "$existing" && "$existing" != "null" ]]; then
  log "Instance '$DISPLAY_NAME' already exists ($existing) — nothing to hunt. Run ./oci_resize.sh to expand."
  exit 0
fi

on_success() {
  local id="$1" ip
  ip="$(oci compute instance list-vnics --instance-id "$id" --query 'data[0]."public-ip"' --raw-output 2>/dev/null || echo '?')"
  log "🎉 LANDED 1 OCPU/6GB: $id  public-ip=$ip"
  alert "Instance landed! $ip" "Bingo. Phase one complete. Instance secured."
  cat <<EOF | tee -a "$LOG"

──────────────────────────────────────────────────────────────
  Instance OCID : $id
  Public IP     : $ip
  Next:
    terraform import oci_core_instance.palanthai $id
    ./oci_resize.sh                       # expand to 4 OCPU / 24 GB
    scp oracle_post_provisioning.sh ubuntu@$ip:~
    ssh ubuntu@$ip 'sudo bash oracle_post_provisioning.sh'
──────────────────────────────────────────────────────────────
EOF
  exit 0
}

# ---------- Hunt loop ----------
log "Phase 1: hunting $SHAPE ${OCPUS}OCPU/${MEMORY}GB/${BOOT_GB}GB-boot"
log "ADs: $ADS | subnet=$SUBNET_OCID | wait=${MIN_WAIT}-${MAX_WAIT}s | log=$LOG"

count=0
while :; do
  for ad in $ADS; do
    count=$((count+1))
    log "Attempt #$count — AD=$ad — launching…"
    out="$(oci compute instance launch \
            --availability-domain "$ad" \
            --compartment-id "$COMPARTMENT_OCID" \
            --shape "$SHAPE" \
            --shape-config "{\"ocpus\": $OCPUS, \"memoryInGBs\": $MEMORY}" \
            --subnet-id "$SUBNET_OCID" \
            --image-id "$IMAGE_OCID" \
            --boot-volume-size-in-gbs "$BOOT_GB" \
            --display-name "$DISPLAY_NAME" \
            --assign-public-ip true \
            --ssh-authorized-keys-file "$SSH_KEY" \
            --no-retry \
            --wait-for-state RUNNING 2>&1)"
    if [[ $? -eq 0 ]]; then
      id="$(echo "$out" | jq -r '.data.id' 2>/dev/null)"
      [[ -z "$id" || "$id" == "null" ]] && id="$(oci compute instance list -c "$COMPARTMENT_OCID" --display-name "$DISPLAY_NAME" --query 'data[0].id' --raw-output 2>/dev/null || true)"
      [[ -n "$id" && "$id" != "null" ]] && on_success "$id"
    fi

    if echo "$out" | grep -qiE 'TooManyRequests|429'; then
      log "  ⚠️  rate limited — cooling down ${RATE_LIMIT_COOLDOWN}s"
      sleep "$RATE_LIMIT_COOLDOWN"
    elif echo "$out" | grep -qiE 'Out of host capacity|InternalError|\(500'; then
      w=$(( (RANDOM % (MAX_WAIT - MIN_WAIT + 1)) + MIN_WAIT ))
      log "  …no capacity on $ad — retry in ${w}s"
      sleep "$w"
    elif echo "$out" | grep -qiE 'LimitExceeded|QuotaExceeded|already exists|NotAuthorized|NotAuthenticated|InvalidParameter|Shape.*not.*support|400|404'; then
      die "$(echo "$out" | grep -iE 'LimitExceeded|QuotaExceeded|already exists|NotAuthorized|NotAuthenticated|InvalidParameter|Shape|400|404' | head -1)"
    else
      w=$(( (RANDOM % (MAX_WAIT - MIN_WAIT + 1)) + MIN_WAIT ))
      log "  …unexpected — retry in ${w}s: $(echo "$out" | head -1)"
      sleep "$w"
    fi
  done
done
