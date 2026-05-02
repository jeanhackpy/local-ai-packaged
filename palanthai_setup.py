#!/usr/bin/env python3
import psycopg2, os, sys
from pathlib import Path

# Load env
load_dotenv = __import__('dotenv', fromlist=['load_dotenv']).load_dotenv
project_dir = Path('/home/phil/palanthai/phase1-project-directory')
load_dotenv('/home/phil/palanthai/config/.env')

conn = psycopg2.connect(os.environ['VPS_PG_URL'])
cur = conn.cursor()

# Drop existing fullrun tables
for t in ['fullrun_unit_floor_plans','fullrun_unit_images','fullrun_unit',
          'fullrun_project_floor_plans','fullrun_project_images','fullrun_projects_live']:
    cur.execute(f'DROP TABLE IF EXISTS {t} CASCADE')
print('Dropped old tables')

# Create 6 tables with fullrun_ prefix (matching what PHASE5_TEST_MODE=3 expects)
sql = """
CREATE TABLE fullrun_projects_live (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    source_url TEXT NOT NULL,
    name TEXT NOT NULL,
    name_normalized TEXT,
    slug TEXT,
    type TEXT,
    status TEXT,
    total_units INTEGER,
    floors INTEGER,
    completion_year INTEGER,
    country TEXT DEFAULT 'Thailand',
    city TEXT,
    district TEXT,
    province TEXT,
    latitude DOUBLE PRECISION,
    longitude DOUBLE PRECISION,
    address TEXT,
    developer_name TEXT,
    construction_status TEXT,
    price_min_thb NUMERIC,
    price_max_thb NUMERIC,
    rent_price_min NUMERIC,
    rent_price_max NUMERIC,
    ownership_type TEXT,
    amenities TEXT[] DEFAULT '{}',
    nearby_places JSONB DEFAULT '[]',
    faqs JSONB DEFAULT '[]',
    metadata JSONB DEFAULT '{}',
    description TEXT,
    data_quality_score INTEGER DEFAULT 0,
    needs_embedding BOOLEAN NOT NULL DEFAULT true,
    qdrant_synced_at TIMESTAMPTZ,
    neo4j_synced_at TIMESTAMPTZ,
    images JSONB DEFAULT '[]',
    primary_image_url TEXT,
    units_for_sale_url TEXT,
    units_for_rent_url TEXT,
    units_for_sale_count INTEGER DEFAULT 0,
    units_for_rent_count INTEGER DEFAULT 0,
    maintenance_fee_thb NUMERIC,
    common_fee_thb NUMERIC,
    sinking_fund_thb NUMERIC,
    land_area_sqm NUMERIC,
    land_area_rai NUMERIC,
    nearest_landmark TEXT,
    region TEXT,
    extraction_method TEXT,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE fullrun_project_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES fullrun_projects_live(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    position INTEGER DEFAULT 0,
    source TEXT DEFAULT 'livephuket',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE fullrun_project_floor_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID NOT NULL REFERENCES fullrun_projects_live(id) ON DELETE CASCADE,
    floor_plan_url TEXT NOT NULL,
    label TEXT,
    position INTEGER DEFAULT 0,
    source TEXT DEFAULT 'livephuket',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE fullrun_unit (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id UUID REFERENCES fullrun_projects_live(id) ON DELETE SET NULL,
    source_url TEXT,
    unit_id VARCHAR,
    property_type VARCHAR,
    bedrooms NUMERIC,
    bathrooms NUMERIC,
    floor_area_sqm NUMERIC,
    floor_number INTEGER,
    price_thb BIGINT,
    price_per_sqm NUMERIC,
    rental_price_thb INTEGER,
    rental_yield NUMERIC,
    ownership_type VARCHAR,
    furnishing VARCHAR,
    view_type VARCHAR,
    pets VARCHAR,
    unit_type VARCHAR,
    plot_size_sqm NUMERIC,
    district TEXT,
    subdistrict TEXT,
    province TEXT,
    latitude NUMERIC,
    longitude NUMERIC,
    description TEXT,
    features JSONB DEFAULT '[]',
    images JSONB DEFAULT '[]',
    floor_plan_images JSONB DEFAULT '[]',
    cam_fee_thb INTEGER,
    developer_name TEXT,
    construction_status TEXT,
    nearest_landmark TEXT,
    building_name TEXT,
    listed_by VARCHAR,
    listed_date TEXT,
    listing_updated TEXT,
    agent_phone VARCHAR,
    data_source TEXT DEFAULT 'scraped',
    data_quality_score INTEGER DEFAULT 0,
    needs_embedding BOOLEAN NOT NULL DEFAULT true,
    price_previous_thb BIGINT,
    qdrant_synced_at TIMESTAMPTZ,
    neo4j_synced_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE fullrun_unit_images (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id UUID NOT NULL REFERENCES fullrun_unit(id) ON DELETE CASCADE,
    image_url TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT false,
    position INTEGER DEFAULT 0,
    source TEXT DEFAULT 'livephuket',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);

CREATE TABLE fullrun_unit_floor_plans (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id UUID NOT NULL REFERENCES fullrun_unit(id) ON DELETE CASCADE,
    floor_plan_url TEXT NOT NULL,
    label TEXT,
    position INTEGER DEFAULT 0,
    source TEXT DEFAULT 'livephuket',
    created_at TIMESTAMPTZ NOT NULL DEFAULT now()
);
"""
cur.execute(sql)
conn.commit()
print('Created 6 tables with fullrun_ prefix')

# Verify
for t in ['fullrun_projects_live','fullrun_project_images','fullrun_project_floor_plans',
          'fullrun_unit','fullrun_unit_images','fullrun_unit_floor_plans']:
    cur.execute(f'SELECT count(*) FROM {t}')
    print(f'{t}: {cur.fetchone()[0]} rows')

conn.close()
print('READY')