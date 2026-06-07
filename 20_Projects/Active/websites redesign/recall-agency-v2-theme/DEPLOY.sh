#!/bin/bash
# ════════════════════════════════════════════════════════════
# REcall Agency — Theme Deploy Script v3
# Deploys child theme to Hostinger shared hosting via SSH/rsync
# Usage: bash DEPLOY.sh [staging|live]
# ════════════════════════════════════════════════════════════

set -e

REMOTE_USER="u965287345"
REMOTE_HOST="92.113.28.34"
REMOTE_PORT="65002"
THEME_DIR="$(dirname "$0")"
THEME_NAME="recall-agency-child-theme"

LIVE_PATH="/home/u965287345/domains/recall-agency.com/public_html/wp-content/themes/$THEME_NAME"
STAGING_PATH="/home/u965287345/domains/staging.recall-agency.com/public_html/wp-content/themes/$THEME_NAME"

TARGET="${1:-staging}"

if [ "$TARGET" = "live" ]; then
  REMOTE_PATH="$LIVE_PATH"
  echo "⚠️  Deploying to LIVE site: recall-agency.com"
else
  REMOTE_PATH="$STAGING_PATH"
  echo "📦 Deploying to STAGING: staging.recall-agency.com"
fi

echo "→ Syncing theme files..."

rsync -avz --progress \
  --exclude="node_modules" \
  --exclude=".DS_Store" \
  --exclude="*.sh" \
  --exclude="docs/" \
  --exclude=".git" \
  -e "ssh -p $REMOTE_PORT" \
  "$THEME_DIR/" \
  "$REMOTE_USER@$REMOTE_HOST:$REMOTE_PATH/"

echo ""
echo "✅ Deploy complete → $TARGET"
echo ""

if [ "$TARGET" = "staging" ]; then
  echo "Next steps:"
  echo "  1. SSH in: ssh -p 65002 $REMOTE_USER@$REMOTE_HOST"
  echo "  2. Create staging subdomain in Hostinger hPanel if not done"
  echo "  3. In WP Admin (staging): Appearance → Themes → Activate 'REcall Agency Child Theme'"
  echo "  4. Add credential in n8n: Credentials → New → HTTP Basic Auth"
  echo "     Name: 'WordPress recall-agency.com'"
  echo "     User: ttnl"
  echo "     Password: [your WP application password]"
  echo ""
  echo "  Workflow ready at: https://n8n.recall-agency.com/workflow/uTRcoXaKKeUjAxdS"
fi
