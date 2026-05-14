---
tags: [cybersecurity, tool, medusa, brute-force, web-security]
---
### Medusa
Medusa est un autre outil de force brute qui peut attaquer divers services de connexion, y compris les formulaires web.

**Utilisation de base pour un formulaire web** :
```sh
medusa -h example.com -u admin -P /path/to/password_list.txt -M web-form -m FORM:/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&testcookie=1
```
- **-h**: Spécifie l'hôte cible.
- **-u**: Spécifie l'utilisateur cible.
- **-P**: Spécifie la liste de mots de passe.
- **-M web-form**: Indique que la méthode cible est un formulaire web.
- **-m FORM**: Spécifie les détails du formulaire web.