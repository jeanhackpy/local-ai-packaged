### Analyse des Fonctionnalités

1. **Propriétaire Initial :**
   - Le propriétaire initial du contrat est l'adresse qui déploie le contrat. Ceci est défini dans le constructeur.

2. **Modificateur `onlyOwner` :**
   - Ce modificateur garantit que seules les fonctions appelées par l'adresse propriétaire peuvent être exécutées.

3. **Fonctions de Gestion de la Propriété :**
   - `owner()`: Retourne l'adresse du propriétaire actuel.
   - `renounceOwnership()`: Permet au propriétaire actuel de renoncer à la propriété, laissant le contrat sans propriétaire.
   - `transferOwnership(address newOwner)`: Transfère la propriété à une nouvelle adresse.

4. **Événement `OwnershipTransferred` :**
   - Cet événement est émis chaque fois que la propriété est transférée, fournissant une traçabilité des changements de propriété.