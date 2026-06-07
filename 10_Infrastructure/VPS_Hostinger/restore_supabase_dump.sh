#!/usr/bin/env bash
# restore_supabase_dump.sh <path-to-dump>
# ------------------------------------------------------------------------------
# One-time restore of a Supabase pg_dump (-Fc custom format) into the running
# stack. Restores DB-only with the app services stopped to avoid schema
# conflicts, from INSIDE the pg15 container (client matches the dump's pg 15.8).
#
# This script lives in 10_Infrastructure (not in the app repo). It targets the
# deployed repo via REPO_DIR (default: ~/local-ai-packaged on the VPS).
#
# Prereqs:
#   - $REPO_DIR/.env present with the OLD JWT_SECRET / ANON_KEY / SERVICE_ROLE_KEY
#     (the dump pins the old app.settings.jwt_secret — mismatched keys break Kong)
#   - stack initialised at least once (so volumes/ + roles exist)
#
# Usage (on the VPS):
#   bash restore_supabase_dump.sh ~/migration-2026-06-05/b2-db-dumps/palanthai_20260605_122924.dump
#   REPO_DIR=/home/phil/local-ai-packaged bash restore_supabase_dump.sh <dump>
# ------------------------------------------------------------------------------
set -euo pipefail

DUMP="${1:?usage: restore_supabase_dump.sh <path-to-dump>}"
REPO_DIR="${REPO_DIR:-$HOME/local-ai-packaged}"
PROJECT="${PROJECT:-localai}"
DB_CONTAINER="${DB_CONTAINER:-supabase-db}"
EXPECT_TABLE="${EXPECT_TABLE:-replica_unit}"   # sanity-check table

[[ -f "$DUMP" ]] || { echo "Dump not found: $DUMP"; exit 1; }
[[ -d "$REPO_DIR" ]] || { echo "REPO_DIR not found: $REPO_DIR (set REPO_DIR=...)"; exit 1; }
[[ -f "$REPO_DIR/.env" ]] || { echo ".env missing in $REPO_DIR — restore secrets first."; exit 1; }

# shellcheck disable=SC1090
set -a; source "$REPO_DIR/.env"; set +a
: "${POSTGRES_PASSWORD:?POSTGRES_PASSWORD not set in .env}"

echo "==> Bringing up database only (app services stopped)…"
docker compose -p "$PROJECT" -f "$REPO_DIR/docker-compose.yml" down >/dev/null 2>&1 || true
docker compose -p "$PROJECT" -f "$REPO_DIR/supabase/docker/docker-compose.yml" up -d db

echo "==> Waiting for Postgres…"
for i in $(seq 1 30); do
  if docker exec "$DB_CONTAINER" pg_isready -U postgres >/dev/null 2>&1; then break; fi
  sleep 2; [[ $i -eq 30 ]] && { echo "Postgres did not become ready."; exit 1; }
done
echo "    ready."

echo "==> Copying dump into container…"
docker cp "$DUMP" "$DB_CONTAINER:/tmp/restore.dump"

echo "==> Restoring (owner-safe, idempotent)… this can take several minutes."
# --no-owner: source ownership references roles that may not exist 1:1
# --clean --if-exists: drop/recreate objects so the dump's state wins (rerunnable)
docker exec -e PGPASSWORD="$POSTGRES_PASSWORD" "$DB_CONTAINER" \
  pg_restore --no-owner --clean --if-exists -U postgres -d postgres /tmp/restore.dump \
  || echo "    (pg_restore reported non-fatal errors — review above; usually missing-role GRANTs)"

echo "==> Verifying…"
docker exec "$DB_CONTAINER" psql -U postgres -d postgres -At \
  -c "SELECT 'rows in $EXPECT_TABLE: ' || count(*) FROM $EXPECT_TABLE;" \
  2>/dev/null || echo "    (could not count $EXPECT_TABLE — check schema name)"

echo "==> Cleaning up dump inside container…"
docker exec "$DB_CONTAINER" rm -f /tmp/restore.dump

cat <<EOF

Restore finished. Now bring the full stack back up (from $REPO_DIR):

  cd $REPO_DIR && python3 start_services.py --profile cpu --environment public

Then verify Kong/Supabase respond and Qdrant/Neo4j rebuild from Postgres.
EOF
