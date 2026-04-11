# MiniMax M2.7 Setup & Usage Guide

Part of [[IDE_Capabilities_Index|AI Orchestration System]].

This note documents the configuration of MiniMax-M2.7 across your AI orchestration layer.

## 1. Connection Details (Automated)

The MiniMax API is integrated into these configurations:

- **Claude Code (CLI):** Configured in `~/.claude/settings.json`.
- **Codex CLI:** Profile `m27` added to `~/.codex/config.toml`.
- **Environment:** `MINIMAX_API_KEY` exported in `~/.zshrc`.

## 2. Usage & Orchestration

### Claude Code (CLI)
Use shell aliases to switch between your **Anthropic Pro** and **MiniMax** brains:

- `claude` or `claude-m2`: Runs using **MiniMax-M2.7**.
- `claude-pro`: Bypasses MiniMax to use your **Anthropic Pro** subscription.

### Codex CLI
- Use the MiniMax profile:
  ```bash
  codex --profile m27
  ```

## 3. IDE Configurations (Manual)

### Cursor
1. **Settings** -> **Models**.
2. Enable **"Override OpenAI Base URL"** -> `https://api.minimax.io/v1`.
3. Enter API Key in **"OpenAI API Key"** field.
4. Add **Custom Model**: `MiniMax-M2.7`.

### Kilo Code (VS Code)
1. **Settings** -> **Kilo Code**.
2. **API Provider**: `MiniMax`.
3. **MiniMax Entrypoint**: `api.minimax.io`.
4. **Model**: `MiniMax-M2.7`.
5. Paste API Key.

---
*Created: 2026-04-01*
