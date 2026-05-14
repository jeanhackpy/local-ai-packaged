---
tags: [geospatial, data-processing, google-earth-engine, export]
---
### Exportation des Résultats

**Google Earth Engine Export:**
- **API:** Google Earth Engine Export API
- **Exemple:**
  ```python
  # Exporter les résultats en shapefile
  export_task = ee.batch.Export.table.toDrive(collection=coastline, description='Coastline', fileFormat='SHP')
  export_task.start()
  ```