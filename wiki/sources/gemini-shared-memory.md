---
created: 2024-12-30
updated: 2025-07-03
tags: [gemini-obsidian, vault-structure, Obsidian, configuration, Supabase, Qdrant]
sources: [raw/gemini-obsidian/README.md]
---

# Gemini Obsidian - Shared Memory README

## Summary

Vault documentation describing the structure and organization of the Gemini-obsidian shared knowledge base. The README outlines the directory structure (config/, logs/, data/, projects/, documents/, scripts/, n8n-configs/, VPS-Config/), daily interaction logging conventions, project note organization, and configured services including Qdrant vector database and Supabase with pgvector extension.

## Key Concepts

- **Directory Structure**: config/ (MCP servers, Qdrant, Supabase), logs/daily_interactions/, data/, projects/, documents/, scripts/
- **Daily Interaction Logs**: Chronological records with date, topics, tasks, file changes, decisions
- **Project Organization**: Centralized notes in `projects/ProjectName/ProjectName_Overview.md`
- **Data Management**: Raw data in `data/`, processed outputs in `documents/`
- **Supabase Configuration**: Tables for profiles, documents, embeddings (384-dimension vectors), chat_history
- **Qdrant Setup**: Vector database with 384-dimensional embeddings compatible with all-MiniLM-L6-v2
- **Version History**: Created 2024-12-30, Supabase config added same day, new logging strategy 2025-07-03

## Connections

- Governance document for vault organization
- Referenced by gemini-reboot-obsidian.md for context recall procedures
- Aligns with the WIKI's knowledge management principles (PARA, collective intelligence)

## References

- Original file: `raw/gemini-obsidian/README.md`