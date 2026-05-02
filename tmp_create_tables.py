#!/usr/bin/env python3
import psycopg2, os
from dotenv import load_dotenv

load_dotenv("/home/phil/palanthai/config/.env")
conn = psycopg2.connect(os.environ["VPS_PG_URL"])
cur = conn.cursor()

for sql in [
    """CREATE TABLE IF NOT EXISTS project_floor_plans (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        project_id UUID NOT NULL REFERENCES projects(id) ON DELETE CASCADE,
        floor_plan_url TEXT NOT NULL,
        label TEXT,
        position INTEGER DEFAULT 0,
        source TEXT DEFAULT 'livephuket',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )""",
    """CREATE TABLE IF NOT EXISTS unit_floor_plans (
        id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
        unit_id UUID NOT NULL REFERENCES units(id) ON DELETE CASCADE,
        floor_plan_url TEXT NOT NULL,
        label TEXT,
        position INTEGER DEFAULT 0,
        source TEXT DEFAULT 'livephuket',
        created_at TIMESTAMPTZ NOT NULL DEFAULT now()
    )""",
    "CREATE INDEX IF NOT EXISTS idx_project_floor_plans_project_id ON project_floor_plans(project_id)",
    "CREATE INDEX IF NOT EXISTS idx_unit_floor_plans_unit_id ON unit_floor_plans(unit_id)",
]:
    cur.execute(sql)

conn.commit()

for t in ["projects","project_images","project_floor_plans","units","unit_images","unit_floor_plans"]:
    cur.execute("SELECT count(*) FROM " + t)
    print(t + ": " + str(cur.fetchone()[0]) + " rows")

conn.close()
print("DONE")