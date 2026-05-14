---
created: 2026-05-14
updated: 2026-05-14
tags: [deeptech, debate-analysis, argumentation, insightfulness]
sources: [raw/deeptech/patterns/analyze_debate.md]
author: 
---

# Analyze Debate - Debate Transcript Analysis

## Summary

A neutral debate analysis system that scores insightfulness (0-10), emotionality (0-5), attributes arguments to participants with external verification sources, identifies agreements/disagreements, possible misunderstandings, learnings, and takeaways. All summaries constrained to exactly 16 words.

## Key Concepts

- **Insightfulness Score**: Rates based on idea exchange, novel subjects, agreement reached
- **Emotionality Score**: 0 (calm) to 5 (very emotional)
- **Participants section**: Lists participants with individual emotionality scores
- **Arguments**: Exactly 16 words each, includes verifiable external references
- **Agreements/Disagreements**: Exactly 16 words with quotes
- **Output format**: No markdown formatting (no asterisks, bullets, headers)

## Connections

- Complements analyze_claims for argument-level analysis
- Used in research synthesis for debate evaluation
- Related to personality analysis for understanding speaker motivations

## File Reference

`raw/deeptech/patterns/analyze_debate.md`