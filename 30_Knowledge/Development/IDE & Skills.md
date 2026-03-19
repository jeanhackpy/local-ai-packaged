# 💻 IDE & Skills Configuration

**Part of:** [[README]]  
**Related:** [[Agents]], [[Scripts]]

## 🛠️ Installed IDEs

| IDE | Path | Primary Use |
|-----|------|-------------|
| Cursor | ~/.cursor/ | Main agentic coding assistant |
| VS Code | /Applications/Visual Studio Code.app | General development |
| Antigravity | ~/.gemini/antigravity/ | Google agentic IDE |
| OpenCode | ~/Applications/OpenCode/ | Alternative AI IDE |
| Claude Code | CLI tool | Anthropic agentic CLI |

## 🧠 Agentic Skills Repository

**Main Repository:** [sickn33/antigravity-awesome-skills](https://github.com/sickn33/antigravity-awesome-skills)

### Skills Locations:
- **Cursor:** `~/.cursor/skills/` (227 skills)
- **Antigravity:** `~/.gemini/antigravity/skills/` (222 skills)
- **VS Code Fallback:** `~/.agent/skills/antigravity-awesome-skills`

### Recommended Symlink Setup:
```bash
ln -s ~/.agent/skills/antigravity-awesome-skills ~/.cursor/skills/
ln -s ~/.agent/skills/antigravity-awesome-skills ~/.gemini/antigravity/skills/
```

## 🔌 Recommended Extensions

### Essential Extensions:
- **Remote - SSH** → VPS connection
- **Python (Microsoft)** → Python development
- **GitLens** → Advanced Git history
- **Markdown All in One** → Markdown editing
- **Prettier** → Code formatting
- **ESLint** → JavaScript/TypeScript linting
- **Tailwind CSS IntelliSense** → Tailwind support
- **Docker** → Container management

## ⚡ AI Coding Assistants

| Assistant | Type | Access | Related Docs |
|----------|------|--------|--------------|
| Cursor | Desktop App + Skills | ~/.cursor/ | [[ClaudeCode CLI]] |
| Antigravity | Desktop App + Skills | ~/.gemini/antigravity/ | [[Gemini CLI]] |
| Claude Code | CLI Tool | Terminal command | [[ClaudeCode CLI]] |
| Continue.dev | VS Code Extension | Extension marketplace | [[Ollama]] |
| GitHub Copilot | VS Code Extension | Extension marketplace | [[Ollama]] |

## 🔧 Development Environment

### Python Setup
- **pyenv:** 2.6.17
- **Global Python:** 3.12.7
- **uv:** 0.9.21 (fast virtual environments)
- **pipx:** 1.8.0 (isolated CLI tools)

### Test Script
`~/Documents/PersonalHub/Projects/PythonTools/crawl_test.py`


## 📁 Project Structure

```
~/Documents/PersonalHub/
├── Vaults/
│   └── SystemMac/              # This vault
├── Projects/
│   └── PythonTools/           # Python dev environment
├── AppsData/
│   └── Superwhisper/          # Voice dictation data
└── README.md                  # Personal hub overview
```

- System Setup: [[SystemPolicy/01_BaseSetup]]
- Agent Documentation: [[ClaudeCode CLI]], [[Gemini CLI]]
- Scripts: [[Scripts/crawl_test.py]]
