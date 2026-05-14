### Étape 2 : Extraction des données

Si les données sont présentées en format non téléchargeable, nous pouvons utiliser un script de web scraping en Python pour extraire les informations. Voici un exemple de script de web scraping :

```python
import requests
from bs4 import BeautifulSoup
import pandas as pd

# URL des pages à scraper (à adapter en fonction des sources réelles)
urls = [
    'https://www.airportthai.co.th/en/annual-reports/',
    'https://www.caat.or.th/en/annual-statistics'
]

data = []

for url in urls:
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'html.parser')
    
    # Logique de scraping à adapter en fonction de la structure des pages
    tables = soup.find_all('table')
    for table in tables:
        rows = table.find_all('tr')
        for row in rows:
            cols = row.find_all('td')
            cols = [ele.text.strip() for ele in cols]
            data.append(cols)

# Convertir les données en DataFrame pandas
df = pd.DataFrame(data, columns=['Année', 'Nom de l_Aéroport', 'Type_de_Passagers', 'Volume_de_Passagers', 'Latitude', 'Longitude'])

# Sauvegarder les données dans un fichier CSV
df.to_csv('airport_data.csv', index=False)
```