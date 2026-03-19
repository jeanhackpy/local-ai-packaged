# 🐘 CHANG — Database Architecture v2

> Central Hub for Aggregation, Normalization & Governance

---

## Schema Evolution: v1 → v2

### What changed
- **Added lat/lng native fields** (from JSON-LD, no geocoding needed)
- **Structured address** (street, locality, region, country)
- **Developer as first-class entity** with financial links (SET ticker)
- **Listing (unit-level)** table for Phase 2
- **FAQ knowledge base** table for RAG
- **Audit trail** on all records

---

## 🗄️ Supabase (PostgreSQL) — Relational Core

### Table: `developer`
```sql
CREATE TABLE developer (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name            TEXT NOT NULL UNIQUE,
    slug            TEXT UNIQUE,
    url             TEXT,                          -- LivePhuket profile
    description     TEXT,
    project_count   INT,
    total_units     INT,
    developer_units INT,
    resale_units    INT,
    set_ticker      TEXT,                          -- SET Thailand stock symbol (Phase 2)
    set_sector      TEXT DEFAULT 'PROP',
    website         TEXT,
    telephone       TEXT,
    logo_url        TEXT,
    created_at      TIMESTAMPTZ DEFAULT now(),
    updated_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_developer_name ON developer(name);
CREATE INDEX idx_developer_set_ticker ON developer(set_ticker);
```

### Table: `project`
```sql
CREATE TABLE project (
    id                  UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    name                TEXT NOT NULL,
    url                 TEXT UNIQUE NOT NULL,

    -- Location (JSON-LD primary)
    address             TEXT,
    address_street      TEXT,
    address_locality    TEXT,
    address_region      TEXT,
    address_country     TEXT DEFAULT 'Thailand',
    latitude            DOUBLE PRECISION,
    longitude           DOUBLE PRECISION,

    -- Pricing
    sale_price_min      DOUBLE PRECISION,
    sale_price_max      DOUBLE PRECISION,
    rent_price_min      DOUBLE PRECISION,
    rent_price_max      DOUBLE PRECISION,

    -- Project details
    developer_id        UUID REFERENCES developer(id),
    num_units           INT,
    number_of_floors    INT,
    completion_date     TEXT,
    completion_year     INT,
    construction_status TEXT,
    ownership_type      TEXT,                      -- Freehold/Leasehold

    -- Rich data
    description         TEXT,
    facilities          TEXT[],                    -- Array of amenity names
    pets_allowed        BOOLEAN,
    payment_plan        TEXT,
    neighborhood        TEXT,
    telephone           TEXT,

    -- Media
    images              TEXT[],                    -- Array of image URLs
    card_image          TEXT,

    -- Unit counts
    units_for_sale      INT DEFAULT 0,
    units_for_rent      INT DEFAULT 0,

    -- Classification
    region              TEXT NOT NULL,
    property_type       TEXT NOT NULL,
    nearest_landmark    TEXT,

    -- Quality & metadata
    data_quality_score  REAL,
    extraction_method   TEXT DEFAULT 'jsonld+css',
    source_markdown     TEXT,
    crawl_timestamp     TIMESTAMPTZ,
    created_at          TIMESTAMPTZ DEFAULT now(),
    updated_at          TIMESTAMPTZ DEFAULT now()
);

-- Indexes for common queries
CREATE INDEX idx_project_region ON project(region);
CREATE INDEX idx_project_type ON project(property_type);
CREATE INDEX idx_project_developer ON project(developer_id);
CREATE INDEX idx_project_geo ON project USING GIST (
    ST_SetSRID(ST_MakePoint(longitude, latitude), 4326)
);  -- PostGIS spatial index
CREATE INDEX idx_project_price ON project(sale_price_min, sale_price_max);
CREATE INDEX idx_project_year ON project(completion_year);
CREATE INDEX idx_project_status ON project(construction_status);
```

