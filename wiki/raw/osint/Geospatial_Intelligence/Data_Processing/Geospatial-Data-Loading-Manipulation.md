---
tags: [geospatial, data-processing, geopandas, python]
---
### Chargement et Manipulation des Données Géospatiales
Utiliser GeoPandas pour charger et manipuler les données géospatiales :
```python
import geopandas as gpd
from shapely.geometry import Point, Polygon

# Charger des données géospatiales
gdf = gpd.read_file('path_to_your_shapefile.shp')

# Afficher les premières lignes du GeoDataFrame
print(gdf.head())
```