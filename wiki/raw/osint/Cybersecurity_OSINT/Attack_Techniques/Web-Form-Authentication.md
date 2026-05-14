---
tags: [cybersecurity, authentication, web-form, hydra, nmap, burp-suite, nikto, attack-technique]
---
### Authentification via formulaire web
Pour des sites web utilisant des formulaires de connexion, l'approche est plus complexe et nécessite généralement l'utilisation de scripts ou d'outils spécialisés pour automatiser l'authentification. Vous pouvez utiliser un outil comme `Hydra`, `Nikto`, ou `Burp Suite` pour cette tâche, mais nmap peut aussi être scripté pour cela avec `http-form-brute`.

Voici un exemple basique avec Hydra pour authentification via un formulaire web :

```bash
hydra -l votre_nom_utilisateur -p votre_mot_de_passe www.monsiteperso.com http-form-post "/chemin_du_formulaire:champ_username=^USER^&champ_password=^PASS^:Erreur d'authentification"
```

Ensuite, une fois que vous avez obtenu l'accès, vous pouvez utiliser nmap pour scanner les pages internes en fournissant les cookies de session si nécessaire.