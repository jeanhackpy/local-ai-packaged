---
tags: [cybersecurity, session, cookies, nmap, concept]
---
### Utilisation de cookies de session
Si vous avez déjà authentifié et avez une session valide, vous pouvez extraire les cookies et les utiliser dans votre scan nmap. Vous pouvez obtenir les cookies en utilisant des outils comme `curl` ou via les outils de développement de votre navigateur.

Voici un exemple de commande nmap utilisant des cookies :

```bash
nmap -A -T4 -p- --script http-cookie-flags --script-args http-cookie-flags.cookie="nom_du_cookie=valeur_du_cookie" www.monsiteperso.com
```