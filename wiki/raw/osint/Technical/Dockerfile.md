### Dockerfile

Créez un fichier `Dockerfile` pour définir l'image Docker.

```Dockerfile
# Utilisez une image de base compatible avec Raspberry Pi (ARM architecture)
FROM python:3.9-slim

# Mettre à jour le système et installer les dépendances nécessaires
RUN apt-get update && apt-get install -y \
    sudo \
    && rm -rf /var/lib/apt/lists/*

# Installer les bibliothèques Python nécessaires
RUN pip install transformers torch

# Ajouter un utilisateur non-root pour la sécurité
RUN useradd -ms /bin/bash llmuser
RUN echo 'llmuser ALL=(ALL) NOPASSWD: /usr/local/bin/task_script.sh' >> /etc/sudoers

# Copier le script de tâche dans l'image Docker
COPY task_script.sh /usr/local/bin/task_script.sh
RUN chmod +x /usr/local/bin/task_script.sh

# Copier le fichier de serveur Python dans l'image Docker
COPY server.py /usr/local/bin/server.py

# Définir l'utilisateur courant
USER llmuser

# Exposer le port pour le serveur HTTP
EXPOSE 8080

# Commande d'entrée pour démarrer le serveur
CMD ["python3", "/usr/local/bin/server.py"]
```