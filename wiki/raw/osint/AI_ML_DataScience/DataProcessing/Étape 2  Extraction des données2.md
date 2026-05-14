### Étape 2 : Extraction des données

Nous pouvons utiliser des API disponibles sur ces sites ou télécharger des fichiers CSV contenant les données historiques. Voici un exemple de script Python utilisant l'API de Yahoo Finance pour extraire des données :

```python
import yfinance as yf
import pandas as pd

# Liste des devises par rapport à l'USD
currencies = ['EURUSD=X', 'THBUSD=X', 'AEDUSD=X', 'SGDUSD=X', 'MXNUSD=X']

# Période de 10 ans
start_date = '2013-01-01'
end_date = '2023-01-01'

# Dictionnaire pour stocker les données
data = {}

# Téléchargement des données
for currency in currencies:
    data[currency] = yf.download(currency, start=start_date, end=end_date)['Adj Close']

# Conversion en DataFrame
df = pd.DataFrame(data)
df.reset_index(inplace=True)
df.rename(columns={'Date': 'Année'}, inplace=True)

# Sauvegarde des données dans un fichier CSV
df.to_csv('historical_exchange_rates.csv', index=False)

print(df.head())
```