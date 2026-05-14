---
tags: [geospatial, image-processing, opencv, gdal, python]
---
### Extraction des Lignes Côtières

**Edge Detection et Vectorization:**
- Utiliser OpenCV et GDAL pour le traitement des images et la vectorisation.

**Exemple de Code Python:**
```python
import cv2
import numpy as np
from osgeo import gdal, ogr

# Charger l'image
image_path = 'path_to_image.tif'
image = cv2.imread(image_path, cv2.IMREAD_GRAYSCALE)

# Appliquer la détection de contours
edges = cv2.Canny(image, 100, 200)

# Convertir en vecteur (shapefile)
def raster_to_vector(raster_path, vector_path):
    src_ds = gdal.Open(raster_path)
    srcband = src_ds.GetRasterBand(1)

    drv = ogr.GetDriverByName("ESRI Shapefile")
    dst_ds = drv.CreateDataSource(vector_path)
    dst_layer = dst_ds.CreateLayer('', None, ogr.wkbLineString)

    gdal.Polygonize(srcband, None, dst_layer, -1, [], callback=None)

raster_to_vector('edges.tif', 'coastline.shp')
```