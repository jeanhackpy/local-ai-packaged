### Script de tâche

Créez un fichier `task_script.sh` pour définir les tâches spécifiques.

```bash
#!/bin/bash
# Script de tâche exemple
echo "Tâche exécutée avec succès" >> /home/llmuser/task_log.txt
logger -t task_script 'Tâche exécutée'
```