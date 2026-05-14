### Étape 4 : Visualisation des données

Utilisez Plotly pour créer un graphique interactif montrant l'évolution des taux de change sur les 10 dernières années :

```python
import plotly.express as px

# Chargement des données
df = pd.read_csv('historical_exchange_rates.csv')

# Création du graphique
fig = px.line(df, x='Date', y=['EURUSD', 'THBUSD', 'AEDUSD', 'SGDUSD', 'MXNUSD'],
              labels={'value': 'Taux de Change', 'variable': 'Devise'},
              title='Évolution des Taux de Change sur les 10 Dernières Années')

fig.show()
```