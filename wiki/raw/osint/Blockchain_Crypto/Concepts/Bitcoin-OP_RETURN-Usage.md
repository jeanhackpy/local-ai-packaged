---
tags: [blockchain, bitcoin, op-return, data-storage, concept]
---

### 1. Utilisation de Bitcoin OP_RETURN

**OP_RETURN** est une opération dans le langage de script de Bitcoin qui permet de stocker une petite quantité de données (actuellement jusqu'à 80 bytes) directement dans une transaction Bitcoin. Voici comment cela pourrait être fait :

#### Étapes :
1. **Création d'une transaction Bitcoin :**
   - Créez une transaction Bitcoin avec une sortie qui utilise l'OP_RETURN pour inclure les données Markdown.

2. **Inclusion des données :**
   - En raison de la limitation de taille (80 bytes), seules des portions très petites du Markdown peuvent être incluses directement. Pour des fichiers plus grands, vous devrez segmenter les données en plusieurs transactions.

3. **Broadcast de la transaction :**
   - Envoyez la transaction à la blockchain Bitcoin.

#### Considérations :
- **Coût :** Chaque transaction coûte des frais de transaction Bitcoin, et segmenter un fichier en plusieurs transactions peut devenir coûteux.
- **Persistance :** Les données stockées de cette manière sont immuables et persistantes.