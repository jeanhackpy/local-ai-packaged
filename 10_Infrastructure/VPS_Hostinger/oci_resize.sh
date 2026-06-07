#!/usr/bin/env bash
# oci_resize.sh — PHASE 2: expand the landed instance 1 OCPU/6 GB -> 4 OCPU/24 GB.
# ------------------------------------------------------------------------------
# In-place shape_config update (no recreate; the instance reboots). Retries until
# the host has spare Ampere capacity for the extra cores/RAM. Run AFTER oci_hunter
# has landed the instance.
#
#   ./oci_resize.sh                       # auto-finds the instance by name
#   INSTANCE_OCID=ocid1.instance... ./oci_resize.sh
#
# Stop with Ctrl-C. Re-runnable: exits early if already at target size.
# ------------------------------------------------------------------------------
set -uo pipefail

COMPARTMENT_OCID="${COMPARTMENT_OCID:-${TF_VAR_tenancy_ocid:-ocid1.tenancy.oc1..aaaaaaaa47hlmpxbk2jn4gukwtz7mihmkhtiounqjy3ytltfq4dggwmjzsbq}}"
DISPLAY_NAME="${DISPLAY_NAME:-palanthai-oracle}"
INSTANCE_OCID="${INSTANCE_OCID:-}"
TARGET_OCPUS="${TARGET_OCPUS:-4}"
TARGET_MEM="${TARGET_MEM:-24}"
WAIT="${WAIT:-600}"          # 10 min between expansion attempts (gentle)
LOG="${LOG:-/tmp/oci_resize.log}"

ts()  { date -u +%Y-%m-%dT%H:%M:%SZ; }
log() { echo "[$(ts)] $*" | tee -a "$LOG"; }
alert() {
  command -v osascript >/dev/null 2>&1 && osascript -e "display notification \"$1\" with title \"OCI Resize\" sound name \"Glass\"" 2>/dev/null || true
  command -v say       >/dev/null 2>&1 && say "$2" 2>/dev/null &
  printf '\a'
}
die() { log "FATAL: $*"; exit 1; }

command -v oci >/dev/null 2>&1 || die "oci CLI not found"
command -v jq  >/dev/null 2>&1 || die "jq not found"

# Resolve instance by display name if not provided.
if [[ -z "$INSTANCE_OCID" ]]; then
  INSTANCE_OCID="$(oci compute instance list -c "$COMPARTMENT_OCID" --display-name "$DISPLAY_NAME" \
                   --query "data[?\"lifecycle-state\"=='RUNNING'].id | [0]" --raw-output 2>/dev/null || true)"
fi
[[ -n "$INSTANCE_OCID" && "$INSTANCE_OCID" != "null" ]] || die "no RUNNING instance '$DISPLAY_NAME' found — land it first with ./oci_hunter.sh"

# Already at target?
cur="$(oci compute instance get --instance-id "$INSTANCE_OCID" \
       --query 'data."shape-config".{o:ocpus,m:"memory-in-gbs"}' 2>/dev/null || echo '{}')"
co="$(echo "$cur" | jq -r '.o // 0')"; cm="$(echo "$cur" | jq -r '.m // 0')"
if (( ${co%.*} >= TARGET_OCPUS )); then
  log "Already at ${co} OCPU / ${cm} GB — nothing to do."
  exit 0
fi

log "Expanding $INSTANCE_OCID  ${co}->${TARGET_OCPUS} OCPU, ${cm}->${TARGET_MEM} GB (retry every ${WAIT}s)"
n=0
while :; do
  n=$((n+1))
  log "Expansion attempt #$n…"
  out="$(oci compute instance update --instance-id "$INSTANCE_OCID" \
          --shape-config "{\"ocpus\": $TARGET_OCPUS, \"memoryInGBs\": $TARGET_MEM}" \
          --no-retry --force 2>&1)"
  if [[ $? -eq 0 ]]; then
    log "💎 Resized to ${TARGET_OCPUS} OCPU / ${TARGET_MEM} GB."
    alert "Expanded to 4 OCPU / 24 GB" "Maximum power achieved."
    exit 0
  fi
  if echo "$out" | grep -qiE 'TooManyRequests|429'; then
    log "  ⚠️  rate limited — cooling 300s"; sleep 300
  elif echo "$out" | grep -qiE 'Out of host capacity|InternalError|\(500'; then
    log "  …host has no spare capacity — keeping current size, retry in ${WAIT}s"; sleep "$WAIT"
  else
    die "$(echo "$out" | head -1)"
  fi
done
