---
tags: [technical-development, database, data-storage, sql, sqlalchemy]
---
### Stockage des données

#### a. Choisir un SGBD (Système de Gestion de Base de Données)
Utilisez un SGBD comme MySQL, PostgreSQL ou SQLite pour stocker vos données.

#### b. Création de la base de données et des tables
Définissez les schémas de votre base de données.

```sql
CREATE DATABASE real_estate_db;
USE real_estate_db;

CREATE TABLE listings (
    id INT AUTO_INCREMENT PRIMARY KEY,
    title VARCHAR(255),
    price DECIMAL(10, 2),
    location VARCHAR(255),
    details TEXT
);
```

#### c. Insertion des données dans la base de données
Utilisez une bibliothèque comme SQLAlchemy pour insérer les données dans votre base de données.

```python
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Float
from sqlalchemy.orm import sessionmaker

engine = create_engine('mysql+pymysql://user:password@localhost/real_estate_db')
Base = declarative_base()

class Listing(Base):
    __tablename__ = 'listings'
    id = Column(Integer, primary_key=True)
    title = Column(String(255))
    price = Column(Float)
    location = Column(String(255))
    details = Column(String)

Base.metadata.create_all(engine)

Session = sessionmaker(bind=engine)
session = Session()

for index, row in df.iterrows():
    listing = Listing(
        title=row['title'],
        price=row['price'],
        location=row['location'],
        details=row['details']
    )
    session.add(listing)

session.commit()
```