---
tags: [obsidian, plugins, automation, workflow]
---
### Utiliser des Plugins Obsidian pour l'Automatisation
Certaines fonctionnalités d'automatisation peuvent être implémentées directement dans Obsidian en utilisant des plugins comme Templater ou Dataview.

#### Exemple avec Templater
Templater permet d'automatiser la création de notes avec des scripts.

```markdown
<%*
const { execSync } = require('child_process');
const result = execSync('python chemin/vers/votre/script.py').toString();
tR += result;
%>
```