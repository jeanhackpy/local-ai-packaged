### Étapes pour utiliser la structure XML

#### 1. Lire et parser le fichier XML

Vous pouvez utiliser des bibliothèques comme `xml.etree.ElementTree` pour lire et parser les fichiers XML en Python.

```python
import xml.etree.ElementTree as ET

# Supposons que le fichier XML soit nommé 'data.xml'
tree = ET.parse('data.xml')
root = tree.getroot()

# Exemple de parcours de la structure XML
for property in root.findall('property'):
    title = property.find('title').text
    price = property.find('price').text
    location = property.find('location').text
    details = property.find('details').text
    print(f"Title: {title}, Price: {price}, Location: {location}, Details: {details}")
```

#### 2. Structurer les données pour insertion dans une base de données

Créez une structure de données pour organiser les informations extraites.

```python
data = {
    'title': [],
    'price': [],
    'location': [],
    'details': []
}

for property in root.findall('property'):
    data['title'].append(property.find('title').text)
    data['price'].append(property.find('price').text.replace('$', '').replace(',', ''))
    data['location'].append(property.find('location').text)
    data['details'].append(property.find('details').text)

# Convertir en DataFrame pour faciliter la manipulation
import pandas as pd

df = pd.DataFrame(data)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
```

#### 3. Créer une base de données et insérer les données

Créez une base de données et une table pour stocker les données immobilières.

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

Utilisez SQLAlchemy pour insérer les données dans la base de données.

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