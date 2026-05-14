---
tags: [geospatial, data-processing, shapely, python]
---
### Opérations Géospatiales avec Shapely
Utiliser Shapely pour des opérations géométriques avancées :
```python
from shapely.geometry import Point

# Exemple de création d'un point et d'un polygone
point = Point(1, 1)
polygon = Polygon([(0, 0), (1, 1), (1, 0)])

# Vérifier si le point est dans le polygone
print(polygon.contains(point))  # True
```