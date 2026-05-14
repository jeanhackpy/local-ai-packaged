---
tags: [real-estate, database, sqlalchemy, python]
---
### Connexion aux Bases de Données Immobilières
Utiliser SQLAlchemy pour se connecter aux bases de données :
```python
from sqlalchemy import create_engine

engine = create_engine('postgresql://user:password@localhost/mydatabase')
```