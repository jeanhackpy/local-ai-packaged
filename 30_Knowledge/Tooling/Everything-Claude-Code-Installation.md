---
tags: [tooling, claude-code, antigravity, gemini-cli, automation]
date: 2026-03-19
---

# Everything Claude Code (ECC) Installation

Ce document détaille l'installation du dépôt [everything-claude-code](https://github.com/affaan-m/everything-claude-code) effectuée le 19 mars 2026 pour optimiser les performances des agents **Claude Code** et **Antigravity (Gemini CLI)**.

## 📦 Détails de l'installation

- **Source :** `https://github.com/affaan-m/everything-claude-code`
- **Langages supportés :** TypeScript, Python, Golang.
- **Dossier temporaire de clonage :** `/Users/phil/.gemini/tmp/phil/everything-claude-code`

## 🎯 Cibles configurées

### 1. Claude Code
Le script d'installation a été exécuté avec la cible `--target claude`.
- **Emplacement :** `~/.claude/`
- **Composants :** Règles (rules), Agents (agents), et Workflows (commands) ont été copiés dans ce répertoire pour une utilisation native par Claude Code.

### 2. Antigravity (Gemini CLI)
Le script d'installation a été exécuté avec la cible `--target antigravity`.
- **Emplacement :** `~/.agent/` et `~/.agents/skills/`
- **Règles et Workflows :** Installés dans `/Users/phil/.agent/`.
- **Skills :** Installés dans `/Users/phil/.agents/skills/` (ex: TDD, Security Review, API Design).

## 🚀 Fonctionnalités activées

### Agents spécialisés
- **Architect :** Conception système et architecture logicielle.
- **Code Reviewer :** Revue de code automatisée.
- **Security Reviewer :** Audit de sécurité et conformité.
- **TDD Guide :** Accompagnement pour le Test-Driven Development.

### Règles (Rules)
Plus de 50 fichiers de règles (`.md`) sont désormais disponibles pour guider le comportement de l'IA sur :
- Les standards de codage (TypeScript, Python, Go, Swift, PHP, Rust, etc.).
- Le workflow Git.
- La sécurité et la performance.

## 🛠️ Maintenance et Mise à jour

Pour mettre à jour les composants ECC, se rendre dans le répertoire source et relancer le script d'installation :
```bash
cd /Users/phil/.gemini/tmp/phil/everything-claude-code
git pull
./install.sh --target claude typescript python golang
./install.sh --target antigravity typescript python golang
```

---
*Document généré par Gemini CLI.*