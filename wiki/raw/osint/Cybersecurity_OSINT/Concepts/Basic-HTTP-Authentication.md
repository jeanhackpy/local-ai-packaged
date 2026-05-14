---
tags: [osint, security, http-authentication, nmap, concept]
---

### 1. Authentification HTTP basique
Si le site utilise une authentification HTTP basique (c'est-à-dire une boîte de dialogue du navigateur demandant un nom d'utilisateur et un mot de passe), vous pouvez utiliser les options `--script http-auth` et `--script-args` pour fournir vos informations d'identification. Par exemple :

```bash
nmap -A -T4 -p- --script http-auth --script-args http-auth.hostname=www.monsiteperso.com,http-auth.username=votre_nom_utilisateur,http-auth.password=votre_mot_de_passe www.monsiteperso.com
```