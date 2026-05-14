### Code Python

```python
import requests
import folium
from geopy.geocoders import Nominatim

# Utiliser une API comme celle de Zillow ou de Realtor pour obtenir des données immobilières (nécessite une clé API)

# Fonction pour obtenir les données immobilières d'une API
def get_real_estate_data(lat, lon):
    # Exemple de requête à une API immobilière
    # url = f"https://api.example.com/realestate?lat={lat}&lon={lon}&radius=1km"
    # response = requests.get(url, headers={"Authorization": "Bearer YOUR_API_KEY"})
    # data = response.json()
    # Simuler des données pour l'exemple
    data = {
        "average_price": 250000,
        "average_rent": 1500,
        "new_developments": [
            {"name": "Project A", "price": 300000},
            {"name": "Project B", "price": 350000}
        ]
    }
    return data

# Fonction pour obtenir des informations sur les commodités locales à partir de la géolocalisation
def get_local_amenities(lat, lon):
    # Utiliser une API comme Google Places pour obtenir ces informations (nécessite une clé API)
    # url = f"https://maps.googleapis.com/maps/api/place/nearbysearch/json?location={lat},{lon}&radius=1000&type=restaurant&key=YOUR_API_KEY"
    # response = requests.get(url)
    # amenities = response.json()
    # Simuler des données pour l'exemple
    amenities = {
        "restaurants": ["Restaurant A", "Restaurant B", "Restaurant C"],
        "shopping_centers": ["Mall A", "Mall B"],
        "airports": ["Airport A"],
        "hospitals": ["Hospital A", "Hospital B"]
    }
    return amenities

# Fonction principale pour l'analyse du marché immobilier
def analyze_real_estate_market(lat, lon):
    real_estate_data = get_real_estate_data(lat, lon)
    amenities = get_local_amenities(lat, lon)
    
    report = {
        "location": (lat, lon),
        "average_price": real_estate_data["average_price"],
        "average_rent": real_estate_data["average_rent"],
        "new_developments": real_estate_data["new_developments"],
        "amenities": amenities
    }
    return report

# Fonction pour générer une carte avec les informations
def generate_map(lat, lon, report):
    m = folium.Map(location=[lat, lon], zoom_start=15)
    
    # Ajouter un marqueur pour la localisation de l'utilisateur
    folium.Marker([lat, lon], popup='Your Location').add_to(m)
    
    # Ajouter des marqueurs pour les nouvelles constructions
    for development in report["new_developments"]:
        folium.Marker(
            [lat, lon], 
            popup=f'{development["name"]}: ${development["price"]}'
        ).add_to(m)
    
    # Ajouter des marqueurs pour les commodités
    for restaurant in report["amenities"]["restaurants"]:
        folium.Marker([lat, lon], popup=restaurant, icon=folium.Icon(color='blue')).add_to(m)
    for shopping_center in report["amenities"]["shopping_centers"]:
        folium.Marker([lat, lon], popup=shopping_center, icon=folium.Icon(color='green')).add_to(m)
    for airport in report["amenities"]["airports"]:
        folium.Marker([lat, lon], popup=airport, icon=folium.Icon(color='red')).add_to(m)
    for hospital in report["amenities"]["hospitals"]:
        folium.Marker([lat, lon], popup=hospital, icon=folium.Icon(color='purple')).add_to(m)
    
    return m

# Exemple d'utilisation
if __name__ == "__main__":
    # Utiliser la géolocalisation du téléphone pour obtenir les coordonnées actuelles (lat, lon)
    geolocator = Nominatim(user_agent="real_estate_analysis")
    location = geolocator.geocode("Your address or place")
    lat, lon = location.latitude, location.longitude
    
    # Analyser le marché immobilier
    report = analyze_real_estate_market(lat, lon)
    
    # Générer et sauvegarder la carte
    map = generate_map(lat, lon, report)
    map.save("real_estate_analysis_map.html")
```