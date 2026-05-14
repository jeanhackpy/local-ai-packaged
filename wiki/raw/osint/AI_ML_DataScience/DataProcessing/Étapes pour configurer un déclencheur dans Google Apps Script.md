### Étapes pour configurer un déclencheur dans Google Apps Script

1. **Ouvrir le projet Apps Script :**
   - Allez dans votre Google Sheet.
   - Cliquez sur `Extensions` > `Apps Script` pour ouvrir l'éditeur de script.

2. **Ajouter la fonction `setupTrigger` :**
   - Assurez-vous que la fonction `setupTrigger` est présente dans votre script. Voici à quoi elle ressemble dans le script fourni :

```javascript
function setupTrigger() {
  ScriptApp.newTrigger('extractIncomingGmailData')
    .forTimeDriven()
    .everyMinutes(5)
    .create();
}
```

3. **Exécuter la fonction `setupTrigger` :**
   - Dans l'éditeur de script, trouvez la barre d'outils en haut.
   - Sélectionnez `setupTrigger` dans le menu déroulant à côté de l'icône de lecture (triangle).
   - Cliquez sur l'icône de lecture pour exécuter la fonction `setupTrigger`.

4. **Autorisation :**
   - La première fois que vous exécutez cette fonction, Google vous demandera de l'autoriser à accéder à votre Gmail et Google Drive.
   - Cliquez sur `Review Permissions`, sélectionnez votre compte Google, et cliquez sur `Allow` pour autoriser l'accès.

5. **Vérifier le déclencheur :**
   - Après avoir exécuté la fonction `setupTrigger`, vous pouvez vérifier que le déclencheur a été correctement configuré.
   - Allez dans `Triggers` (Déclencheurs) en cliquant sur l'icône de l'horloge dans l'éditeur de script ou en allant dans `Edit` > `Current project's triggers` (Modifier > Déclencheurs du projet actuel).
   - Vous devriez voir un déclencheur pour la fonction `extractIncomingGmailData` configuré pour s'exécuter toutes les 5 minutes.