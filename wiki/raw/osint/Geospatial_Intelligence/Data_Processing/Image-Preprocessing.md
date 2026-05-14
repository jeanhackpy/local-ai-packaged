---
tags: [geospatial, image-processing, google-earth-engine, sentinel-2, python]
---
### Prétraitement des Images

**Google Earth Engine:**
- **API:** Google Earth Engine Python API
- **Exemple:**
  ```python
  import ee

  ee.Initialize()

  # Charger la collection d'images Sentinel-2
  collection = ee.ImageCollection('COPERNICUS/S2').filterDate('2022-01-01', '2022-12-31').filterBounds(ee.Geometry.Rectangle([98, 5, 105, 20]))

  # Appliquer le masque des nuages et créer une composite médiane
  def maskClouds(image):
      cloudProb = ee.Image(image.get('QA60')).divide(10000)
      isCloud = cloudProb.gt(0.2)
      return image.updateMask(isCloud.Not())

  cloudMasked = collection.map(maskClouds)
  medianComposite = cloudMasked.median()

  # Calculer l'NDWI
  ndwi = medianComposite.normalizedDifference(['B3', 'B8'])

  # Seuil de l'NDWI pour classifier l'eau
  water = ndwi.gt(0.3)
  ```