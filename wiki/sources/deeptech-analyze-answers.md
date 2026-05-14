---
created: 2026-05-14
updated: 2026-05-14
tags: [deeptech, education, assessment, answer-evaluation, learning]
sources: [raw/deeptech/patterns/analyze_answers.md]
author: 
---

# Analyze Answers - Student Answer Evaluation

## Summary

A PhD-level expert framework for evaluating student answers against generated correct answers. Adapts evaluation to student level (default: senior university/industry professional). Calculates 0-10 alignment scores with reasoning, marking >=5 as and <5 as.

## Key Concepts

- **Subject extraction**: Identify the learning subject from input
- **Learning objectives**: Extract from provided content
- **Generated answers**: Create correct answers aligned to student level
- **Evaluation**: Compare student provided vs generated answers
- **Score**: 0-10 with reasoning, >=5 gets green check, <5 gets red X

## Connections

- Used in educational content analysis
- Complements analyze_prose for writing quality
- Applied in training and assessment workflows

## File Reference

`raw/deeptech/patterns/analyze_answers.md`