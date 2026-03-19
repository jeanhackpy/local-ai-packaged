# 🛠️ AI Tools & IDE Optimization Guide

*Ce document répertorie les extensions, plugins et configurations pour maximiser les capacités de vos outils d'IA selon votre stack (Hostinger, n8n, Supabase).*

## 🤖 Claude Code (CLI Agent)
**Usage :** Orchestration terminal, maintenance VPS, debug rapide.
- **Extensions (MCP Servers) :**
  - `Filesystem MCP` : Pour accéder à `/Users/phil/Documents/AppsData`.
  - `Memory MCP` : Persistance du contexte entre les sessions.
  - `GitHub MCP` : Gestion native de vos 234 dépôts.
- **Skills & Tools :**
  - Import direct de vos scripts Python (`~/.agents/skills`).
  - Capacité à exécuter `super_clean.sh` sur demande.

## 🚀 Cursor (AI-Powered IDE)
**Usage :** Développement lourd (TypeScript, React, Python).
- **Configurations Cruciales :**
  - `.cursorrules` : Doit pointer vers `40_Context_Hub/AGENT_INSTRUCTIONS.md`.
  - **Indexation Docs** : Ajouter les URLs `https://docs.qdrant.tech` et `https://supabase.com/docs`.
- **Extensions VS Code Recommandées :**
  - `Docker` : Gestion des containers du VPS.
  - `Tailwind CSS IntelliSense` : Pour vos projets 3D.
  - `REST Client` : Pour tester les APIs Hostinger et n8n directement.

## 🏄‍♂️ Windsurf (Agentic IDE)
**Usage :** Flux de travail autonomes ("Flows").
- **Points Forts :**
  - **Context-Aware Indexing** : Très performant sur votre dossier `Pipeline`.
  - **Native MCP Support** : Permet de lier directement votre base de données Supabase pour générer du code SQL/Typescript précis.

## 🌌 Antigravity (Browser-Based Agent)
**Usage :** Automatisation web, Monitoring UI de vos sites Hostinger, n8n UI.
- **Capacités :**
  - **Computer Use** : Interaction avec les applications macOS locales.
  - **Web Navigation** : Audit visuel de vos 3 sites web.
  - **Ollama Integration** : Utilisation de modèles locaux pour le traitement de données sensibles.

## 🛠 Codex & Agentic Skills Repo
**Usage :** Votre "Usine à Agents" personnalisée.
- **Moteurs d'Action :**
  - `Crawl4AI` : Transformation massive de sites en Markdown.
  - `MCP-Toolbox` : Conversion de vos scripts Python (`rato-sequencer-condominium`) en outils utilisables par Claude Code ou Windsurf.
  - `LlamaIndex` / `LangChain` : Frameworks de mémoire pour vos scripts d'ingestion.

---
## 🎯 Matrice de Décision (Quel outil utiliser ?)
| Tâche | Outil Recommandé | Raison |
| :--- | :--- | :--- |
| **Coder une UI 3D** | `Cursor` / `Windsurf` | IntelliSense, Preview, Debugger |
| **Lancer un Crawl VPS** | `Claude Code` | Rapidité terminal, accès SSH direct |
| **Configurer n8n UI** | `Antigravity` | Navigation web autonome |
| **Audit SEO/Perf** | `Gemini CLI` | Skill `debug-optimize-lcp` et `chrome-devtools` |

---

## 🧪 Google Jules (Autonomous Coding Agent)
**Usage :** Refactoring massif, correction de bugs asynchrone, revue de code.
- **Points Forts :**
  - **Critic-Augmented Generation** : Effectue une auto-revue critique avant de soumettre du code (adversarial review).
  - **Asynchrone** : Travaille en arrière-plan sur des tâches complexes (ex: "Migrer tout le projet vers Node 20").
  - **Vérification native** : Lance des tests unitaires dans un environnement cloud sécurisé avant d'ouvrir une PR.
- **Configuration :**
  - Utilise le fichier `AGENTS.md` à la racine du repo GitHub pour comprendre les conventions du projet.

---
*Dernière mise à jour : 2026-03-11*
