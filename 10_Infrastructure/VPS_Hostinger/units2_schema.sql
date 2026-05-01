-- units2_schema.sql
-- Clean table set for unit extraction (Phase 2, fresh start)
-- Based on latest replica schema v3: 63 cols projects, 58 cols units + image tables with traceability
-- Run: psql $VPS_PG_URL -f units2_schema.sql
-- Idempotent: DROP IF EXISTS then CREATE

BEGIN;

-- ── 1. units2_projects_live ────────────────────────────────────────────────
DROP TABLE IF EXISTS units2_projects_live CASCADE;
CREATE TABLE units2_projects_live (
    id                           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    name                         TEXT NOT NULL,
    name_normalized              TEXT NOT NULL,
    slug                         TEXT,
    type                         TEXT,
    status                       TEXT,
    total_units                  INTEGER,
    floors                       INTEGER,
    completion_year              INTEGER,
    country                      TEXT DEFAULT 'Thailand',
    city                         TEXT,
    district                     TEXT,
    province                     TEXT,
    sub_district                 TEXT,
    latitude                     DOUBLE PRECISION,
    longitude                    DOUBLE PRECISION,
    address                      TEXT,
    developer_name               TEXT,
    construction_status           TEXT,
    price_min_thb                NUMERIC,
    price_max_thb                NUMERIC,
    rent_price_min               NUMERIC,
    rent_price_max               NUMERIC,
    ownership_type               TEXT,
    amenities                    TEXT[] DEFAULT '{}',
    nearby_places                JSONB DEFAULT '[]',
    faqs                         JSONB DEFAULT '[]',
    metadata                     JSONB DEFAULT '{}',
    description                  TEXT,
    source_url                   TEXT NOT NULL,
    data_quality_score           INTEGER DEFAULT 0,
    needs_embedding              BOOLEAN NOT NULL DEFAULT true,
    qdrant_synced_at             TIMESTAMPTZ,
    neo4j_synced_at              TIMESTAMPTZ,
    images                       JSONB DEFAULT '[]',
    primary_image_url            TEXT,
    created_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
    updated_at                   TIMESTAMPTZ NOT NULL DEFAULT now(),
    maintenance_fee_thb          NUMERIC,
    common_fee_thb               NUMERIC,
    sinking_fund_thb            NUMERIC,
    land_area_sqm                NUMERIC,
    land_area_rai                NUMERIC,
    telephone                    TEXT,
    unit_sale_links              JSONB DEFAULT '[]',
    unit_rent_links              JSONB DEFAULT '[]',
    units_for_sale_count          INTEGER DEFAULT 0,
    units_for_rent_count          INTEGER DEFAULT 0,
    nearest_landmark             TEXT,
    region                       TEXT,
    extraction_method            TEXT,
    units_in_db                  INTEGER DEFAULT 0,
    -- v2 extra columns
    payment_plan                 TEXT,
    neighborhood_overview        TEXT,
    units_listing_urls           JSONB,
    developer_about              TEXT,
    developer_projects_count     TEXT,
    developer_units_count        TEXT,
    -- v3 extra columns (latest)
    developer_all_url            TEXT,
    developer_all_text           TEXT,
    reviews                      JSONB,
    previous_sales_label         TEXT,
    previous_sales              JSONB,
    -- fullrun tracking
    batch_id                     TEXT,
    scraped_at                   TIMESTAMPTZ
);

CREATE INDEX units2_projects_live_source_url_idx ON units2_projects_live(source_url);
CREATE INDEX units2_projects_live_city_idx ON units2_projects_live(city);
CREATE INDEX units2_projects_live_province_idx ON units2_projects_live(province);
CREATE INDEX units2_projects_live_data_quality_score_idx ON units2_projects_live(data_quality_score);
CREATE INDEX units2_projects_live_developer_name_idx ON units2_projects_live(developer_name);
CREATE INDEX units2_projects_live_needs_embedding_idx ON units2_projects_live(needs_embedding) WHERE needs_embedding = true;

