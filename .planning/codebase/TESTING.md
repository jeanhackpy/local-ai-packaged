# Testing Patterns

**Analysis Date:** 2026-04-13

## Test Framework

**Status: Not Directly Applicable**

This is an **Obsidian markdown vault**, not a traditional codebase. There is no `package.json`, `Makefile`, or test suite. Work is accomplished via:
- Direct file editing in `content/`, `phase2/`, `phase3/`, scripts
- SSH to VPS for Python script execution
- n8n UI for workflow management

**Python Testing:** pytest is referenced in user rules, but no test files found in this vault.

---

## Quality Metrics and Standards

### From User Rules (Global)

**Minimum Test Coverage:** 80% (from `~/.claude/rules/common/testing.md`)

**Test Types Required:**
1. **Unit Tests** — Individual functions, utilities, components
2. **Integration Tests** — API endpoints, database operations
3. **E2E Tests** — Critical user flows (framework chosen per language)

**TDD Workflow:**
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

### Quality Practices Observed in Vault

**Code Quality Checklist (from user rules):**
- [ ] Code is readable and well-named
- [ ] Functions are small (<50 lines)
- [ ] Files are focused (<800 lines)
- [ ] No deep nesting (>4 levels)
- [ ] Proper error handling
- [ ] No hardcoded values (use constants or config)
- [ ] No mutation (immutable patterns used)

**Immutability Principle (Critical):**
```
WRONG:  modify(original, field, value) → changes original in-place
CORRECT: update(original, field, value) → returns new copy with change
```

---

## Code Review Practices

### Agent-Based Code Review

**Code Reviewer Agent:**
- Use **code-reviewer** agent immediately after writing code
- Address CRITICAL and HIGH issues
- Fix MEDIUM issues when possible

**Security Reviewer Agent:**
- Use **security-reviewer** agent before any commit
- Mandatory security checks:
  - [ ] No hardcoded secrets (API keys, passwords, tokens)
  - [ ] All user inputs validated
  - [ ] SQL injection prevention (parameterized queries)
  - [ ] XSS prevention (sanitized HTML)
  - [ ] CSRF protection enabled
  - [ ] Authentication/authorization verified
  - [ ] Rate limiting on all endpoints
  - [ ] Error messages don't leak sensitive data

### Manual Review Patterns

**Session Logs for Review:**
- Agent reports stored in `40_Context_Hub/SESSION_LOGS/`
- Example: `2026-01-28-Agent-Report.md` documents vault optimization changes
- Includes action tracking, decision rationale, and link updates

**Agent Orchestration Strategy:**
- Documented in `40_Context_Hub/SESSION_LOGS/2026-01-28-Agent-Report.md`
- Tracks changes made, decisions, and next steps
- Uses structured sections: "I. Vault Structure Improvement", "II. Improving Vault Cross-Referencing", "III. AI Agent Orchestration Strategy"

---

## Verification Approaches

### Health Check Scripts

**mac_health_check.sh:**
```bash
#!/bin/bash
HEALTH_NOTE="/Users/phil/Documents/Vaults/SystemMac/00_System/OS_Health_Status.md"
echo "# 🖥️ macOS Health Status" > "$HEALTH_NOTE"
echo "*Dernière mise à jour : $(date '+%Y-%m-%d %H:%M:%S')*" >> "$HEALTH_NOTE"
echo "## 📊 Statistiques Système" >> "$HEALTH_NOTE"
echo "- **Uptime** : $(uptime | awk -F', ' '{print $1}')" >> "$HEALTH_NOTE"
echo "- **Charge CPU** : $(sysctl -n vm.loadavg | awk '{print $2}')" >> "$HEALTH_NOTE"
echo "- **Mémoire Vive** : $(top -l 1 | grep PhysMem | awk '{print $2 " utilisées, " $6 " libres"}')" >> "$HEALTH_NOTE"
```

**check_env.sh:**
```bash
#!/bin/bash
ENV_FILE="/Users/phil/Documents/Vaults/SystemMac/.env.local"
REQUIRED_KEYS=(
    "HOSTINGER_API_KEY"
    "ANTHROPIC_API_KEY"
    "GEMINI_API_KEY"
    "SUPABASE_URL"
    "SUPABASE_SERVICE_ROLE_KEY"
)
for key in "${REQUIRED_KEYS[@]}"; do
    if grep -q "^$key=" "$ENV_FILE"; then
        echo "✅ $key est configuré."
    else
        echo "⚠️  $key est MANQUANT."
    fi
done
```

### Database Audit Tools

