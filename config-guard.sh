#!/usr/bin/env bash
# config-guard.sh — Palanthai infra config protection
# Guards Caddyfile, docker-compose files, and kong.yml against accidental edits.
#
# Usage:
#   config-guard.sh check       — verify configs match golden checksums
#   config-guard.sh lock        — store current state as golden baseline
#   config-guard.sh diff        — show what changed vs golden
#   config-guard.sh restore     — restore files from golden backup
#   config-guard.sh status      — one-line per file

set -euo pipefail

BASE="/home/phil/local-ai-packaged"
GOLDEN_DIR="$BASE/.golden"
GOLDEN_BACKUP="$GOLDEN_DIR/backups"
CHECKSUMS="$GOLDEN_DIR/checksums.sha256"

PROTECTED=(
  "Caddyfile"
  "docker-compose.yml"
  "docker-compose.override.public.yml"
  "docker-compose.override.public.supabase.yml"
  "supabase/docker/volumes/api/kong.yml"
)

RED='\033[0;31m'; GREEN='\033[0;32m'; YELLOW='\033[1;33m'; BLUE='\033[0;34m'; NC='\033[0m'

cmd="${1:-status}"

case "$cmd" in
  lock)
    mkdir -p "$GOLDEN_BACKUP"
    : > "$CHECKSUMS"
    echo -e "${BLUE}Locking golden config $(date -u +%Y-%m-%dT%H:%M:%SZ)${NC}"
    for f in "${PROTECTED[@]}"; do
      fp="$BASE/$f"
      if [[ -f "$fp" ]]; then
        sha256sum "$fp" >> "$CHECKSUMS"
        cp "$fp" "$GOLDEN_BACKUP/$(basename "$f").golden"
        echo -e "  ${GREEN}✓ locked${NC} $f"
      else
        echo -e "  ${YELLOW}SKIP${NC}   $f (not found)"
      fi
    done
    cd "$BASE" && git add "$GOLDEN_DIR" 2>/dev/null && git commit -m "chore(config-guard): golden baseline $(date -u +%Y-%m-%d)" --allow-empty 2>/dev/null || true
    echo -e "${GREEN}Done.${NC}"
    ;;

  check)
    if [[ ! -f "$CHECKSUMS" ]]; then echo -e "${YELLOW}No golden baseline. Run: config-guard.sh lock${NC}"; exit 1; fi
    FAIL=0
    while IFS=' ' read -r expected fp; do
      [[ -z "$fp" ]] && continue
      if [[ -f "$fp" ]]; then
        actual=$(sha256sum "$fp" | awk '{print $1}')
        [[ "$expected" == "$actual" ]] && echo -e "  ${GREEN}✓${NC} $(basename "$fp")" || { echo -e "  ${RED}✗ MODIFIED${NC} $(basename "$fp")"; FAIL=1; }
      else echo -e "  ${RED}✗ MISSING${NC} $fp"; FAIL=1; fi
    done < "$CHECKSUMS"
    [[ $FAIL -eq 0 ]] && echo -e "${GREEN}All configs match golden.${NC}" || { echo -e "${RED}Drift detected! Run: config-guard.sh diff${NC}"; exit 1; }
    ;;

  diff)
    for f in "${PROTECTED[@]}"; do
      golden="$GOLDEN_BACKUP/$(basename "$f").golden"; current="$BASE/$f"
      if [[ -f "$golden" && -f "$current" ]]; then
        diff -q "$golden" "$current" > /dev/null 2>&1 || { echo -e "${RED}CHANGED: $f${NC}"; diff "$golden" "$current" || true; echo; }
      fi
    done
    ;;

  restore)
    echo -e "${YELLOW}Restoring from golden backup...${NC}"
    for f in "${PROTECTED[@]}"; do
      golden="$GOLDEN_BACKUP/$(basename "$f").golden"; current="$BASE/$f"
      [[ -f "$golden" ]] && { cp "$golden" "$current"; echo -e "  ${GREEN}✓${NC} $f"; } || echo -e "  ${YELLOW}SKIP${NC} $f"
    done
    echo -e "Reload: ${BLUE}docker exec caddy caddy reload --config /etc/caddy/Caddyfile${NC}"
    ;;

  status|*)
    if [[ ! -f "$CHECKSUMS" ]]; then echo -e "${YELLOW}No baseline. Run: config-guard.sh lock${NC}"; exit 0; fi
    while IFS=' ' read -r expected fp; do
      [[ -z "$fp" ]] && continue
      [[ -f "$fp" ]] && { actual=$(sha256sum "$fp" | awk '{print $1}'); [[ "$expected" == "$actual" ]] && echo -e "  ${GREEN}✓ OK${NC}     $(basename "$fp")" || echo -e "  ${RED}✗ CHANGED${NC} $(basename "$fp")"; } || echo -e "  ${RED}✗ MISSING${NC} $(basename "$fp")"
    done < "$CHECKSUMS"
    ;;
esac
