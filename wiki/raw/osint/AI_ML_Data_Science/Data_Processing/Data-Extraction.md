---
tags: [data-processing, data-extraction, web-scraping, python, real-estate]
---
### Extraction des Données

#### a. Récupération des Actualités Immobilières

Nous allons utiliser des API comme celles de Google News pour extraire des articles sur l'immobilier en Thaïlande.

```python
import requests
from bs4 import BeautifulSoup

def get_real_estate_news():
    url = "https://news.google.com/rss/search?q=immobilier+en+Thaïlande"
    response = requests.get(url)
    soup = BeautifulSoup(response.content, 'xml')
    items = soup.findAll('item')
    news = []
    for item in items:
        news.append({
            "title": item.title.text,
            "link": item.link.text,
            "pubDate": item.pubDate.text
        })
    return news
```