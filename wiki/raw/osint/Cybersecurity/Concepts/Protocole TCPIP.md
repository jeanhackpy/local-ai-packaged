### Protocole TCP/IP

Le protocole TCP/IP (Transmission Control Protocol/Internet Protocol) est la suite de protocoles fondamentaux de l'Internet. Il est utilisé pour transmettre des données entre des ordinateurs sur un réseau et assure que ces données arrivent intactes et dans l'ordre correct. TCP/IP est divisé en quatre couches principales, chacune ayant un rôle spécifique.

#### 1. Couches du Modèle TCP/IP

1. **Couche d'accès réseau (Network Interface Layer)** :
   - **Fonction**: Gère les détails physiques de la communication avec le réseau. Cela inclut l'interface matérielle, les pilotes de périphériques, etc.
   - **Protocole**: Ethernet, Wi-Fi, etc.

2. **Couche Internet (Internet Layer)** :
   - **Fonction**: Gère l'adressage, l'acheminement des paquets de données entre les hôtes et les sous-réseaux.
   - **Protocole**: IP (Internet Protocol), ICMP (Internet Control Message Protocol), ARP (Address Resolution Protocol).

3. **Couche de transport (Transport Layer)** :
   - **Fonction**: Assure la transmission fiable des données entre les applications sur les hôtes de bout en bout.
   - **Protocole**: TCP (Transmission Control Protocol) pour une communication fiable, UDP (User Datagram Protocol) pour une communication non fiable mais rapide.

4. **Couche application (Application Layer)** :
   - **Fonction**: Gère les protocoles de haut niveau utilisés par les applications pour fournir divers services de réseau.
   - **Protocole**: HTTP (HyperText Transfer Protocol), FTP (File Transfer Protocol), SMTP (Simple Mail Transfer Protocol), etc.