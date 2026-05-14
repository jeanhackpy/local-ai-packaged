### Exemple de Code avec Plotly en Python

Pour illustrer ce processus, voici un exemple de script Python utilisant Plotly pour créer une carte interactive :

```python
import pandas as pd
import plotly.express as px

# Exemple de données (à remplacer par les données réelles)
data = {
    'Année': [2010, 2010, 2011, 2011, 2022, 2022],
    'Nom de l_Aéroport': ['Suvarnabhumi', 'Don Mueang', 'Suvarnabhumi', 'Don Mueang', 'Suvarnabhumi', 'Don Mueang'],
    'Type_de_Passagers': ['Domestiques', 'Domestiques', 'Internationaux', 'Internationaux', 'Domestiques', 'Internationaux'],
    'Volume_de_Passagers': [14000000, 7000000, 22000000, 6000000, 40000000, 15000000],
    'Latitude': [13.6923, 13.9126, 13.6923, 13.9126, 13.6923, 13.9126],
    'Longitude': [100.7501, 100.6077, 100.7501, 100.6077, 100.7501, 100.6077]
}

# Convertir les données en DataFrame
df = pd.DataFrame(data)

# Créer une carte interactive avec Plotly
fig = px.scatter_geo(df, lat='Latitude', lon='Longitude', 
                     size='Volume_de_Passagers', color='Nom de l_Aéroport',
                     hover_name='Nom de l_Aéroport', hover_data={'Année': True, 'Type_de_Passagers': True, 'Volume_de_Passagers': True},
                     animation_frame='Année', title='Volume de Passagers des Aéroports Thaïlandais (2010-2023)')

fig.update_geos(showcoastlines=True, coastlinecolor="Black", showland=True, landcolor="LightGreen")

fig.show()
```