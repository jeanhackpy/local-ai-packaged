---
tags: [technical-development, file-system, analysis, macos]
---
### Analyser les Changements Réalisés
Vous pouvez également vérifier les métadonnées des fichiers ajoutés pour voir quand et comment ils ont été créés ou modifiés.

- **Vérifier les dates de modification des fichiers :**
  ```bash
  ls -lR /chemin/vers/votre/dossier/Obsidian
  ```

- **Vérifier les métadonnées des fichiers :**
  ```bash
  stat /chemin/vers/votre/dossier/Obsidian/*
  ```