**RLS Security Audit Tool (`rls_security_audit.py`):**
- Detects PostgreSQL tables without Row-Level Security
- Command-line usage:
  ```bash
  python3 rls_security_audit.py --host 31.97.67.145 --db postgres --user postgres
  python3 rls_security_audit.py --docker supabase-db
  python3 rls_security_audit.py --json  # JSON output for CI/CD
  ```

**RLS Redundancy Audit Tool (`rls_redundancy_audit.py`):**
- Detects multiple permissive RLS policies for same action/role
- Generates consolidation SQL
  ```bash
  python3 rls_redundancy_audit.py --docker supabase-db --json
  python3 rls_redundancy_audit.py --docker supabase-db --fix  # Generate fix SQL
  ```

### VPS Monitoring

**Plan Action Monitoring:**
- Documented in `10_Infrastructure/VPS_Hostinger/Plan_Action_Monitoring.md`
- Integration with Hostinger MCP server
- Python monitoring scripts on VPS

### Pipeline Verification

**Palanthai Pipeline Commands:**
```bash
# Single job (limit 10 for testing)
python phase1_project_extractor.py --config phase1_config.yaml --job phuket_condo --limit 10

# All 10 jobs
python phase1_project_extractor.py --config phase1_config.yaml --all

# Developer directory
python phase1_developer_extractor.py --config phase1_config.yaml --enrich
```

**QC Dimensions (9 total):**
1. Grammar/spelling
2. Brand voice compliance
3. Factual accuracy
4. Formatting
5. Completeness
6. Readability
7. SEO optimization
8. Engagement potential
9. ai_search_readiness (AEO/LLM visibility)

---

## Coverage Expectations

### Unit Testing

**Coverage Target:** 80% minimum (from user rules)

**What Would Be Tested (if this were a traditional codebase):**
- Individual Python functions in scripts
- Shell script functions
- Pydantic model validation
- API endpoint handlers

**Test Organization Pattern (from user rules):**
```python
import pytest

@pytest.mark.unit
def test_calculate_total():
    ...

@pytest.mark.integration
def test_database_connection():
    ...
```

### Integration Testing

**Database Operations:**
- Supabase PostgreSQL connections
- Qdrant vector database operations
- Neo4j graph database operations
- Row-Level Security policy verification

**API Testing:**
- FastAPI endpoints in `content_flywheel.py`
- Crawl4AI web scraping results
- Ollama local LLM inference

### E2E Testing

**Critical User Flows (would require framework per language):**
- Web scraping and data extraction pipeline
- Content generation and brand voice verification
- RAG query and semantic search
- WordPress publishing workflow

---

## Verification Without Tests

Since this vault uses alternative verification approaches:

### Manual Verification Steps

**Before Any Commit:**
1. Run `check_env.sh` to verify environment variables
2. Run `mac_health_check.sh` to update system status
3. Verify no hardcoded secrets in modified files
4. Check `.gitignore` excludes sensitive files

**For Scripts:**
1. Check shell script syntax: `bash -n script.sh`
2. Verify script has correct permissions: `chmod +x script.sh`
3. Test in dry-run mode if available

**For Database Changes:**
1. Run `rls_security_audit.py` to verify RLS policies
2. Run `rls_redundancy_audit.py` to check policy optimization
3. Use `--json` output for CI/CD integration

**For Pipeline Scripts:**
1. Test with `--limit 10` first
2. Verify JSON-LD output structure
3. Check Pydantic validation passes

---

## Documentation Quality

**Requirements for Documentation:**
- Wiki-links for cross-referencing: `[[filename]]`, `[[filename#heading]]`
- Frontmatter in YAML format
- Emoji prefixes for visual scanning
- Timestamps for recent updates

**Brand Content Verification:**
- Quality gate: Only embed units with quality score >= 75/100
- Brand replacement: All external source names -> "Reflexion" in outputs
- 9-dimension QC check before publishing

---

## TDD Workflow (When Applicable)

**For new Python features:**
1. Write test first (RED)
2. Run test - it should FAIL
3. Write minimal implementation (GREEN)
4. Run test - it should PASS
5. Refactor (IMPROVE)
6. Verify coverage (80%+)

**Troubleshooting Test Failures:**
1. Use **tdd-guide** agent
2. Check test isolation
3. Verify mocks are correct
4. Fix implementation, not tests (unless tests are wrong)

---

## Quality Gates

| Gate | Requirement |
|------|-------------|
| Environment | `check_env.sh` passes with all required keys present |
| System Health | `mac_health_check.sh` runs without errors |
| Database Security | `rls_security_audit.py` shows no exposed tables |
| Database Performance | `rls_redundancy_audit.py` shows no redundant policies |
| Content Quality | QC score >= 75/100 for embedding |
| Brand Consistency | Correct naming: REcall Agency, REflexion Asia, PatrimoinAsia |

---

*Testing analysis: 2026-04-13*
