---
tags: [osint, reconnaissance, information-gathering, theharvester, recon-ng, nmap]
---

### 1. **Reconnaissance et collecte d'informations**
#### 1.1 Utiliser **theHarvester**
   - **Objectif**: Collecter des emails, sous-domaines, noms d'hôte, etc.
   - **Commande**: `theHarvester -d example.com -l 500 -b all`

#### 1.2 Utiliser **Recon-ng**
   - **Objectif**: Automatiser la collecte d'informations à partir de diverses sources.
   - **Modules**: `recon/domains-hosts/bing_domain_web`, `recon/domains-hosts/google_site_web`
   - **Commande**: `recon-ng` puis charger et exécuter les modules nécessaires.

#### 1.3 Utiliser **Nmap**
   - **Objectif**: Scanner les ports ouverts et découvrir les services en cours d'exécution.
   - **Commande**: `nmap -sS -A example.com`