#!/usr/bin/env python3
"""Write phase5 codemap documents via SSH."""
import subprocess
import sys

host = "phil@31.97.67.145"
base = "/home/phil/palanthai/phase5-mapping/.planning/codebase"

docs = {
    "STACK.md": """# STACK.md — Phase 5 Technology Stack

## Core Framework
- **React 19.2.5** — UI framework, hooks-based component architecture
- **Vite 8.0.10** — Build tool, HMR dev server, bundler
- **No TypeScript** — Plain JavaScript (.jsx files)

## Mapping & 3D
- **MapLibre GL 5.24.0** — Vector tile map rendering (CartoDB Positron basemap)
- **Three.js 0.184.0** — WebGL 3D rendering (buildings, labels, interactions)
- **Turf.js 7.3.5** — Spatial analysis (distance, centroid, bbox operations)
- **RBush 4.0.1** — High-performance 2D spatial index (O(k log n) range queries)

## Backend & Database
- **@supabase/supabase-js 2.104.1** — PostgreSQL client, auth, realtime subscriptions
- **Supabase** — Primary data store (projects, units, developers, districts, transit, schools, hospitals)

## Coordinate Systems
- **EPSG:4326** (WGS84) — Source coordinates from Supabase/OSM
- **Vector3 (Three.js)** — Internal 3D representation (lng, lat → x/y/z)
- **Bangkok center**: lng 100.5018, lat 13.7563
- **Tile bounds**: lat 13.5–13.9, lng 100.35–100.7

## Build & Dev
- **ESLint 10.2.1** — Linting
- **No unit test framework** — Plain Node.js test scripts in tests/

## Environment Variables
```
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

## Key Package.json Scripts
```json
{
  "dev": "vite",
  "build": "vite build",
  "preview": "vite preview",
  "lint": "eslint ."
}
```

## Dependencies Summary
| Package | Version | Purpose |
|---------|---------|---------|
| react | 19.2.5 | UI components |
| react-dom | 19.2.5 | DOM rendering |
| maplibre-gl | 5.24.0 | Vector tile map |
| three | 0.184.0 | WebGL 3D |
| @turf/turf | 7.3.5 | Spatial math |
| rbush | 4.0.1 | Spatial index |
| @supabase/supabase-js | 2.104.1 | Database client |

## Missing / Not Used
- **Cesium** — Not installed despite phase5 name
- **Google Draco** — Decoder from Gstatic CDN (no npm package)
- **proj4** — No coordinate transformation library
- **No Jest/Vitest** — only 3 plain Node test scripts
""",
    "INTEGRATIONS.md": """# INTEGRATIONS.md — Phase 5 External Integrations

## Supabase Database
- **projects** / **replica_projects_live** — Project metadata (name, type, prices, coordinates, developer)
- **units** — Individual unit listings linked to projects
- **developers** — Developer profiles
- **districts** — Geographic boundaries
- **transit_stations** — BTS/MRT station locations
- **schools** — Educational institutions
- **hospitals** — Medical facilities

## Map Tiles
- **CartoDB Positron** (`https://basemaps.cartocdn.com/gl/positron-gl-style/`) — No auth required
- Free vector tile basemap for maplibre-gl

## OpenStreetMap (OSM)
- **Overpass API** — `https://overpass-api.de/api/interpreter`
- Queries for building footprints within Bangkok bounds
- Bounds: lat 13.5–13.9, lng 100.35–100.7

## Google Draco
- **Decoder**: `https://fonts.gstatic.com/s/draco_decoder/draco_decoder.v1.5.0.js`
- CDN URL for 3D building mesh decoding
- No authentication required

## Environment Variables
```
VITE_SUPABASE_URL=https://xxx.supabase.co
VITE_SUPABASE_ANON_KEY=eyJ...
```

## Integration Architecture
```
Supabase (projects, units, developers, districts)
    ├── replica_projects_live view → buildings_3d
    ├── districts (polygon lookup for map)
    └── spatial index (RBush) → cached in memory

OSM Overpass API → building footprints → Three.js GeoJSONLoader → building meshes

CartoDB Positron → MapLibre GL basemap layer
```

## Potential Issues
- spatial_entities table may not exist → Supabase realtime subscription fails
- No RLS policy validation in codebase
- OSM data freshness: Overpass API may have stale building data
""",
    "ARCHITECTURE.md": """# ARCHITECTURE.md — Phase 5 3D Map Interface

**Analysis Date:** 2026-05-01

## Pattern Overview
- MapLibre GL JS as primary mapping engine with CARTO basemap
- Three.js integrated via MapLibre Custom Layer Interface for 3D rendering
- React 19 with hooks-based state management
- RBush spatial indexing for point-in-polygon queries
- Supabase as backend data store

## Layers

**UI Layer (React Components):** `src/components/` — Map.jsx, Panel.jsx, Search.jsx, Filters.jsx

**Map Rendering Layer (MapLibre GL JS):** `src/components/Map.jsx` — base map, building extrusions, landmarks, click/hover

**3D Rendering Layer (Three.js):** `src/utils/GlbLoader.js`, `src/utils/PrestigeShader.js` — custom layer interface

**Spatial Indexing Layer (RBush + Turf.js):** `src/utils/spatial_building_match.js` — exact + proximity matching

**Data Access Layer (Supabase):** `src/lib/supabase.js` — @supabase/supabase-js client

**State Management (React Hooks):** `src/hooks/` — useEntityLoader, useSpatialInteraction, useSpatialNavigation, useSpatialSync

## Data Flow

**Project Loading Flow:**
1. MapLibre loads with CARTO basemap
2. On map 'load' event, `loadAllData()` called
3. Bangkok building footprints loaded from `/data/bangkok_buildings.geojson`
4. Projects fetched from Supabase `replica_projects_live`
5. Projects matched to buildings via `matchProjectsToBuildings()`:
   - Exact: point-in-polygon via Turf.js
   - Fallback: proximity matching (closest centroid within 100m)
6. 3D fill-extrusion layer created from matched building polygons

**Project-to-Building Matching Pipeline:**
```
Supabase (replica_projects_live) → spatial_building_match.matchProjectsToBuildings()
    ├── RBush spatial index from building footprints
    └── For each project:
            ├── Exact: point-in-polygon via Turf.js
            └── Proximity: closest centroid within 100m
    → Map.addLayer('matched-buildings-3d') as fill-extrusion
```

## Key Abstractions

**useEntityLoader:** Bounds-based querying with client-side filtering
**useSpatialInteraction:** THREE.Raycaster with mouse coordinate transformation
**useSpatialNavigation:** Easing functions for animation (easeInQuad, easeOutCubic)
**useSpatialSync:** MapLibre 'move' event → Three.js camera sync
**PrestigeShader:** ShaderMaterial with prestige index uniforms
**createThreeCustomLayer:** MapLibre Custom Layer Interface implementation

## Entry Points

- `src/main.jsx` — React root, StrictMode
- `src/App.jsx` — Renders Map in full-viewport container
- `src/components/Map.jsx` — MapLibre init, data loading, layer management

## Error Handling
Console logging with graceful degradation, try-catch around async ops, fallback to empty data on source failure.
""",
    "STRUCTURE.md": """# STRUCTURE.md — Phase 5 File Organization

**Analysis Date:** 2026-05-01

## Directory Layout
```
phase5-mapping/
├── .env                         # Supabase credentials
├── .planning/codebase/          # GSD codemap docs
├── GIS_github_repo              # File with GIS GitHub resource links
├── IMPLEMENTATION_STATUS.md
├── PHASE5_IMPLEMENTATION.md
├── PRD_mapping/                  # Product requirements
├── README-RUN.md
├── README.md
├── SUPABASE_DB_INSPECTION.md
├── eslint.config.js
├── index.html
├── map_feature_proto_S2Vec/
├── node_modules/
├── open-buildings/
│   └── 30f_buildings.csv.gz    # 1GB Google Open Buildings
├── package.json
├── public/
│   ├── data/
│   │   ├── bangkok_buildings.geojson  # 39MB building footprints
│   │   ├── buildings.geojson
│   │   └── test_buildings.geojson
│   ├── favicon.svg
│   └── icons.svg
├── scripts/
│   ├── export_data.mjs
│   ├── extract_buildings_near_projects.mjs
│   ├── extract_open_buildings.mjs
│   └── extract_osm_buildings.mjs
├── src/
│   ├── App.jsx, App.css, main.jsx, index.css
│   ├── assets/ (hero.png, react.svg, vite.svg)
│   ├── components/ (Map.jsx, Panel.jsx, Search.jsx, Filters.jsx)
│   ├── hooks/ (useEntityLoader.js, useSpatialInteraction.js, useSpatialNavigation.js, useSpatialSync.js)
│   ├── lib/ (supabase.js)
│   └── utils/ (EraConfig.js, GlbLoader.js, PrestigeShader.js, landmarks.js, overpass.js, prestige_scoring.js, spatial_building_match.js, spatial_utils.js)
├── test_supabase.js
├── test_supabase_fetch.js
└── tests/
    ├── test_navigation.js
    ├── test_raycaster.js
    └── test_shader.js
```

## Directory Purposes

- **`src/components/`** — UI components (Map, Panel, Search, Filters)
- **`src/hooks/`** — React custom hooks (entity loading, spatial interaction, navigation, sync)
- **`src/utils/`** — Pure functions (spatial matching, shaders, API clients, config)
- **`src/lib/`** — Third-party library wrappers (Supabase client)
- **`public/data/`** — Local GeoJSON building footprints (bangkok_buildings.geojson 39MB)
- **`scripts/`** — Node.js data extraction (Supabase export, OSM extraction)
- **`open-buildings/`** — Google Open Buildings dataset (not git-tracked, 1GB)
- **`tests/`** — Plain Node.js test scripts (no Jest/Vitest)

## Naming Conventions

- Components: PascalCase.jsx (Map.jsx, Panel.jsx)
- Hooks: camelCase with `use` prefix (useEntityLoader.js, useSpatialSync.js)
- Utilities: camelCase.js (spatial_utils.js, GlbLoader.js)
- Config: PascalCase (EraConfig.js, PrestigeShader.js)
- Directories: lowercase plural (components/, hooks/, utils/)

## Where to Add New Code

- New component: `src/components/NewFeature.jsx`
- New hook: `src/hooks/useNewHook.js`
- New utility: `src/utils/newUtility.js`
- New script: `scripts/extract_new_data.mjs`
- New static data: `public/data/new_data.geojson`
""",
    "CONCERNS.md": """# CONCERNS.md — Phase 5 Quality & Technical Concerns

**Analysis Date:** 2026-05-01

## Critical Issues

### Coordinate System Mismatch
- `Map.jsx` uses `replica_projects_live` table (lat/lng columns)
- `useEntityLoader.js` queries `projects` table (PostGIS geo_point)
- The hook is effectively dead code — not used by Map.jsx
- Root cause: two data sources for the same entities

### Realtime Subscription Target Missing
- `subscribeToEntityUpdates()` targets `spatial_entities` table
- This table does not exist per SUPABASE_DB_INSPECTION.md
- Subscription will fail silently — no error thrown
- Results in: no realtime updates reaching the client

### Dead Code Path
- `useEntityLoader.js` exported but never imported anywhere
- 146 lines of Supabase query code with no caller
- Cleanup candidate — verify no future plan before removing

## Performance Issues

### RBush Index Rebuilt on Every Filter
- `matchProjectsToBuildings()` rebuilds the RBush index on each filter change
- Called twice per project (once in `loadAllData`, once in `onFilterChange`)
- For large building sets, this is O(n log n) per filter change

### Full Scene Traversal for Raycasting
- `useSpatialInteraction.js` does full Three.js scene traversal on every mouse move
- No frustum culling before raycasting
- Will degrade badly with dense 3D content

### No Level-of-Detail (LOD)
- All 3D buildings rendered at same polygon count regardless of zoom
- No geometry simplification at distance
- Will cause performance issues at city-wide zoom levels

## Security Concerns

### API Keys Client-Side
- `VITE_SUPABASE_ANON_KEY` exposed in client-side bundle
- Should be fine for public read-only data
- No validation of RLS policies in code

### No Input Validation
- Supabase responses parsed without schema validation
- No check that coordinate values are within expected ranges
- Potential for malformed data to crash rendering

## Missing Features

### Building Height Not from GeoJSON
- GeoJSON only has footprint polygons, no height field
- All buildings rendered at uniform ~3m per floor estimate
- Actual building heights not visualized

### No Clustering at Low Zoom
- All projects rendered as individual markers at low zoom
- Will cause overdraw issues for large datasets
- Should cluster at z < 12

### Custom Layer Unused
- `createThreeCustomLayer` documented in GlbLoader.js
- Not actually called by Map.jsx
- Map uses native MapLibre fill-extrusion instead
- Planned 3D enhancements not active

## Test Gaps
- No Jest/Vitest test framework
- Only 3 plain Node.js test scripts (test_raycaster.js, test_navigation.js, test_shader.js)
- No integration tests
- No E2E tests
- No test for spatial building matching logic

## Documentation Gaps
- No API documentation
- No component prop types
- README-RUN.md exists but no inline code documentation
""",
    "CONVENTIONS.md": """# CONVENTIONS.md — Phase 5 Coding Conventions

**Analysis Date:** 2026-05-01

## Coordinate Convention
- **GeoJSON standard: [lng, lat] array order**
- Bangkok center: `{ lng: 100.5018, lat: 13.7563 }`
- NEVER use [lat, lng] — this is a common mistake
- All Supabase coordinates stored as (lng, lat) pairs

## Component Conventions
- **File naming**: PascalCase.jsx (Map.jsx, Panel.jsx, Search.jsx, Filters.jsx)
- **Default export** for all React components
- **JSDoc comments** on hook functions describing parameters and return values
- **Inline styles** mixed with CSS classes from index.css
- **Lucide icons** used for UI iconography (imported from lucide-react)

## Hook Conventions
- Named exports with `use` prefix
- Return object or tuple (not mixed)
- useCallback for memoized event handlers
- useEffect for side effects (subscriptions, event listeners)
- Example: `export function useEntityLoader(map) { ... }`

## 3D Conventions
- **Floor height**: ~3m per floor (used for building height estimation)
- **Origin**: bottom-center of building bounding box
- **Prestige index**: 0-100 scale, gold/silver/dark color coding
- **Shader uniforms**: time, prestigeIndex, glowColor for PrestigeShader

## Era System
- 5 eras with distinct hex colors (CSS variables):
  - Pre-1990, 1990-1999, 2000-2009, 2010-2019, 2020+
- Era derived from `completion_year` field
- Used for building color coding in 3D view

## CSS Conventions
- CSS custom properties (variables) for colors, fonts, spacing
- BEM-like class naming in index.css
- No CSS-in-JS
- No Tailwind — plain CSS with utility classes

## Testing Conventions
- Plain Node.js scripts in `tests/` directory
- No Jest/Vitest framework
- Manual testing approach with console assertions
- Test files: test_raycaster.js, test_navigation.js, test_shader.js

## Supabase Conventions
- `VITE_SUPABASE_URL` and `VITE_SUPABASE_ANON_KEY` env vars
- Client initialized in `src/lib/supabase.js`
- Use `.select()` with explicit column lists (no `*`)
- Filter with `.eq()`, `.gte()`, `.contains()` etc.
""",
    "TESTING.md": """# TESTING.md — Phase 5 Testing Approach

**Analysis Date:** 2026-05-01

## Current Test Coverage

### Test Framework: None (Plain Node.js scripts)
No Jest, Vitest, or any JS test framework installed. Tests are manual console scripts.

## Existing Tests (3 files in tests/ directory)

### test_raycaster.js
- Tests THREE.Raycaster mouse picking logic
- Mock Three.js objects for raycaster tests
- Manual console output verification

### test_navigation.js
- Tests camera navigation easing functions
- Tests easeInQuad, easeOutCubic, easeInOutCubic
- Manual verification of easing curve output

### test_shader.js
- Tests PrestigeShader uniform handling
- Tests shader compilation
- Manual console output checking

## Recommended Test Setup

For Phase 5, recommended framework: **Vitest** (integrates well with Vite)

```bash
npm install -D vitest @testing-library/react jsdom
```

## Test Categories Needed

### Unit Tests
- `spatial_building_match.js` — RBush matching logic
- `prestige_scoring.js` — score calculation
- Era color assignment logic
- Coordinate transformation utilities

### Component Tests
- Map.jsx rendering with mock MapLibre
- Panel.jsx display of selected entity
- Search.jsx filtering behavior
- Filters.jsx filter state management

### Integration Tests
- Full data flow: Supabase → match → render
- Map interaction: click → panel update
- Filter change → re-render cycle

### E2E Tests
- Load map → verify buildings rendered
- Search for project → click → panel shows details
- Filter by price/type → results update

## Performance Testing
- Load with 1000 projects (currently using test_buildings.geojson 36KB)
- Measure RBush rebuild time
- Measure render frame rate with 3D buildings
- Test low zoom performance with no clustering

## Coverage Target
Current: ~0% (no automated tests)
Recommended: 60%+ core logic, 80%+ spatial matching
"""
}

for filename, content in docs.items():
    path = f"{base}/{filename}"
    result = subprocess.run(
        ['ssh', host, f'python3 -c "import os; os.makedirs(os.path.dirname(\'{path}\'), exist_ok=True); f=open(\'{path}\', \'w\'); f.write({repr(content)}); f.close(); print(\'OK: {filename}\')"'],
        capture_output=True, text=True, timeout=30
    )
    print(result.stdout, result.stderr)

if __name__ == '__main__':
    print("Done")