-- ── 2. units2_unit ─────────────────────────────────────────────────────────
DROP TABLE IF EXISTS units2_unit CASCADE;
CREATE TABLE units2_unit (
    id                           UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id                   UUID REFERENCES units2_projects_live(id) ON DELETE CASCADE,
    fazwaz_unit_id              VARCHAR,
    external_id                  VARCHAR,
    property_type                VARCHAR,
    bedrooms                     NUMERIC,
    bathrooms                    NUMERIC,
    floor_area_sqm               NUMERIC,
    floor_number                 INTEGER,
    price_thb                    BIGINT,
    price_per_sqm               NUMERIC,
    rental_price_thb             INTEGER,
    rental_yield                NUMERIC,
    ownership_type               VARCHAR,
    foreign_quota_available      BOOLEAN DEFAULT false,
    listing_status               VARCHAR DEFAULT 'available',
    availability_date            DATE,
    safe_haven_score             INTEGER DEFAULT 0,
    score_breakdown             JSONB DEFAULT '{}',
    source_url                   TEXT,
    scraped_at                   TIMESTAMPTZ,
    created_at                   TIMESTAMPTZ DEFAULT now(),
    updated_at                   TIMESTAMPTZ DEFAULT now(),
    search_vector               TSVECTOR,
    plot_size_sqm                NUMERIC,
    price_per_sqm_thb           BIGINT,
    view_type                    VARCHAR,
    furnishing                   VARCHAR,
    description                  TEXT,
    features                     JSONB DEFAULT '[]',
    cam_fee_thb                  INTEGER,
    developer_name               TEXT,
    construction_status           TEXT,
    nearest_landmark             TEXT,
    building_name                TEXT,
    listed_by                    VARCHAR,
    listed_date                  TEXT,
    listing_updated              TEXT,
    district                     TEXT,
    subdistrict                  TEXT,
    province                     TEXT,
    latitude                     NUMERIC,
    longitude                    NUMERIC,
    data_quality_score           INTEGER DEFAULT 0,
    pets                         VARCHAR,
    unit_type                    VARCHAR,
    agent_phone                  VARCHAR,
    data_source                  TEXT DEFAULT 'livephuket_scraped',
    internal_meta                JSONB DEFAULT '{}',
    qdrant_synced_at             TIMESTAMPTZ,
    price_previous_thb           BIGINT,
    needs_embedding              BOOLEAN NOT NULL DEFAULT true,
    neo4j_synced_at              TIMESTAMPTZ,
    images                       JSONB DEFAULT '[]',
    gallery_images              JSONB DEFAULT '[]',
    floor_plan_images           JSONB DEFAULT '[]',
    primary_image_url            TEXT,
    -- v3 extra column
    price_history                JSONB,
    -- fullrun tracking
    batch_id                     TEXT,
    quality_gate_passed          BOOLEAN DEFAULT false
);

CREATE INDEX units2_unit_project_id_idx ON units2_unit(project_id);
CREATE INDEX units2_unit_source_url_idx ON units2_unit(source_url);
CREATE INDEX units2_unit_data_quality_score_idx ON units2_unit(data_quality_score);
CREATE INDEX units2_unit_bedrooms_idx ON units2_unit(bedrooms);
CREATE INDEX units2_unit_price_thb_idx ON units2_unit(price_thb);
CREATE INDEX units2_unit_province_idx ON units2_unit(province);
CREATE INDEX units2_unit_furnishing_idx ON units2_unit(furnishing);
CREATE INDEX units2_unit_listing_status_idx ON units2_unit(listing_status);
CREATE INDEX units2_unit_needs_embedding_idx ON units2_unit(needs_embedding) WHERE needs_embedding = true;
CREATE INDEX units2_unit_unit_type_idx ON units2_unit(unit_type);

