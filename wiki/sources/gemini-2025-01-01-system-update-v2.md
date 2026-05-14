---
created: 2025-01-01
updated: 2025-01-01
tags: [gemini-obsidian, MCP, Ollama, open-source, Qdrant, infrastructure]
sources: [raw/gemini-obsidian/2025-01-01_system_update_v2.md]
---

# System Update v2 - 2025-01-01

## Summary

Updated maintenance log from January 1, 2025 documenting the pivot from proprietary LLM providers (OpenAI, Anthropic) to open-source alternatives. The key change was the addition of Ollama (port 8002) to replace the previously planned mcp-server-openai and mcp-server-anthropic. Default model is Qwen 7B with configuration pointing to localhost:11434. The stack emphasizes sovereignty and privacy through open-source components.

## Key Concepts

- **Open-Source AI Stack**: Qdrant for vector storage, Ollama for LLM inference, sentence-transformers for embeddings
- **Ollama Configuration**: Host http://localhost:11434, default model qwen:7b, MCP port 8002
- **Quantized Models**: Recommendation to use quantized models for performance optimization
- **Privacy-First Approach**: Locally hosted LLMs for sensitive data processing
- **Infrastructure Stack**: Qdrant + Ollama + sentence-transformers as the core open-source trio

## Connections

- Replaces `2025-01-01_system_update.md` which initially included proprietary servers
- Aligns with REcall OS philosophy of sovereign, open-source infrastructure
- Related to the Project Blueprint's emphasis on locally-hosted LLMs via Ollama
- Complementary to Supabase for structured data and Neo4j for graph relationships

## References

- Original file: `raw/gemini-obsidian/2025-01-01_system_update_v2.md`