# 🔐 03 - Security Configuration

**Part of:** [[SystemPolicy]]  
**Related:** [[README]], [[Development/VPS Hostinger & WordPress]]

## Security Best Practices

This document outlines security configuration and best practices.

## System Security

- FileVault full disk encryption enabled
- Firewall configured with strict rules (see [[Development/VPS Hostinger & WordPress#Security Management]])
- Automatic security updates enabled
- Gatekeeper configured for app installation

## Credential Management

- Bitwarden as primary password manager
- SSH keys properly secured (see [[Development/VPS Hostinger & WordPress#SSH Hardening]])
- API keys stored in secure locations (e.g., for [[Infra/VPS_Hostinger/Plan_Action_Monitoring#2-Intégration-Hostinger-MCP]])
- Two-factor authentication enabled for all accounts

## Development Security Practices

- Regular updates of all development tools
- Secure storage of API keys and credentials
- Isolated development environments
- Regular backups of development work

## Network Security

- VPN usage for public networks
- SSH key-based authentication only
- Regular port scanning and monitoring
- Certificate pinning for critical services

## Application Security

- Regular updates of all applications
- Code signing verification
- Sandbox permissions review
- Malware scanning and prevention (see [[Infra/VPS_Hostinger/VPS_Exploration_2026-01-27#Monarx Malware Scanner]])
