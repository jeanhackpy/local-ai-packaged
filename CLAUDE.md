# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Repository Overview

SystemMac is an **Obsidian vault** serving as the agent orchestration hub for Thai real estate intelligence operations. It coordinates three projects: Palanthai (property intelligence), Recall Agency, and Reflexion Asia. It is not a traditional codebase — there are no builds, tests, or package managers.

## PARA 2.0 Organization

```
00_System/       — macOS local maintenance (scripts, inventory, policies)
10_Infrastructure/ — Hostinger VPS (31.97.67.145), Shared Hosting, sites
20_Projects/     — Active work with end dates (Recall Agency, Reflexion Asia, Patrimonasia)
30_Knowledge/    — Technical knowledge base (AI, Docker, Supabase, Qdrant)
40_Context_Hub/   — AI dialogue window (agent instructions, sessions, logs)
Clippings/        — Curated research
gemini-scribe/    — Gemini CLI workspace
```

## Key Entry Points

- **Agent Instructions**: `40_Context_Hub/AGENT_INSTRUCTIONS.md`
- **Current Context**: `40_Context_Hub/CURRENT_CONTEXT.md`
- **Command Center**: `00_COMMAND_CENTER.md` (strategic axes, dashboards)
- **Inbox**: `00_Inbox/`

## External Connections

| Service | Access | Purpose |
|---------|--------|---------|
| VPS SSH | `ssh phil@31.97.67.145` | Supabase, Qdrant, Neo4j, Ollama, n8n, Caddy |
| n8n | https://n8n.recall-agency.com | Workflow automation |
| WordPress | 92.113.28.34:65002 | reflexion.asia, recall-agency.com |

## Operating Rules

1. **Free models only**: OpenRouter calls use `:free` suffix
2. **Brand replacement**: External source names → "Reflexion" in outputs
3. **Governance**: Agents propose, humans approve — no autonomous external actions
4. **patrimonasia.com**: Not built — skip until reflexion + recall stable

## Workflow

Work is done via:
- Direct file editing in this vault
- SSH to VPS for Python script execution
- n8n UI for workflow management

## Related Documentation

Parent vault context: `/Users/phil/Documents/Vaults/CLAUDE.md`
Palanthai details: `/Users/phil/Documents/Vaults/Palanthai/CLAUDE.md`
