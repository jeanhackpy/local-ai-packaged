### Failles Connues du Protocole TCP/IP

#### Failles au Niveau IP

1. **IP Spoofing**:
   - **Description**: Un attaquant envoie des paquets en utilisant une adresse IP source falsifiée pour masquer son identité.
   - **Impact**: Peut être utilisé pour détourner des sessions ou lancer des attaques par déni de service.

2. **Fragmentation Attacks**:
   - **Description**: Manipule les fragments de paquets pour contourner les mécanismes de sécurité tels que les pare-feu.
   - **Impact**: Permet aux paquets malveillants de pénétrer des réseaux sécurisés.

#### Failles au Niveau TCP

1. **SYN Flooding**:
   - **Description**: Envoie un grand nombre de requêtes SYN pour établir des connexions TCP, mais ne complète jamais le handshake.
   - **Impact**: Épuise les ressources du serveur, provoquant un déni de service (DoS).

2. **TCP Session Hijacking**:
   - **Description**: Un attaquant intercepte ou injecte des paquets dans une session TCP établie en devinant les numéros de séquence.
   - **Impact**: Permet à l'attaquant de prendre le contrôle d'une session de communication active.

3. **RST Injection**:
   - **Description**: Envoie des paquets TCP avec le drapeau RST (Reset) pour terminer une connexion TCP active.
   - **Impact**: Perturbe les communications entre les hôtes.

#### Failles au Niveau de la Couche Application

1. **Man-in-the-Middle (MitM)**:
   - **Description**: Un attaquant intercepte et éventuellement modifie les communications entre deux parties sans qu'elles s'en aperçoivent.
   - **Impact**: Peut entraîner la compromission des données sensibles échangées.