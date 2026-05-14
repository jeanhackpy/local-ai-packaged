---
tags: [cybersecurity, tool, wpscan, wordpress, brute-force]
---
### WPScan
WPScan est un outil dédié aux tests de sécurité de WordPress et peut être utilisé pour brute forcer les pages de connexion WordPress. Cependant, il est principalement conçu pour brute forcer les identifiants utilisateur et mot de passe, et non un code d'accès unique.

**Utilisation de base** :
```sh
wpscan --url example.com --passwords /path/to/password_list.txt --username admin
```
- **--url**: Spécifie l'URL du site WordPress.
- **--passwords**: Spécifie la liste de mots de passe.
- **--username**: Spécifie le nom d'utilisateur à tester.