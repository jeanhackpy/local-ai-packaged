---
tags: [obsidian, workflow, fabric, zettelkasten, knowledge-management, productivity]
---
### 5. Utilisation du Modèle dans Vos Notes
1. Pour créer une nouvelle note en utilisant le modèle Fabric, ouvrez une nouvelle note dans Obsidian.
2. Utilisez la commande **Templater** (`Ctrl + P` ou `Cmd + P` sur Mac) pour insérer un modèle.
3. Recherchez et sélectionnez votre modèle `fabric-template.md`.

### 6. Analyse des Notes avec Dataview
Utilisez Dataview pour extraire et analyser les informations de vos notes structurées avec le framework Fabric. Vous pouvez créer des vues, des tableaux, ou des listes basées sur vos critères.

**Exemple de vue Dataview pour l'analyse** :
```markdown
```dataview
list from "Notes"
where contains(tags, "#fabric") and date(today) - file.ctime <= dur(7 days)
sort file.ctime desc
```
```

Cette requête affiche une liste des notes créées dans les 7 derniers jours et marquées avec le tag `#fabric`.

En suivant ces étapes, vous pourrez efficacement utiliser le framework Fabric dans Obsidian pour structurer et analyser vos notes.

User

Connais tu d autre projet comme fabric 

ChatGPT

Oui, il existe plusieurs frameworks et méthodologies similaires à Fabric qui peuvent être utilisés pour organiser et analyser des notes dans Obsidian. Voici quelques-uns des plus populaires :

### 1. **Zettelkasten**
Le Zettelkasten (boîte à fiches) est une méthode de prise de notes développée par le sociologue allemand Niklas Luhmann. Elle repose sur la création de notes interconnectées par des liens, ce qui permet de créer un réseau de connaissances.

**Principes de base :**
- Chaque note doit être autonome et contenir une seule idée.
- Les notes sont reliées entre elles par des liens, formant ainsi un réseau.
- Utilisation d'identifiants uniques pour chaque note.

**Exemple de structure de note :**
```markdown
---
tags: [zettelkasten]
---