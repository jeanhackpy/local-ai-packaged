---
tags: [web-scraping, data-collection, curl, cli]
---

### 1. Curl (en ligne de commande)

**Curl** est un outil en ligne de commande disponible sur la plupart des systèmes d'exploitation (y compris macOS, Linux et Windows via des installations tierces comme Cygwin ou Git Bash sur Windows). Il est simple à utiliser pour effectuer des requêtes HTTP et récupérer des réponses JSON.

Exemple de commande pour récupérer une réponse JSON :
```bash
curl https://api.example.com/endpoint
```
- **Avantages :**
  - Facile à utiliser en ligne de commande.
  - Supporte une variété de protocoles et d'options.

- **Inconvénients :**
  - Peut nécessiter une manipulation supplémentaire pour analyser et traiter les données JSON.