### Table: `listing` (Phase 2 — Unit-level)
```sql
CREATE TABLE listing (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    project_id      UUID REFERENCES project(id),
    url             TEXT UNIQUE NOT NULL,

    -- Unit details
    unit_type       TEXT,                          -- Studio, 1BR, 2BR, Penthouse, etc.
    title           TEXT,
    price_thb       DOUBLE PRECISION,
    price_per_sqm   DOUBLE PRECISION,
    area_sqm        DOUBLE PRECISION,
    floor           INT,
    bedrooms        INT,
    bathrooms       INT,

    -- Title deed
    ownership_type  TEXT,                          -- Freehold/Leasehold
    title_deed_type TEXT,                          -- Chanote, Nor Sor 3, etc.

    -- Classification
    listing_type    TEXT NOT NULL,                 -- 'sale' or 'rent'
    is_resale       BOOLEAN DEFAULT false,

    -- Media
    images          TEXT[],

    -- Metadata
    source          TEXT,                          -- livephuket, ddproperty, etc.
    crawl_timestamp TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_listing_project ON listing(project_id);
CREATE INDEX idx_listing_type ON listing(listing_type);
CREATE INDEX idx_listing_price ON listing(price_thb);
```

### Table: `faq_article` (RAG Knowledge Base)
```sql
CREATE TABLE faq_article (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    title           TEXT NOT NULL,
    url             TEXT UNIQUE NOT NULL,
    category        TEXT,
    content         TEXT,
    meta_description TEXT,
    word_count      INT,
    published_date  DATE,
    author          TEXT,
    keywords        TEXT,
    source          TEXT DEFAULT 'fazwaz',
    crawl_timestamp TIMESTAMPTZ,
    created_at      TIMESTAMPTZ DEFAULT now()
);
CREATE INDEX idx_faq_category ON faq_article(category);
```

### Table: `market_data` (KINNAREE — Financial Intelligence)
```sql
CREATE TABLE market_data (
    id              UUID DEFAULT gen_random_uuid() PRIMARY KEY,
    ticker          TEXT NOT NULL,
    company_name    TEXT,
    sector          TEXT DEFAULT 'PROP',
    date            DATE NOT NULL,

    -- Financial metrics
    market_cap_thb  DOUBLE PRECISION,
    price           DOUBLE PRECISION,
    pe_ratio        DOUBLE PRECISION,
    pb_ratio        DOUBLE PRECISION,
    dividend_yield  DOUBLE PRECISION,

    -- Source
    source          TEXT DEFAULT 'SET',
    raw_data        JSONB,
    crawl_timestamp TIMESTAMPTZ,

    UNIQUE(ticker, date, source)
);
CREATE INDEX idx_market_ticker ON market_data(ticker);
CREATE INDEX idx_market_date ON market_data(date);
```

### RLS Policies (Row-Level Security)
```sql
-- Enable RLS on all tables
ALTER TABLE project ENABLE ROW LEVEL SECURITY;
ALTER TABLE developer ENABLE ROW LEVEL SECURITY;
ALTER TABLE listing ENABLE ROW LEVEL SECURITY;

-- Public read access (for API)
CREATE POLICY "Public read" ON project FOR SELECT USING (true);
CREATE POLICY "Public read" ON developer FOR SELECT USING (true);
CREATE POLICY "Public read" ON listing FOR SELECT USING (true);

-- Service role write access
CREATE POLICY "Service write" ON project FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service write" ON developer FOR ALL USING (auth.role() = 'service_role');
CREATE POLICY "Service write" ON listing FOR ALL USING (auth.role() = 'service_role');
```

---

## 🧠 Qdrant — Vector Search (GARUDA)

### Collection: `projects`
- **Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Distance**: Cosine
- **Text for embedding**: `{name} {address} {description} {facilities_joined}`

```json
{
  "vectors": { "size": 384, "distance": "Cosine" },
  "payload_schema": {
    "name": "keyword",
    "region": "keyword",
    "property_type": "keyword",
    "developer": "keyword",
    "latitude": "float",
    "longitude": "float",
    "sale_price_min": "float",
    "sale_price_max": "float",
    "completion_year": "integer",
    "construction_status": "keyword",
    "facilities": "keyword[]",
    "data_quality_score": "float"
  }
}
```

