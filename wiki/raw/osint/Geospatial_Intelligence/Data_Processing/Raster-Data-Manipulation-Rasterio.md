---
tags: [geospatial, data-processing, rasterio, python]
---
### Manipulation de Données Raster avec Rasterio
Utiliser Rasterio pour manipuler des données raster :
```python
import rasterio

# Ouvrir un fichier raster
with rasterio.open('path_to_your_raster.tif') as src:
    raster_data = src.read(1)
    print(raster_data)
```