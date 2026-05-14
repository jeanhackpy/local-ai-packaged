---
tags: [cybersecurity, tool, burp-suite, web-security, brute-force]
---
### Burp Suite
Burp Suite est un outil de test de sécurité web très puissant qui peut être utilisé pour brute forcer des formulaires personnalisés, y compris les pages de connexion avec un code d'accès.

**Procédure** :
1. **Capturer la requête** : Utilisez le proxy de Burp Suite pour capturer la requête POST de la page de connexion.
2. **Intruder** : Envoyez la requête à l'outil Intruder et configurez les points d'injection pour le champ de code d'accès.
3. **Configurer les Payloads** : Chargez une liste de codes d'accès potentiels et lancez l'attaque.