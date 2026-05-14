---
tags: [database, postgresql, python, technical-development]
---
### PostgreSQL
**Pourquoi choisir PostgreSQL**:
- **Flexibilité des types de données** : Supporte les types de données JSON et JSONB, ce qui est utile pour les données web.
- **Performance** : Excellent pour les requêtes complexes et les transactions.
- **PostGIS** : Extension pour gérer les données géospatiales, utile pour les coordonnées de propriétés.

**Comment l'utiliser**:
- **Psycopg2** : Utilisez la bibliothèque Psycopg2 pour interagir avec PostgreSQL en Python.
- **Exemple d'insertion** :
    ```python
    import psycopg2
    
    conn = psycopg2.connect("dbname=real_estate user=postgres password=secret")
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id SERIAL PRIMARY KEY,
        title TEXT,
        price INTEGER,
        address TEXT,
        images JSONB
    )
    """)
    
    listing = {
        'title': 'Beautiful Apartment',
        'price': 250000,
        'address': '123 Main St',
        'images': [
            {'filename': 'img1.jpg', 'url': 'http://example.com/img1.jpg'},
            {'filename': 'img2.jpg', 'url': 'http://example.com/img2.jpg'}
        ]
    }
    
    cur.execute("""
    INSERT INTO listings (title, price, address, images)
    VALUES (%s, %s, %s, %s)
    """, (listing['title'], listing['price'], listing['address'], json.dumps(listing['images'])))
    
    conn.commit()
    cur.close()
    conn.close()
    ```