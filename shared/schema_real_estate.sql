-- ============================================================================
-- PALANTIR IMMOBILIER - SCHÉMA UNIFIÉ
-- Version: 1.0
-- Objectif: Normalisation + Déduplication + Scoring opportunités
-- ============================================================================

-- Extensions requises
CREATE EXTENSION IF NOT EXISTS "uuid-ossp";
CREATE EXTENSION IF NOT EXISTS "pg_trgm";  -- Pour matching flou
CREATE EXTENSION IF NOT EXISTS "postgis";  -- Pour géolocalisation

-- ============================================================================
-- 1. RÉFÉRENTIEL GÉOGRAPHIQUE
-- ============================================================================

CREATE TABLE geo_provinces (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name_th TEXT NOT NULL,
    name_en TEXT NOT NULL,
    code TEXT UNIQUE,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE geo_districts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    province_id UUID REFERENCES geo_provinces(id),
    name_th TEXT NOT NULL,
    name_en TEXT NOT NULL,
    code TEXT,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE geo_zones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    district_id UUID REFERENCES geo_districts(id),
    name_th TEXT,
    name_en TEXT NOT NULL,
    slug TEXT,
    geo_center GEOMETRY(POINT, 4326),
    geo_bounds GEOMETRY(POLYGON, 4326),
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE geo_microzones (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    zone_id UUID REFERENCES geo_zones(id),
    name TEXT NOT NULL,
    geo_center GEOMETRY(POINT, 4326),
    radius_meters INTEGER DEFAULT 500,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index géographiques
CREATE INDEX idx_geo_zones_center ON geo_zones USING GIST(geo_center);
CREATE INDEX idx_geo_microzones_center ON geo_microzones USING GIST(geo_center);

-- ============================================================================
-- 2. PROMOTEURS & PROJETS (Knowledge Graph ready)
-- ============================================================================

CREATE TABLE developers (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL,
    name_normalized TEXT,  -- Pour matching
    slug TEXT UNIQUE,
    website TEXT,
    rating_score DECIMAL(3,2),  -- 0-5
    projects_count INTEGER DEFAULT 0,
    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE TABLE projects (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    developer_id UUID REFERENCES developers(id),

    -- Identification
    name TEXT NOT NULL,
    name_normalized TEXT,
    slug TEXT UNIQUE,

    -- Localisation
    geo_zone_id UUID REFERENCES geo_zones(id),
    geo_microzone_id UUID REFERENCES geo_microzones(id),
    address_raw TEXT,
    address_normalized TEXT,
    geo_point GEOMETRY(POINT, 4326),

    -- Caractéristiques
    project_type TEXT CHECK (project_type IN ('condominium', 'villa', 'townhouse', 'land')),
    total_units INTEGER,
    floors INTEGER,
    completion_year INTEGER,
    status TEXT CHECK (status IN ('planning', 'under_construction', 'completed')),

    -- Amenities (array)
    amenities TEXT[],

    -- Standing
    standing_level TEXT CHECK (standing_level IN ('budget', 'mid_range', 'premium', 'luxury')),

    -- Métadonnées
    external_ids JSONB DEFAULT '{}',  -- {"thailand-property": "123", "fazwaz": "456"}
    metadata JSONB DEFAULT '{}',

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index pour matching
CREATE INDEX idx_projects_name_normalized ON projects(name_normalized);
CREATE INDEX idx_projects_geo_point ON projects USING GIST(geo_point);

-- ============================================================================
-- 3. RÉSIDENCES (Condos/Villas individuels)
-- ============================================================================

CREATE TABLE residences (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    project_id UUID REFERENCES projects(id),

    -- Identification
    unit_number TEXT,
    building_name TEXT,

    -- Caractéristiques physiques
    property_type TEXT CHECK (property_type IN ('condo', 'villa', 'townhouse', 'land')),
    bedrooms DECIMAL(3,1),  -- Peut être 1.5
    bathrooms DECIMAL(3,1),
    floor_area_sqm DECIMAL(10,2),
    land_area_sqm DECIMAL(10,2),
    floor_number INTEGER,
    orientation TEXT,  -- N, S, E, W, NE, etc.

    -- Vue
    view_type TEXT[],  -- ['sea', 'city', 'pool', 'garden']

    -- Statut
    ownership_type TEXT CHECK (ownership_type IN ('freehold', 'leasehold')),
    foreign_quota_available BOOLEAN,

    -- Déduplication
    canonical_hash TEXT,  -- Hash pour matching
    duplicate_of UUID REFERENCES residences(id),  -- Si doublon détecté

    metadata JSONB DEFAULT '{}',
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Index déduplication
CREATE INDEX idx_residences_canonical_hash ON residences(canonical_hash);

-- ============================================================================
-- 4. LISTINGS (Annonces multi-sources)
-- ============================================================================

CREATE TABLE sources (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    name TEXT NOT NULL UNIQUE,  -- thailand-property, fazwaz, ddproperty
    base_url TEXT,
    scraping_config JSONB DEFAULT '{}',
    last_scraped_at TIMESTAMPTZ,
    is_active BOOLEAN DEFAULT true
);

CREATE TABLE listings (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    source_id UUID REFERENCES sources(id),
    residence_id UUID REFERENCES residences(id),  -- Link après matching

    -- ID externe
    external_id TEXT NOT NULL,
    external_url TEXT NOT NULL,

    -- Prix
    price_thb DECIMAL(15,2),
    price_original DECIMAL(15,2),
    currency_original TEXT DEFAULT 'THB',
    price_per_sqm DECIMAL(10,2),

    -- Titre & Description
    title TEXT,
    description TEXT,

    -- Caractéristiques (raw)
    raw_specs JSONB DEFAULT '{}',  -- Données brutes source

    -- Statut annonce
    listing_status TEXT CHECK (listing_status IN ('active', 'sold', 'withdrawn', 'expired')),
    first_seen_at TIMESTAMPTZ DEFAULT NOW(),
    last_seen_at TIMESTAMPTZ DEFAULT NOW(),
    days_on_market INTEGER,

    -- Images
    images TEXT[],
    main_image_url TEXT,

    -- Contact
    agent_name TEXT,
    agent_phone TEXT,
    agency_name TEXT,

    -- Matching
    match_confidence DECIMAL(5,4),  -- 0-1 score de confiance matching
    match_method TEXT,  -- 'exact', 'fuzzy', 'geo', 'manual'

    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW(),

    UNIQUE(source_id, external_id)  -- Pas de doublons par source
);

-- Index pour recherche
CREATE INDEX idx_listings_price ON listings(price_thb);
CREATE INDEX idx_listings_status ON listings(listing_status);
CREATE INDEX idx_listings_first_seen ON listings(first_seen_at);

-- ============================================================================
-- 5. HISTORIQUE PRIX (Pour détection tendances)
-- ============================================================================

CREATE TABLE price_history (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    listing_id UUID REFERENCES listings(id),
    residence_id UUID REFERENCES residences(id),

    price_thb DECIMAL(15,2),
    price_per_sqm DECIMAL(10,2),
    recorded_at TIMESTAMPTZ DEFAULT NOW(),

    change_from_previous DECIMAL(10,4),  -- Pourcentage
    change_type TEXT CHECK (change_type IN ('increase', 'decrease', 'stable')),

    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_price_history_listing ON price_history(listing_id, recorded_at DESC);

-- ============================================================================
-- 6. SCORING OPPORTUNITÉS
-- ============================================================================

CREATE TABLE opportunity_scores (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    residence_id UUID REFERENCES residences(id),
    listing_id UUID REFERENCES listings(id),

    -- Scores individuels (0-100)
    price_vs_zone_score DECIMAL(5,2),
    dom_score DECIMAL(5,2),  -- Days on market
    standing_score DECIMAL(5,2),
    rarity_score DECIMAL(5,2),
    developer_score DECIMAL(5,2),
    location_score DECIMAL(5,2),

    -- Score global
    total_score DECIMAL(5,2),
    score_percentile DECIMAL(5,2),  -- Position vs autres listings

    -- Signal
    signal_type TEXT CHECK (signal_type IN ('hot', 'warm', 'neutral', 'avoid')),
    signal_reasons TEXT[],

    -- Validité
    valid_until TIMESTAMPTZ,
    calculated_at TIMESTAMPTZ DEFAULT NOW(),

    metadata JSONB DEFAULT '{}'
);

CREATE INDEX idx_opportunity_scores_total ON opportunity_scores(total_score DESC);
CREATE INDEX idx_opportunity_signals ON opportunity_scores(signal_type, calculated_at);

-- ============================================================================
-- 7. ALERTES & NOTIFICATIONS
-- ============================================================================

CREATE TABLE alerts (
    id UUID PRIMARY KEY DEFAULT uuid_generate_v4(),
    alert_type TEXT NOT NULL,
    reference_type TEXT CHECK (reference_type IN ('listing', 'residence', 'zone')),
    reference_id UUID,

    title TEXT,
    description TEXT,
    severity TEXT CHECK (severity IN ('info', 'warning', 'critical')),

    is_read BOOLEAN DEFAULT false,
    is_dismissed BOOLEAN DEFAULT false,

    notified_at TIMESTAMPTZ,
    created_at TIMESTAMPTZ DEFAULT NOW()
);

CREATE INDEX idx_alerts_unread ON alerts(is_read, created_at DESC) WHERE is_read = false;

-- ============================================================================
-- 8. VUES UTILES
-- ============================================================================

-- Vue listings avec scoring
CREATE VIEW v_listings_scored AS
SELECT
    l.id,
    l.external_url,
    l.title,
    l.price_thb,
    l.price_per_sqm,
    l.bedrooms,
    l.floor_area_sqm,
    l.days_on_market,
    l.listing_status,
    s.name as source_name,
    p.name as project_name,
    p.standing_level,
    os.total_score,
    os.signal_type,
    os.signal_reasons,
    l.last_seen_at
FROM listings l
JOIN sources s ON l.source_id = s.id
LEFT JOIN residences r ON l.residence_id = r.id
LEFT JOIN projects p ON r.project_id = p.id
LEFT JOIN opportunity_scores os ON l.id = os.listing_id
WHERE l.listing_status = 'active';

-- Vue statistiques par zone
CREATE VIEW v_zone_stats AS
SELECT
    gz.id as zone_id,
    gz.name_en as zone_name,
    COUNT(DISTINCT l.id) as listing_count,
    AVG(l.price_thb) as avg_price,
    AVG(l.price_per_sqm) as avg_price_per_sqm,
    AVG(l.days_on_market) as avg_dom,
    MIN(l.price_per_sqm) as min_price_per_sqm,
    MAX(l.price_per_sqm) as max_price_per_sqm
FROM geo_zones gz
LEFT JOIN projects p ON p.geo_zone_id = gz.id
LEFT JOIN residences r ON r.project_id = p.id
LEFT JOIN listings l ON l.residence_id = r.id AND l.listing_status = 'active'
GROUP BY gz.id, gz.name_en;

-- ============================================================================
-- 9. FONCTIONS UTILITAIRES
-- ============================================================================

-- Fonction de normalisation de texte pour matching
CREATE OR REPLACE FUNCTION normalize_for_matching(text_to_normalize TEXT)
RETURNS TEXT AS $$
BEGIN
    RETURN lower(
        regexp_replace(
            regexp_replace(text_to_normalize, '[^\w\s]', '', 'g'),
            '\s+', ' ', 'g'
        )
    );
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Fonction calcul hash canonique pour déduplication
CREATE OR REPLACE FUNCTION compute_canonical_hash(
    p_project_name TEXT,
    p_unit_number TEXT DEFAULT NULL,
    p_bedrooms DECIMAL DEFAULT NULL,
    p_floor_area DECIMAL DEFAULT NULL
)
RETURNS TEXT AS $$
DECLARE
    hash_input TEXT;
BEGIN
    hash_input := concat_ws('|',
        normalize_for_matching(p_project_name),
        COALESCE(p_unit_number, ''),
        COALESCE(p_bedrooms::TEXT, ''),
        COALESCE(p_floor_area::TEXT, '')
    );
    RETURN md5(hash_input);
END;
$$ LANGUAGE plpgsql IMMUTABLE;

-- Trigger pour MAJ automatique updated_at
CREATE OR REPLACE FUNCTION update_updated_at()
RETURNS TRIGGER AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER trigger_projects_updated
    BEFORE UPDATE ON projects
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_residences_updated
    BEFORE UPDATE ON residences
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

CREATE TRIGGER trigger_listings_updated
    BEFORE UPDATE ON listings
    FOR EACH ROW EXECUTE FUNCTION update_updated_at();

-- ============================================================================
-- 10. DONNÉES INITIALES
-- ============================================================================

-- Sources de données
INSERT INTO sources (name, base_url) VALUES
    ('thailand-property', 'https://www.thailand-property.com'),
    ('fazwaz', 'https://www.fazwaz.com'),
    ('ddproperty', 'https://www.ddproperty.com'),
    ('propertyhub', 'https://propertyhub.in.th'),
    ('bangkokcondos', 'https://bangkokcondos.com')
ON CONFLICT (name) DO NOTHING;

-- Provinces principales
INSERT INTO geo_provinces (name_th, name_en, code) VALUES
    ('กรุงเทพมหานคร', 'Bangkok', 'BKK'),
    ('ภูเก็ต', 'Phuket', 'PKT'),
    ('สุราษฎร์ธานี', 'Surat Thani', 'SRI')  -- Pour Koh Samui
ON CONFLICT DO NOTHING;

COMMIT;
