### Exemple de Code Complet
Voici un exemple de script Python intégrant ces composants :
```python
import geopandas as gpd
import folium
from shapely.geometry import Point, Polygon
import rasterio
from pyproj import Proj, transform

# Charger des données géospatiales
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Créer une carte interactive avec Folium
map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]
m = folium.Map(location=map_center, zoom_start=10)
for _, row in gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)
m.save('map.html')

# Opérations géométriques avec Shapely
point = Point(1, 1)
polygon = Polygon([(0, 0), (1, 1), (1, 0)])
print(polygon.contains(point))  # True

# Manipulation de données raster avec Rasterio
with rasterio.open('path_to_your_raster.tif') as src:
    raster_data = src.read(1)
    print(raster_data)

# Transformation de coordonnées avec Pyproj
in_proj = Proj(init='epsg:4326')
out_proj = Proj(init='epsg:3857')
x1, y1 = -120.0, 35.0
x2, y2 = transform(in_proj, out_proj, x1, y1)
print(x2, y2)
```