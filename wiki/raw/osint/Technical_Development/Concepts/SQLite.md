---
tags: [database, sqlite, python, technical-development]
---
### SQLite
**Pourquoi choisir SQLite**:
- **Simplicité** : Facile à configurer et utiliser, pas besoin d'un serveur dédié.
- **Portabilité** : Les bases de données sont stockées sous forme de fichiers, ce qui facilite la portabilité.

**Comment l'utiliser**:
- **sqlite3** : Utilisez le module sqlite3 pour interagir avec SQLite en Python.
- **Exemple d'insertion** :
    ```python
    import sqlite3
    import json
    
    conn = sqlite3.connect('real_estate.db')
    cur = conn.cursor()
    
    cur.execute("""
    CREATE TABLE IF NOT EXISTS listings (
        id INTEGER PRIMARY KEY,
        title TEXT,
        price INTEGER,
        address TEXT,
        images TEXT
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
    VALUES (?, ?, ?, ?)
    """, (listing['title'], listing['price'], listing['address'], json.dumps(listing['images'])))
    
    conn.commit()
    cur.close()
    conn.close()
    ```