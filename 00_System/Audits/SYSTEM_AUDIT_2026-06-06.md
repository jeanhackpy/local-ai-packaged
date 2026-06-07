# 🔍 Audit Système Mac — Pre-Oracle VPS Setup
*Date : 2026-06-06 | Objectif : état propre avant configuration Oracle VPS*

---

## 1. 🔌 MCP Servers (Claude Desktop)

**Config** : `~/Library/Application Support/Claude/claude_desktop_config.json`

| Serveur | Package | Auth | État |
|:---|:---|:---|:---|
| cloudflare | `@cloudflare/mcp-server-cloudflare` | Wrangler OAuth | ✅ Fixé (session 2026-06-06) |
| google | `ga4-mcp` | gcloud ADC (palanthai client) | ✅ Fixé (APIs activées) |
| obsidian | `@mauricio.wolff/mcp-obsidian` | Filesystem | ✅ OK |

**⚠️ Zombie processes identifiés** (anciens MCPs toujours en RAM depuis sessions précédentes) :
- `mcp-server-ga4` × 3 instances mortes
- `mcp-server-gsc` × 1 instance morte
- `mcp-server-cloudflare` × 2 anciennes instances

→ **Action** : Redémarrer Claude Desktop pour nettoyer. Les process orphelins meurent au prochain reboot.

---

## 2. 📡 SSH Tunnel VPS (autossh)

**LaunchAgent** : `com.palanthai.vps-tunnel` — `KeepAlive=true`, démarre au login
**Tunnel** : `autossh → phil@31.97.67.145`

| Port local | Service VPS | État |
|:---|:---|:---|
| `localhost:6333` | Qdrant (Vector DB) | ✅ LISTEN |
| `localhost:7474` | Neo4j HTTP | ✅ LISTEN |
| `localhost:7687` | Neo4j Bolt | ✅ LISTEN |
| `localhost:18789` | ? (à identifier) | ✅ LISTEN |
| `localhost:8000` | API / backend | ✅ LISTEN |
| `localhost:8765` | ? | ✅ LISTEN |
| `localhost:5678` | n8n | ✅ LISTEN |

**Log** : `/tmp/vps-tunnel.log`

---

## 3. ⏰ LaunchAgents (~/Library/LaunchAgents/)

| Label | Commande | Intervalle | État |
|:---|:---|:---|:---|
| `com.palanthai.vps-tunnel` | autossh → 31.97.67.145 | KeepAlive | ✅ Running |
| `com.phil.palanthai-kanban` | `python3 sync-palanthai-kanban.py` | 5 min | ✅ Running |
| `com.phil.sync-obsidian-systemmac` | `sync-obsidian-systemmac.sh` | 60 min | ⚠️ Exit 127 (script introuvable ?) |
| `homebrew.mxcl.syncthing` | syncthing --no-browser | KeepAlive | ⚠️ none (brew service stopped) |
| `com.dropbox.DropboxUpdater.wake` | Dropbox updater | macOS géré | 💤 Passif |
| `com.github.domt4.homebrew-autoupdate` | brew autoupdate | macOS géré | 💤 Passif |
| `com.google.keystone.agent` | Google Updater | macOS géré | 💤 Passif |

**⚠️ Action requise** : `com.phil.sync-obsidian-systemmac` a exit code 127 (commande introuvable). Vérifier le script `/Users/phil/scripts/sync-obsidian-systemmac.sh`.

---

## 4. ⏲️ Cron Jobs (crontab -l)

```
0 * * * *   /Users/phil/Documents/Vaults/SystemMac/00_System/Scripts/sync_obsidian_links.sh
0 0 * * *   /Users/phil/Documents/Vaults/SystemMac/00_System/Maintenance/mac_health_check.sh
0 3 1 * *   /Users/phil/Documents/Vaults/SystemMac/00_System/Maintenance/super_clean.sh
0 * * * *   /Users/phil/Scripts/sync_obsidian_leon.sh
0 * * * *   /Users/phil/Scripts/sync-obsidian-systemmac.sh
```

