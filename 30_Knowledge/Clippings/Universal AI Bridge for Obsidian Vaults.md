---
title: "Universal AI Bridge for Obsidian Vaults"
source: "https://mcp-obsidian.org/"
author:
  - "[[Mauricio Wolff (bitbonsai)]]"
published:
created: 2026-01-27
description: "Connect ANY AI assistant to your Obsidian vault with the open MCP standard. Works with Claude, ChatGPT, and future AI tools. Private, secure, and future-proof."
tags:
  - "clippings"
---
## AI + Obsidian = 🚀

Your assistant. Your notes. Zero friction.

This MCP server lets Claude, ChatGPT+, and other assistants access your vault. Locally, safe frontmatter, no cloud sync.

[Get Started](https://mcp-obsidian.org/#install) [View on GitHub](https://github.com/bitbonsai/mcp-obsidian)

1

### Configure Your AI Platform

```
claude mcp add-json obsidian --scope user '{"type":"stdio","command":"npx","args":["@mauricio.wolff/mcp-obsidian@latest","/path/to/your/vault"]}'
```

💡

💡

Usage Examples

After configuration, Claude Code can access your vault:

`  Read my meeting notes from yesterday  ` `  Search my vault for notes about machine learning  ` `  Create a new note summarizing our discussion  `

📍 **Config file locations:**

Claude Desktop (JSON)

macOS: `  ~/Library/Application\ Support/Claude/claude_desktop_config.json  `

Windows: `%APPDATA%\Claude\claude_desktop_config.json`

Claude Code (CLI)

User scope: `~/.claude.json`

Use `claude mcp add-json --scope user` for global access

ChatGPT+ Desktop (JSON)

macOS: `~/Library/Application Support/ChatGPT/chatgpt_config.json`

Windows: `%APPDATA%\ChatGPT\chatgpt_config.json`

Gemini CLI (JSON)

All platforms: `~/.gemini/settings.json`

OpenAI Codex (TOML)

macOS/Linux: `~/.codex/config.toml`

Windows: `%USERPROFILE%\.codex\config.toml`

⚡ **No pre-installation needed!** npx automatically downloads and runs the server when needed.

2

### Developers: Test with MCP Inspector

\# Install MCP Inspector globally

$ npm install -g @modelcontextprotocol/inspector

\# Test MCP-Obsidian server

$ mcp-inspector npx @mauricio.wolff/mcp-obsidian@latest /path/to/vault

🌐 Opens interactive web interface at http://localhost:5173

🔍 **MCP Inspector** provides a web UI to test all MCP methods interactively.

🌐 **Works with all MCP-compatible platforms:** Claude Desktop, ChatGPT+, Claude Code, Gemini CLI, Cursor IDE, Windsurf, and more coming soon!  
Use the same configuration with your platform's MCP server settings.

🔒 **What "private" means:**

For commercial Claude users: Your data won't be used for AI training.

✓

### You're all set!

Restart your AI platform and you'll see MCP-Obsidian connected. Your AI assistant can now safely read, search, and manage your Obsidian vault.

🔍 Search notes 📝 Edit content 🗂️ Organize files ⚡ Batch operations

🎯

### 🔍 Powerful Search

Fast search across your entire vault. AI can locate notes by content, tags, or metadata instantly.

```json
[
  {
    "p": "Notes/GTD.md",
    "t": "GTD",
    "ex": "...getting things done...",
    "mc": 5,
    "ln": 12
  },
  {
    "p": "Books/Deep Work.md",
    "t": "Deep Work",
    "ex": "...focus and productivity...",
    "mc": 8,
    "ln": 45
  }
]
```

AI Desktop Tool - MCP-Obsidian Active

Connected

You

Add the equation for energy-mass equivalence to my physics notes

AI

```json
🔧 MCP-Obsidian: Using patch_note...

Request:
```
```json
{
  "path": "Physics/Relativity.md",
  "oldString": "## Energy and Mass",
  "newString": "## Energy and Mass\n\nE = mc²",
  "prettyPrint": true
}
```
```json
Response:
```
```json
{
  "success": true,
  "message": "Successfully replaced 1 occurrence",
  "matchCount": 1
}
```
```json
✅ Done! Added Einstein's equation to your notes.
Only the specific section was updated - no full file rewrite needed.
```

### Technical Details

MCP server used patch\_note for efficient partial update

Multi-line text replacement performed atomically

Frontmatter and formatting preserved perfectly

10x faster than rewriting entire file

prettyPrint defaults to false for minimal token usage

Search & Read Notes

Search Read Analysis

You

Find my productivity notes and summarize the key concepts

AI

```json
🔧 MCP-Obsidian: Using search_notes...

Request:
```
```json
{
  "query": "productivity",
  "limit": 5
}
```
```json
Response:
```
```json
{
  "resultCount": 3,
  "results": [
    {
      "path": "Notes/Getting Things Done.md",
      "matchCount": 5
    },
    {
      "path": "Books/Deep Work.md",
      "matchCount": 4
    }
  ]
}
```
```json
🔧 MCP-Obsidian: Using read_multiple_notes...

Request:
```
```json
{
  "paths": [
    "Notes/Getting Things Done.md",
    "Books/Deep Work.md"
  ]
}
```
```json
✅ I've analyzed the notes. Key concepts include:
• Time blocking and focused work sessions
• Eliminating distractions
• Weekly reviews for planning
```

Find notes and read their content for analysis

Update Metadata

Frontmatter Batch Updates

You

Mark all my project notes as completed

AI

```json
🔧 MCP-Obsidian: Using update_frontmatter...

Request:
```
```json
{
  "path": "Projects/Website Redesign.md",
  "frontmatter": {
    "status": "completed",
    "completed": "2025-01-20"
  }
}
```
```json
Response:
Successfully updated frontmatter

✅ Updated 4 project notes with completion status
```

Batch update frontmatter across multiple notes

Feature

MCP-Obsidian

This package

Other MCP-Obsidian

Plugin-based

Generic FS MCP

Basic file access

Direct File Access

Manual approach

Setup Complexity

✅

Simple

Just point to vault path - works instantly

❌

Requires Obsidian plugin + API key setup

⚠️

Moderate

Basic MCP configuration needed

⚠️

Variable

Depends on chosen approach

Obsidian Running Required

✅

No

Works with closed Obsidian - direct file access

❌

Obsidian must be running with REST API plugin

✅

No

Direct filesystem access

✅

No

Direct file manipulation

Plugin Dependencies

✅

None

Zero dependencies - pure file system access

❌

Needs Local REST API community plugin

✅

None

Standard filesystem MCP

✅

None

No additional software needed

Frontmatter Safety

✅

Protected

Advanced YAML parsing with validation

⚠️

API-dependent

Safety depends on Obsidian API implementation

❌

Raw file editing risks corruption

❌

No safety mechanisms

Built-in Search

✅

Advanced

Semantic + full-text search with rankings

✅

Good

Uses Obsidian's search via API

❌

Must manually search directories

❌

Basic grep at best

Performance

✅

Fast

Optimized for large vaults with caching

⚠️

API overhead

HTTP API calls add latency

⚠️

Slow

No vault-specific optimizations

⚠️

Variable

Depends on system capabilities

Link Handling

✅

Intelligent

Preserves and updates internal links

✅

Good

Leverages Obsidian's link management

❌

No understanding of Obsidian format

❌

Can corrupt references

Reliability

✅

High

Direct file access - no intermediary failures

⚠️

Plugin-dependent

Can fail if Obsidian crashes or plugin issues

⚠️

Basic

Standard filesystem reliability

⚠️

Variable

Depends on implementation quality