### Collection: `faq_knowledge`
- **Model**: `all-MiniLM-L6-v2` (384 dimensions)
- **Distance**: Cosine
- **Chunking**: 500 tokens with 50 token overlap
- **Text for embedding**: article content chunks

```json
{
  "payload_schema": {
    "title": "keyword",
    "category": "keyword",
    "url": "keyword",
    "chunk_index": "integer",
    "word_count": "integer"
  }
}
```

---

## 🐉 Neo4j — Knowledge Graph (NAGA)

### Node Types
```cypher
(:Project {name, url, latitude, longitude, region, property_type,
           sale_price_min, completion_year, quality_score})
(:Developer {name, slug, url, project_count, total_units, set_ticker})
(:Location {name, type})  -- type: Province, District, Subdistrict
(:Facility {name})
(:PropertyType {name})    -- Condo, Villa, Townhouse, House
(:MarketSector {name})    -- PROP, PROPCON
```

### Relationships
```cypher
(:Project)-[:DEVELOPED_BY]->(:Developer)
(:Project)-[:LOCATED_IN]->(:Location)
(:Project)-[:HAS_FACILITY]->(:Facility)
(:Project)-[:IS_TYPE]->(:PropertyType)
(:Developer)-[:LISTED_ON {ticker}]->(:MarketSector)
(:Location)-[:PART_OF]->(:Location)  -- District → Province
(:Developer)-[:ALSO_DEVELOPS]->(:Developer)  -- co-development relations
```

### Constraints
```cypher
CREATE CONSTRAINT project_url IF NOT EXISTS FOR (p:Project) REQUIRE p.url IS UNIQUE;
CREATE CONSTRAINT developer_name IF NOT EXISTS FOR (d:Developer) REQUIRE d.name IS UNIQUE;
CREATE CONSTRAINT location_name IF NOT EXISTS FOR (l:Location) REQUIRE l.name IS UNIQUE;
CREATE CONSTRAINT facility_name IF NOT EXISTS FOR (f:Facility) REQUIRE f.name IS UNIQUE;
```

---

## Data Flow Diagram

```
SIAM Extractors                  CHANG Storage                    GARUDA/NAGA
───────────────                  ─────────────                    ──────────

phase1_project_extractor.py ──┬──▶ Supabase: project          ──▶ Qdrant: projects
                              │                                  ──▶ Neo4j: Project nodes
                              │
phase1_developer_extractor.py ──▶ Supabase: developer          ──▶ Neo4j: Developer nodes
                              │
phase1_faq_extractor.py ──────▶ Supabase: faq_article          ──▶ Qdrant: faq_knowledge
                              │
phase1_financial_extractor.py ─▶ Supabase: market_data         ──▶ Neo4j: MarketSector
```

---

## Frontend Recommendation: Mapbox GL JS

**Why Mapbox over alternatives:**

| Criteria | Mapbox GL JS | Leaflet | Google Maps |
|:---|:---|:---|:---|
| 3D buildings | ✅ Native | ❌ No | ⚠️ Limited |
| Custom styling | ✅ Full control | ⚠️ Limited | ⚠️ Limited |
| Performance (10K+ markers) | ✅ WebGL | ❌ DOM-based | ⚠️ OK |
| Thai map data quality | ✅ Good | ✅ OSM-based | ✅ Best |
| Pricing | ⚠️ Free tier 50K loads | ✅ Free | ⚠️ $200/mo credit |
| Privacy | ✅ Self-hostable tiles | ✅ Full control | ❌ Google tracking |
| Clustering | ✅ Built-in | ⚠️ Plugin | ✅ Built-in |

**Recommendation**: Mapbox GL JS for primary map, with fallback to MapLibre GL (100% open-source fork) for self-hosted deployment.

---

## Scalability Considerations

1. **Horizontal scaling**: Supabase handles read replicas natively
2. **Vector search**: Qdrant supports sharding for >1M vectors
3. **Graph queries**: Neo4j Aura scales to enterprise
4. **Caching**: Redis/Upstash for API response caching
5. **CDN**: Image URLs already on FazWaz CDN, no self-hosting needed
6. **Batch processing**: n8n workflows on VPS for scheduled crawls