**Note** : Doublon détecté — `sync-obsidian-systemmac` tourne à la fois en cron ET en LaunchAgent. Choisir l'un ou l'autre.

---

## 5. 🍺 Brew Services

| Service | État |
|:---|:---|
| ollama | ⬜ none (non démarré comme service) |
| syncthing | ⬜ none (non démarré comme service) |
| tailscale | ⬜ none (root service, géré séparément) |

**Note** : Ollama et Syncthing sont installés via Homebrew mais tournent via LaunchAgents, pas via `brew services`.

---

## 6. 🌐 Ports en écoute (localhost)

| Port | Process | Rôle |
|:---|:---|:---|
| 50141, 63035 | Antigravity (Google) | Gemini MCP stack |
| 50145, 50146 | language_server | LSP (probablement Cursor/VSCode) |
| 61448 | Bitwarden | IPC local |
| 32222, 63255 | OrbStack | Docker/VM management |
| 6333 | ssh (tunnel) | Qdrant VPS |
| 7474 | ssh (tunnel) | Neo4j HTTP VPS |
| 7687 | ssh (tunnel) | Neo4j Bolt VPS |
| 18789 | ssh (tunnel) | ? VPS |
| 8000 | ssh (tunnel) | API VPS |
| 8765 | ssh (tunnel) | ? VPS |
| 5678 | ssh (tunnel) | n8n VPS |

---

## 7. 📱 Apps avec LaunchAgents système actifs

| App | Label launchd | Rôle |
|:---|:---|:---|
| Antigravity (Google AI) | `application.com.google.antigravity.*` | Gemini / MCP stack |
| Claude Desktop | `application.com.anthropic.claudefordesktop.*` | Claude + MCPs locaux |
| Chrome | `application.com.google.Chrome.*` | Browser |
| OrbStack | `dev.kdrag0n.MacVirt.*` | Docker/VMs |
| Bitwarden | `application.com.bitwarden.desktop.*` | Password manager |
| NI Hardware | `com.native-instruments.NIHardwareService.*` | Audio hardware |

---

## 8. 🤖 Stack MCP Antigravity (Gemini CLI — séparé de Claude Desktop)

MCPs actifs dans Antigravity (ports 50141/63035) :
- `mcp-remote https://stitch.googleapis.com/mcp` (API Key)
- Jules (Google AI coding agent)
- context7 (docs MCP)
- hostinger-api-mcp
- chrome-devtools-mcp
- genkit
- obsidian (custom)

**Important** : Stack totalement indépendante de Claude Desktop. Pas d'interférence.

---

## 9. 🔧 Actions recommandées avant Oracle VPS

### Critiques
- [ ] **Fix `com.phil.sync-obsidian-systemmac` (exit 127)** : vérifier si le script existe à l'emplacement référencé
- [ ] **Supprimer doublon cron/launchagent** pour sync-obsidian-systemmac
- [ ] **Redémarrer Claude Desktop** pour tuer les zombies MCP (ga4 ×3, gsc ×1)
- [ ] **Identifier port 18789** sur le VPS (`ss -tlnp | grep 18789`)

### Optionnelles
- [ ] **Activer GitHub MCP** : image `ghcr.io/github/github-mcp-server:latest` déjà dans OrbStack → besoin GitHub PAT + entrée dans `claude_desktop_config.json`
- [ ] **Documenter port 8765** sur VPS (probablement Ollama API ou custom)

---

## 10. 📋 Résumé état global

| Composant | État |
|:---|:---|
| MCPs Claude Desktop | ✅ 3/3 fonctionnels (fixés le 2026-06-06) |
| Tunnel SSH VPS | ✅ Actif + persistant (autossh KeepAlive) |
| Cron jobs | ✅ 5 jobs actifs (1 doublon à nettoyer) |
| LaunchAgents | ⚠️ 1 agent en erreur (exit 127) |
| Brew services | ✅ Ollama/Syncthing gérés via agents |
| OrbStack | ✅ Actif (image GitHub MCP disponible) |
| Antigravity/Gemini | ✅ Stack séparée, fonctionnelle |
| Ports VPS exposés | ✅ Qdrant, Neo4j, n8n, API accessibles localement |
