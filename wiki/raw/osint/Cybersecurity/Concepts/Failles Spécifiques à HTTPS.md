### Failles Spécifiques à HTTPS

1. **Attaques Man-in-the-Middle (MitM)** :
   - **Description** : Un attaquant intercepte les communications entre le client et le serveur pour espionner ou altérer les données transmises.
   - **Impact** : Peut compromettre des informations sensibles, même si elles sont chiffrées.
   - **Mitigation** : Utilisation de certificats SSL/TLS valides et de la vérification rigoureuse des certificats côté client.

2. **Certificats SSL/TLS Compromis** :
   - **Description** : Si une autorité de certification (CA) est compromise, des certificats peuvent être émis de manière frauduleuse.
   - **Impact** : Permet aux attaquants de mener des attaques MitM et de se faire passer pour des sites légitimes.
   - **Mitigation** : Utilisation de mécanismes comme Certificate Transparency et de politiques de sécurité strictes pour les CAs.

3. **Attaques sur les Protocoles SSL/TLS** :
   - **Description** : Les anciennes versions et certaines configurations de SSL/TLS présentent des vulnérabilités, telles que POODLE, BEAST, CRIME, et Heartbleed.
   - **Impact** : Peut permettre aux attaquants de déchiffrer le trafic ou d'exploiter des failles dans la négociation du chiffrement.
   - **Mitigation** : Utilisation de versions récentes de TLS (comme TLS 1.2 ou TLS 1.3) et des configurations sécurisées.

4. **Attaques de Downgrade** :
   - **Description** : Forcer un client et un serveur à utiliser une version ou une suite cryptographique moins sécurisée.
   - **Impact** : Rend les communications vulnérables aux attaques connues sur ces versions ou suites.
   - **Mitigation** : Utilisation de mécanismes comme HTTP Strict Transport Security (HSTS) et la désactivation des protocoles et suites cryptographiques obsolètes.

5. **Certificat Self-Signed ou Invalide** :
   - **Description** : Utilisation de certificats auto-signés ou invalides qui ne sont pas reconnus par les navigateurs.
   - **Impact** : Peut entraîner une fausse impression de sécurité et permettre des attaques MitM.
   - **Mitigation** : Utilisation de certificats émis par des CAs fiables et reconnus.