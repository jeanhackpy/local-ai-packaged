---
tags: [ai, agent, statistics, data-collection, weather, python]
---
### Agent Statistiques
Cet agent recueillera des données sur les aéroports, les températures, l'hygrométrie, etc.

**Bibliothèques et outils :**
- **Requests** pour accéder aux API météorologiques et aéroportuaires.
- **Pandas** pour la manipulation de données.
- **Matplotlib** et **Seaborn** pour la visualisation des données.

```python
import requests
import pandas as pd

def get_weather_data(location):
    response = requests.get(f'https://api.weather.com/v3/wx/conditions/current?apiKey=YOUR_API_KEY&geocode={location}&format=json')
    weather_data = response.json()
    return weather_data

# Exemple d'utilisation
location = '48.8566,2.3522'  # Coordonnées de Paris
weather_data = get_weather_data(location)
print(weather_data)
```