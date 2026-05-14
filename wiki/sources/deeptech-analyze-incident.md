---
created: 2026-05-14
updated: 2026-05-14
tags: [deeptech, cybersecurity, incident-analysis, breach, CVE]
sources: [raw/deeptech/patterns/analyze_incident.md]
author: 
---

# Analyze Incident - Cybersecurity Breach Data Extraction

## Summary

A structured framework for extracting essential information from cybersecurity breach articles. Produces attack date, one-sentence summary, key details (attack type, vulnerable component, attacker info, target info), incident details (CVEs, compromised accounts, business impact, root cause), and analysis with MITRE ATT&CK, atomic tests, remediation.

## Key Concepts

- **Attack Date**: YYYY-MM-DD format
- **Key Details**: Type, vulnerable component, attacker (name/country), target (name/country/size/industry)
- **Incident Details**: CVEs, accounts compromised, business impact explanation, root cause
- **Analysis**: MITRE ATT&CK tactics/techniques, Atomic Red Team atomics, remediation recommendation/action plan, lessons learned

## Connections

- Related to analyze_malware and analyze_threat_report
- Used in vulnerability_management and threat_modeling
- Applied in incident response workflows

## File Reference

`raw/deeptech/patterns/analyze_incident.md`