-- ── 3. units2_project_images ────────────────────────────────────────────────
DROP TABLE IF EXISTS units2_project_images CASCADE;
CREATE TABLE units2_project_images (
    id          UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id  UUID REFERENCES units2_projects_live(id) ON DELETE CASCADE,
    image_url   TEXT NOT NULL,
    is_primary  BOOLEAN DEFAULT false,
    position    INTEGER DEFAULT 0,
    source      TEXT DEFAULT 'livephuket',
    created_at  TIMESTAMPTZ DEFAULT now(),
    batch_id    TEXT,
    -- traceability
    project_name TEXT,
    project_url  TEXT,
    project_type  TEXT
);

CREATE INDEX units2_project_images_project_id_idx ON units2_project_images(project_id);
CREATE INDEX units2_project_images_is_primary_idx ON units2_project_images(is_primary) WHERE is_primary = true;
CREATE INDEX units2_project_images_project_url_idx ON units2_project_images(project_url);

-- ── 4. units2_project_floor_plans ──────────────────────────────────────────
DROP TABLE IF EXISTS units2_project_floor_plans CASCADE;
CREATE TABLE units2_project_floor_plans (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    project_id     UUID REFERENCES units2_projects_live(id) ON DELETE CASCADE,
    floor_plan_url  TEXT NOT NULL,
    label           TEXT,
    position        INTEGER DEFAULT 0,
    source          TEXT DEFAULT 'livephuket',
    created_at      TIMESTAMPTZ DEFAULT now(),
    batch_id        TEXT,
    -- traceability
    project_name   TEXT,
    project_url     TEXT,
    project_type    TEXT
);

CREATE INDEX units2_project_floor_plans_project_id_idx ON units2_project_floor_plans(project_id);

-- ── 5. units2_unit_images ──────────────────────────────────────────────────
DROP TABLE IF EXISTS units2_unit_images CASCADE;
CREATE TABLE units2_unit_images (
    id                   UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id              UUID REFERENCES units2_unit(id) ON DELETE CASCADE,
    image_url            TEXT,
    is_primary           BOOLEAN,
    position             INTEGER,
    source               TEXT DEFAULT 'livephuket',
    created_at           TIMESTAMPTZ DEFAULT now(),
    vision_tags          JSONB DEFAULT '{}',
    vision_confidence    DOUBLE PRECISION,
    vision_model         TEXT,
    vision_classified_at TIMESTAMPTZ,
    is_floorplan         BOOLEAN DEFAULT false,
    batch_id             TEXT,
    -- traceability
    project_name         TEXT,
    project_url          TEXT,
    project_type         TEXT
);

CREATE INDEX units2_unit_images_unit_id_idx ON units2_unit_images(unit_id);
CREATE INDEX units2_unit_images_is_primary_idx ON units2_unit_images(is_primary) WHERE is_primary = true;
CREATE INDEX units2_unit_images_is_floorplan_idx ON units2_unit_images(is_floorplan) WHERE is_floorplan = true;
CREATE INDEX units2_unit_images_project_url_idx ON units2_unit_images(project_url);

-- ── 6. units2_unit_floor_plans ────────────────────────────────────────────
DROP TABLE IF EXISTS units2_unit_floor_plans CASCADE;
CREATE TABLE units2_unit_floor_plans (
    id             UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    unit_id        UUID REFERENCES units2_unit(id) ON DELETE CASCADE,
    floor_plan_url  TEXT NOT NULL,
    label           TEXT,
    position        INTEGER DEFAULT 0,
    source          TEXT DEFAULT 'livephuket',
    created_at      TIMESTAMPTZ DEFAULT now(),
    batch_id        TEXT,
    -- traceability
    project_name   TEXT,
    project_url     TEXT,
    project_type    TEXT
);

CREATE INDEX units2_unit_floor_plans_unit_id_idx ON units2_unit_floor_plans(unit_id);

COMMIT;