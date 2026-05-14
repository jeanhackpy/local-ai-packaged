---
tags: [geospatial, data-visualization, folium, python]
---
### Visualisation Interactive avec Folium
Créer des cartes interactives avec Folium :
```python
import folium

# Définir le centre de la carte
map_center = [gdf.geometry.centroid.y.mean(), gdf.geometry.centroid.x.mean()]

# Créer une carte Folium
m = folium.Map(location=map_center, zoom_start=10)

# Ajouter des données géospatiales à la carte
for _, row in gdf.iterrows():
    folium.GeoJson(row['geometry']).add_to(m)

# Sauvegarder la carte en fichier HTML
m.save('map.html')
```