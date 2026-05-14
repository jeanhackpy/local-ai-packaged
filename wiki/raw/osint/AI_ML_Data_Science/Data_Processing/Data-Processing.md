### 2. Traitement des données

Une fois les données extraites, elles doivent être nettoyées et structurées.

#### a. Nettoyage des données
- Supprimez les valeurs nulles ou non valides.
- Convertissez les données dans des formats appropriés (par exemple, prix en chiffres, dates en formats date).

```python
import pandas as pd

# Exemple de structure de données
data = {
    'title': [],
    'price': [],
    'location': [],
    'details': []
}

# Ajoutez des données à la structure
for listing in listings:
    data['title'].append(listing.find('h2', class_='title').text)
    data['price'].append(listing.find('span', class_='price').text.replace('$', '').replace(',', ''))
    data['location'].append(listing.find('div', class_='location').text)
    data['details'].append(listing.find('ul', class_='details').text)

df = pd.DataFrame(data)
df['price'] = pd.to_numeric(df['price'], errors='coerce')
```