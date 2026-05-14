---
tags: [blockchain, python, data-analysis, script, example, cryptocurrency]
---
### Exemple de Script Python pour l'Analyse des Données de la Blockchain

Voici un exemple simplifié de script Python pour extraire certaines de ces données à partir d'une API blockchain (comme Solana):

```python
import requests
import pandas as pd
from datetime import datetime

# Fonction pour extraire les données de transactions de la blockchain
def fetch_transactions(token_address, start_date, end_date):
    url = f"https://api.blockchain.com/v3/tokens/{token_address}/transactions"
    params = {
        "start_date": start_date,
        "end_date": end_date
    }
    response = requests.get(url, params=params)
    data = response.json()
    return data

# Exemple d'utilisation pour un token spécifique
token_address = "example_token_address"
start_date = "2023-01-01"
end_date = "2023-12-31"

transactions = fetch_transactions(token_address, start_date, end_date)

# Convertir les données en DataFrame
df_transactions = pd.DataFrame(transactions)

# Calculer les KPI
volume_transactions = df_transactions['amount'].sum()
nombre_transactions = df_transactions.shape[0]
adresses_actives = df_transactions['from_address'].nunique()

print(f"Volume de Transactions: {volume_transactions}")
print(f"Nombre de Transactions: {nombre_transactions}")
print(f"Adresses Actives: {adresses_actives}")
```