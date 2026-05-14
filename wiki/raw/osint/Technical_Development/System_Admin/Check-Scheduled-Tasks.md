---
tags: [technical-development, system-admin, cron, launchd, macos]
---
### Vérifier les Tâches Planifiées
Il est possible qu'un script ait été exécuté via une tâche planifiée. Sur macOS, cela peut être géré via `cron` ou `launchd`.

- **Vérifier les tâches cron :**
  ```bash
  crontab -l
  ```
  - Cette commande liste les tâches planifiées par l'utilisateur actuel.

- **Vérifier les fichiers de lancement `launchd` :**
  - Les fichiers de lancement pour l'utilisateur se trouvent dans `~/Library/LaunchAgents` et pour tout le système dans `/Library/LaunchAgents` et `/Library/LaunchDaemons`.
  ```bash
  ls ~/Library/LaunchAgents
  ls /Library/LaunchAgents
  ls /Library/LaunchDaemons
  ```