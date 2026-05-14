### Étapes pour tester la vulnérabilité SQL Injection

#### 1. **Collecte d'informations**
Avant de commencer les tests d'injection SQL, il est essentiel de collecter des informations sur les formulaires de saisie, les paramètres URL, et autres points d'entrée de l'application web.

#### 2. **Tests manuels**
Les tests manuels peuvent souvent détecter des vulnérabilités SQL que les outils automatisés manquent. Voici quelques techniques manuelles :

- **Injection basique dans les paramètres URL ou les formulaires** :
  - Ajoutez `' OR '1'='1` ou `";--` aux paramètres de l'URL ou aux champs de formulaire pour voir si des erreurs SQL apparaissent.
  - Exemple : `http://example.com/index.php?id=1' OR '1'='1`

- **Observation des messages d'erreur** :
  - Les messages d'erreur SQL détaillés peuvent révéler une vulnérabilité. Essayez des entrées comme `"'` ou `" OR 1=1;--` pour déclencher une erreur.

#### 3. **Utilisation d'outils automatisés**
Les outils automatisés peuvent effectuer des tests complets et rapides sur l'ensemble de l'application web.

- **SQLmap** : Un outil puissant pour détecter et exploiter les vulnérabilités SQL.
  - **Commande de base** :
    ```sh
    sqlmap -u "http://example.com/index.php?id=1" --batch
    ```
  - **Commande avec données POST** :
    ```sh
    sqlmap -u "http://example.com/login.php" --data="username=admin&password=admin" --batch
    ```
  - **Options utiles** :
    - `--dbs` : Pour lister les bases de données disponibles.
    - `--tables` : Pour lister les tables d'une base de données spécifique.
    - `--columns` : Pour lister les colonnes d'une table spécifique.

- **OWASP ZAP (Zed Attack Proxy)** : Un proxy qui aide à détecter les vulnérabilités dans les applications web, y compris les injections SQL.
  - Utilisez l'option d'analyse active pour rechercher automatiquement les vulnérabilités SQL.

- **Burp Suite** : Une plateforme complète pour les tests de sécurité des applications web.
  - Utilisez l'outil Intruder pour tester les points d'injection avec des charges utiles malveillantes.
  - Utilisez le scanner pour détecter automatiquement les vulnérabilités SQL.

#### 4. **Analyse et exploitation**
Une fois une vulnérabilité détectée, vous pouvez l'exploiter pour récupérer des informations sensibles de la base de données.

- **Extraction de données** : Utilisez des commandes comme `UNION SELECT` pour extraire des données de la base de données.
  - Exemple : `http://example.com/index.php?id=1 UNION SELECT username, password FROM users`

- **Bypass authentification** : Utilisez des payloads comme `' OR '1'='1` pour contourner les formulaires de connexion.