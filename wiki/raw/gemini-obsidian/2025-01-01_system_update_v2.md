# Journal de maintenance - 1er Janvier 2025 01:17 (Mise à jour v2)

## Mise à jour de la configuration des serveurs MCP

### Modifications effectuées
- Retrait des serveurs propriétaires (OpenAI, Anthropic)
- Ajout du serveur Ollama pour l'intégration des modèles open source :
  - Support pour Qwen, Deepseek et autres modèles open source
  - Configuration par défaut avec Qwen 7B
  - Port 8002 pour le serveur Ollama

### Prérequis d'installation
1. Ollama doit être installé sur le système
2. Les modèles suivants doivent être téléchargés via Ollama :
   ```bash
   ollama pull qwen:7b
   ```

### Configuration du serveur Ollama
- Host : http://localhost:11434
- Modèle par défaut : qwen:7b
- Port du serveur MCP : 8002

### Actions requises
- [ ] Installer Ollama si ce n'est pas déjà fait
- [ ] Télécharger les modèles nécessaires
- [ ] Vérifier que le port 11434 est accessible pour Ollama
- [ ] Tester la connexion avec le serveur MCP
- [ ] Valider l'intégration avec Qdrant pour le stockage vectoriel

### Notes techniques
- Privilégier les modèles quantifiés pour optimiser les performances
- Possible d'ajouter d'autres modèles open source selon les besoins
- Les embeddings restent gérés par sentence-transformers via Qdrant

### Rappel de la stack open source
- Qdrant : Stockage et recherche vectorielle
- Ollama : Inférence des modèles de langage
- sentence-transformers : Génération d'embeddings
