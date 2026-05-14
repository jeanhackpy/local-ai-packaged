---
tags: [cybersecurity, tool, hping3, ddos, network-analysis]
---
### Hping3
**Description**: Hping3 est un outil de manipulation et d'analyse de paquets TCP/IP qui peut être utilisé pour des attaques DDoS, notamment en envoyant des paquets TCP SYN pour inonder une cible.

**Utilisation**:
- **Commande de base**: `hping3 -S -p 80 --flood example.com`
- **Options**: Supporte l'envoi de paquets ICMP, UDP, TCP et la personnalisation des flags.