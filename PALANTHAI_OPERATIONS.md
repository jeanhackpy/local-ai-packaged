# Phase1 - Palanthai Operations Guide

## VPS Access
```
ssh phil@31.97.67.145
cd /home/phil/palanthai/phase1-project-directory
```

## Database Credentials
Source: `/home/phil/palanthai/config/.env`
```bash
VPS_PG_URL=postgresql://postgres.9d1cadcd-481f-4cbe-acc0-aa6ded64064f:xpKe3z1z8q5d1QKjx1ZZzRRgFtQlUe3K@localhost:6543/postgres
```

## 6 Core Tables (clean, empty)
| Table | Purpose | Rows |
|-------|---------|------|
| `projects` | Project metadata | 0 |
| `project_images` | Project gallery images | 0 |
| `project_floor_plans` | Project floor plans | 0 |
| `units` | Unit listings | 0 |
| `unit_images` | Unit gallery images | 0 |
| `unit_floor_plans` | Unit floor plans | 0 |

## Quick Commands

### Check table row counts
```bash
/home/phil/venv/bin/python -c "
import psycopg2, os
from dotenv import load_dotenv
load_dotenv('/home/phil/palanthai/config/.env')
conn = psycopg2.connect(os.environ['VPS_PG_URL'])
cur = conn.cursor()
for t in ['projects','project_images','project_floor_plans','units','unit_images','unit_floor_plans']:
    cur.execute('SELECT count(*) FROM ' + t)
    print(t + ': ' + str(cur.fetchone()[0]))
conn.close()
"
```

### Check running processes (no zombies)
```bash
ps aux | grep -E 'playwright|crawl4ai|chromium' | grep -v grep | wc -l
# Should return 0
```

### Kill any zombie processes
```bash
ps aux | grep -E 'playwright|crawl4ai|chromium' | grep -v grep | awk '{print $2}' | xargs -r kill -9
```

## Run Full Extraction

```bash
cd /home/phil/palanthai/phase1-project-directory
PHASE5_TEST_MODE=1 /home/phil/venv/bin/python sync_full_run.py \
  --force-all \
  --pages 2 \
  --checkpoint /tmp/fullrun_$(date +%s).jsonl \
  -v
```

## Pause / Resume

**Pause** (between project extractions):
```bash
touch /tmp/sync_PAUSE
```

**Resume**:
```bash
rm /tmp/sync_PAUSE
```

**Check live state**:
```bash
cat /tmp/sync_state.json
```

## Crash Recovery

If run crashes, resume with same checkpoint:
```bash
/home/phil/venv/bin/python sync_full_run.py \
  --resume /tmp/fullrun_XXXXXXXX.jsonl \
  -v
```

Find latest checkpoint:
```bash
ls -lt /tmp/fullrun_*.jsonl | head -3
```

## View Logs (streaming)

```bash
# Real-time log tail
tail -f /tmp/sync_state.json

# Or run with verbose output in screen/tmux
```

## Environment Variables

```bash
export PHASE5_TEST_MODE=1   # routes to clean tables
source /home/phil/palanthai/config/.env
```

## Key Scripts

| Script | Purpose |
|--------|---------|
| `sync_full_run.py` | Main orchestrator - runs full pipeline |
| `sync_count_ping.py` | Count-ping endpoints (fast check for new projects) |
| `sync_new_projects.py` | Deep-extract project details |
| `sync_project_units.py` | Extract units per project |
| `ingestor_v5.py` | DB writer - upsert projects/units |
| `source_crawler.py` | URL discovery from livephuket.com |
| `data_quality_service.py` | Quality scoring |
| `models_parsers_00.py` | Pydantic models + parsers |

## Memory Check (before run)

```bash
free -m | grep Mem
# Need >= 1024 MiB available
```

## Clear checkpoint files
```bash
rm /tmp/sync_PAUSE /tmp/sync_state.json
rm /tmp/fullrun_*.jsonl
```

## Production tables (existing, DO NOT TOUCH)
- `projects_live` (6300 rows)
- `replica_projects_live` (6646 rows)
- `units` (51839 rows)
- `replica_unit` (53301 rows)