---
created: 2026-05-14
updated: 2026-05-14
tags: [deeptech, summarization, content-extraction, brevity]
sources: [raw/deeptech/patterns/create_micro_summary.md]
author: 
---

# Create Micro Summary - Compact Content Summarization

## Summary

An expert content summarizer that produces ultra-compact summaries. Creates a single 20-word sentence summary, three main points (12 words max each), and three takeaways (12 words max each). All output bullets not numbers, human-readable markdown only.

## Key Concepts

- **One Sentence Summary**: 20-word single sentence capturing entire content
- **Main Points**: 3 items, 12 words max each
- **Takeaways**: 3 items, 12 words max each
- **Format**: Bulleted lists, no numbers, no warnings/notes
- **Constraint**: No repeated items, no same opening words

## Connections

- Core summarization pattern used across all analysis workflows
- Lightweight alternative to more detailed analysis patterns
- Applied in情报 synthesis and quick content triage

## File Reference

`raw/deeptech/patterns/create_micro_summary.md`