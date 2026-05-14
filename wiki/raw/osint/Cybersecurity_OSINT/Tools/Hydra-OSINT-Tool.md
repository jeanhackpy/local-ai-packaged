---
tags: [osint, tool, hydra, brute-force, security, password-attack]
---

### 1. **Hydra**
Hydra est un outil de force brute très flexible qui peut être utilisé pour attaquer différents types de services de connexion, y compris les formulaires web.

**Utilisation de base pour un formulaire web** :
```sh
hydra -l admin -P /path/to/password_list.txt example.com http-post-form "/wp-login.php:log=^USER^&pwd=^PASS^&wp-submit=Log+In&testcookie=1:S=Location" -V
```
- **-l**: Spécifie l'utilisateur cible.
- **-P**: Spécifie la liste de mots de passe.
- **http-post-form**: Indique que c'est un formulaire POST HTTP.
- **S=Location**: Indique le succès basé sur la redirection de l'URL.