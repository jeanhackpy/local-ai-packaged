### Création d'un Environnement Virtuel dans Python

**Environnements virtuels** sont des outils permettant de créer des environnements isolés pour des projets Python. Voici les avantages et le fonctionnement de ces environnements :

1. **Isolation des Dépendances :**
   - Permet d'installer des paquets spécifiques à un projet sans affecter les autres projets ou le système global.
   - Par exemple, vous pouvez avoir deux projets utilisant différentes versions d'une même bibliothèque sans conflit.

2. **Facilité de Gestion :**
   - Simplifie la gestion des dépendances et rend les projets plus portables.
   - Facilite la reproduction de l'environnement de développement sur d'autres machines.

3. **Création et Activation :**
   - Vous créez un environnement virtuel en utilisant `venv` ou `virtualenv` :
     ```bash
     python3 -m venv myenv
     ```
   - Vous l'activez ensuite :
     ```bash
     source myenv/bin/activate
     ```

4. **Persistance des Environnements :**
   - Les environnements virtuels sont persistants sur le système tant que vous ne les supprimez pas explicitement.
   - Ils sont stockés dans des répertoires spécifiques (par exemple, `myenv/`) et contiennent leurs propres copies de l'interpréteur Python et des bibliothèques.

5. **Désactivation :**
   - Vous pouvez désactiver un environnement virtuel en utilisant la commande `deactivate` :
     ```bash
     deactivate
     ```
   - Cela ne supprime pas l'environnement ; il reste sur votre disque dur jusqu'à ce que vous décidiez de le supprimer.