# OS-PALANTHAI 3D Map - Matched Buildings

## Ce qui a été fait

### Problème initial
Les bâtiments 3D n'affichaient pas sur la carte. Cause racine : la couche `matched-buildings-3d` utilisait `type: 'fill'` avec des propriétés `fill-extrusion-*` (ignoré silencieusement).

### Fichiers modifiés

#### 1. `/home/phil/palanthai/phase5-mapping/src/components/Map.jsx`

**Correction du type de couche (bug critique)**
- Changé `type: 'fill'` → `type: 'fill-extrusion'` pour les bâtiments 3D

**Filtre Supabase - Condominiums Bangkok uniquement**
```javascript
.eq('type', 'condominium')
.eq('province', 'Bangkok')
.not('latitude', 'is', null)
```

**Couleurs cyberpunk appliquées**
- Exact matches: `#e94560` (neon pink/rouge)
- Proximity matches: `#00f5ff` (cyan)

```javascript
'fill-extrusion-color': [
  'case',
  ['==', ['get', 'matchMethod'], 'exact'], '#e94560',
  '#00f5ff'
]
```

**Données projet complètes pour l'affichage**
- floors, total_units, price_min/max_thb, completion_year, district, developer_name, address

#### 2. `/home/phil/palanthai/phase5-mapping/src/utils/spatial_building_match.js`

**Indexation spatiale RBush**
- Pour performer avec 50,000 bâtiments OSM
- RBush = bounding box tree pour requêtes O(log n)

**Fermeture des polygones**
- Vérifie que les rings GeoJSON sont fermés (premier point = dernier point)
- Évite l'erreur "First and last Position are not equivalent"

```javascript
if (first[0] !== last[0] || first[1] !== last[1]) {
  coords = [[...ring, first]];
}
```

### Logique de matching

1. **Exact match** : Le point projet (lng/lat) est contenu dans le polygone bâtiment → `matchMethod: 'exact'`
2. **Proximity match** : Aucun exact found → cherche le centroïde bâtiment le plus proche dans un rayon de 100m → `matchMethod: 'proximity'`
3. **No match** : `matchedBuilding: null`

### Résultats attendus

- 1944 condominiums Bangkok avec coordonnées
- Bâtiments 3D affichés en neon (rose = exact, cyan = proximity)
- Clic sur bâtiment → panel avec données projet (year, developer, floors, etc.)

## Accès

```bash
ssh -L 5173:localhost:5173 phil@31.97.67.145
# Ouvrir http://localhost:5173
```

## Stats de matching

Le matching rate s'affiche dans la console du navigateur :
```
Matched X/1944 projects to building footprints
```

## Architecture

```
Map.jsx
├── loadAllData()
│   ├── Fetch GeoJSON bangkok_buildings.geojson (50k bâtiments OSM)
│   ├── Query Supabase (condos Bangkok + coords)
│   └── matchProjectsToBuildings() → RBush spatial index
├── addLayers()
│   ├── matched-buildings source ( GeoJSON FeatureCollection)
│   └── matched-buildings-3d layer (fill-extrusion, cyberpunk colors)
└── click handlers → Panel avec données projet
```