# Codebase Concerns

**Analysis Date:** 2026-04-13

## Critical Security Issues

### RLS (Row-Level Security) Not Enabled on Supabase Database

**Issue:** 83 PostgreSQL tables are exposed without Row-Level Security protection via PostgREST API.
- **Files:** `10_Infrastructure/VPS_Hostinger/RLS_HARDENING_ACTION_PLAN.md`
- **Impact:** Critical tables containing credentials, tokens, and workflow data are publicly accessible
- **Risk:** API keys, OAuth tokens, refresh tokens, and session data exposed to anyone querying the API
- **Tables at Risk:**
  - `user_api_keys` - API credentials (1 row)
  - `oauth_access_tokens` - OAuth tokens (7 rows)
  - `refresh_tokens` - JWT tokens
  - `sessions` - Session data
  - `binary_data` - Unknown files (50 rows)
  - 11 n8n workflow tables with 3,400+ rows of execution data
- **Fix Approach:** Execute the 3 bulk RLS enable scripts documented in `RLS_HARDENING_ACTION_PLAN.md`

### Hardcoded Server IP Address

**Issue:** VPS IP `31.97.67.145` appears in approximately 80+ locations across the codebase.
- **Files:** `20_Projects/20_Reflexion_Asia/02_Technical/real_estate_tools/viewers/*.html`, `10_Infrastructure/VPS_Hostinger/*.md`, `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/SPRINT1_ACTION_PLAN.md`, and many more
- **Impact:** If VPS IP changes, all references must be updated manually
- **Risk:** Configuration drift, broken SSH tunnels, broken API endpoints
- **Fix Approach:** Use environment variable `VPS_HOST` and reference `.env.local` for all IP-dependent code

---

## Technical Debt

### Pipeline Monitoring Not Operational

**Issue:** The `master_runner.py` script has no execution tracking.
- **File:** `10_Infrastructure/VPS_Hostinger/Pipeline_Dashboard.md`
- **Status:** "Non suivi" (not tracked) for all pipeline scripts
- **Impact:** No visibility into whether extraction scripts run, succeed, or fail
- **Fix Approach:** Implement cron scheduling documented in `10_Infrastructure/VPS_Hostinger/TODO.md` (priority-high task)

### Deprecated Crawl4AI API References

**Issue:** Multiple deprecated API patterns in documentation and code.
- **Files:** `30_Knowledge/Development/docs.crawl4ai.com/api/async-webcrawler/index.md` (lines 69, 79, 104, 148, 243, 332, 367)
- **Status:** "Legacy", "deprecated", "backwards compatibility" mentioned throughout
- **Impact:** Using deprecated patterns may break on library upgrade
- **Risk:** Technical debt increases as deprecated code accumulates
- **Fix Approach:** Update documentation to use current API patterns

### Legacy Patterns in Crawl4AI Documentation

**Issue:** Multiple references to outdated patterns:
- `30_Knowledge/Development/docs.crawl4ai.com/core/cache-modes/index.md` - "Old Way (Deprecated)"
- `30_Knowledge/Development/docs.crawl4ai.com/api/crawl-result/index.md` - "Legacy field", "Raw Markdown (legacy)"
- `30_Knowledge/Development/docs.crawl4ai.com/core/installation/index.md` - "Local Server Mode (Legacy)"
- `30_Knowledge/Development/docs.crawl4ai.com/api/async-webcrawler/index.md` - "Legacy parameters still accepted"
- `30_Knowledge/AI_Orchestration/crawl4ai-deep-dive.md` - "Selenium – Legacy automation"

### jQuery Console Error on reflexion.asia

**Issue:** `jQuery is not defined` error persists on production site.
- **File:** `00_System/Audits/reflexion.asia.md`
- **Cause:** LiteSpeed Cache JS Defer/Combine conflicting with theme
- **Impact:** JavaScript-dependent functionality broken on reflexion.asia
- **Fix Approach:** Disable "Load JS Deferred" in LiteSpeed Cache temporarily

### 403 Forbidden on guest.vary.php

**Issue:** Cloudflare WAF blocking `guest.vary.php` on reflexion.asia.
- **File:** `00_System/Audits/reflexion.asia.md`
- **Impact:** Certain PHP includes fail, potential functionality gaps
- **Fix Approach:** Create Cloudflare WAF rule to allow `guest.vary.php`

### WordPress Core Checksum Validation Failure

**Issue:** WordPress core file checksums cannot be validated due to SG Security interference.
- **File:** `00_System/Audits/reflexion.asia.md`
- **Impact:** Cannot detect file tampering or malware injection
- **Risk:** Potential compromise goes undetected
- **Fix Approach:** Disable SG Security temporarily to run checksum verification, then re-enable

---

## Missing Components

### Social Media Integration Incomplete

**Issue:** LinkedIn, X/Twitter, Facebook/Instagram API integration not completed.
- **File:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/SPRINT1_ACTION_PLAN.md` (lines 70-100)
- **Current Status:**
  - LinkedIn: Requires OAuth2 setup with 60-day token expiry
  - X/Twitter: Requires API key/secrets but n8n native node available
  - Facebook/Instagram: Deferred to Phase 2
- **Impact:** Cannot automatically publish to social platforms
- **Fix Approach:** Use n8n native X/Twitter node (OAuth2 handled automatically), or use Phantombuster/Buffer alternatives

### Phase 1.5 Data Sources Not Implemented

**Issue:** Financial and market data sources planned but not built.
- **File:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/02_Pipeline_Status.md`
- **Missing Sources:**
  - SET Thailand (`set.or.th`) — PropCon sector financials
  - Bank of Thailand — REIC housing index, construction permits
  - CBRE Thailand — Quarterly market reports (PDF)
  - EIA databases — Environmental impact assessments
- **Impact:** Incomplete market intelligence for Thailand real estate analysis

### Phase 2 Multi-Marketplace Not Started

**Issue:** DDProperty, Hipflat, PropertyHub, Thailand-Property, sitemap discovery engine not implemented.
- **File:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/02_Pipeline_Status.md`
- **Impact:** Limited to only LivePhuket and FazWaz data sources

### Backup System Missing

**Issue:** No backup configuration found in vault.
- **Files:** Glob for `**/backup*` returns no results
- **Impact:** No documented backup procedures for:
  - Obsidian vault
  - Supabase database
  - Qdrant vector store
  - Neo4j graph database
- **Fix Approach:** Document backup procedures for all infrastructure components

---

## Performance Concerns

### Large Media Upload on reflexion.asia

**Issue:** 5.4 GB of media files on reflexion.asia.
- **File:** `00_System/Audits/reflexion.asia.md`
- **Impact:** Slow page loads, high bandwidth costs
- **Recommendation:** Convert to WebP format to reduce size by 30-50%

### VPS Disk Space Management Not Implemented

**Issue:** No automatic cleanup of Docker images, logs, or old snapshots.
- **File:** `10_Infrastructure/VPS_Hostinger/TODO.md` (priority-medium: "Optimisation disque")
- **Impact:** Disk space will eventually fill up
- **Fix Approach:** Configure log rotation and Docker prune cron jobs

### SSH Tunnel Manual Management

**Issue:** Multiple documentation references require manual SSH tunnel setup.
- **Example:** `ssh -L 3000:127.0.0.1:8000 phil@31.97.67.145 "sleep 600" &`
- **Files:** `20_Projects/20_Reflexion_Asia/02_Technical/real_estate_tools/viewers/data_viewer.html`, `20_Projects/20_Reflexion_Asia/02_Technical/real_estate_tools/viewers/image_viewer.html`
- **Impact:** Fragile, timeout-prone, not resilient
- **Fix Approach:** Use persistent SSH tunnels with systemd service or autossh

---

## Architecture Issues

### External Site Exposed Separately

**Issue:** reflexion.asia (92.113.28.34:65002) is on different infrastructure than main VPS (31.97.67.145).
- **Files:** `00_System/Audits/reflexion.asia.md`, `30_Knowledge/Development/VPS Hostinger & WordPress.md`
- **Impact:** Separate security considerations, different monitoring required
- **Risk:** Site-specific issues may not be visible in main pipeline dashboard

### Symlink Outside Vault

**Issue:** Main scraper lives outside vault at `/Users/phil/Documents/The_Lab/Pipeline/main_scraper`.
- **File:** `20_Projects/Active/Pipeline_Main_Scraper.md`
- **Impact:** Version control doesn't track the actual code, only a symlink reference
- **Risk:** Code may become orphaned or out of sync

### Obsidian Plugins Contain Minified Code

**Issue:** Plugin JavaScript files in `.obsidian/plugins/` are minified, preventing security audit.
- **Files:** `.obsidian/plugins/*/main.js` (multiple plugins)
- **Impact:** Cannot review plugin behavior for security issues
- **Risk:** Malicious or vulnerable plugins could be present
- **Fix Approach:** Document which plugins are trusted, consider removing unneeded plugins

---

## Known Bugs and Limitations

### Syncthing Conflicts

**Issue:** Syncthing creates conflicts when syncing bidirectional between VPS and Mac.
- **File:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/SPRINT1_ACTION_PLAN.md`
- **Resolution:** Work directly on VPS via SSH, Syncthing only for read-only Mac access

### Google MCP Restart Required

**Issue:** Google Analytics and Search Console MCP servers require Gemini CLI restart to activate.
- **File:** `40_Context_Hub/CURRENT_CONTEXT.md`
- **Impact:** MCP tools unavailable until manual restart performed
- **Fix Approach:** Document restart procedure, consider automation

### Cloudflare Zone Monitoring Not Automated

**Issue:** Security monitoring relies on manual log review via Cloudflare dashboard.
- **File:** `40_Context_Hub/CURRENT_CONTEXT.md`
- **Impact:** Delayed response to security incidents
- **Fix Approach:** Configure Cloudflare alert policies and webhook notifications

### reflexion.asia LiteSpeed Cache JS Conflict

**Issue:** LiteSpeed Cache JS optimization conflicts with jQuery loading on reflexion.asia.
- **File:** `00_System/Audits/reflexion.asia.md`
- **Status:** Partially resolved by disabling some optimizations, but jQuery error persists
- **Fix Approach:** Further LiteSpeed Cache configuration review needed

---

## Documentation Gaps

### No Test Suite Documentation

**Issue:** No testing documentation found. This is an Obsidian vault, not a traditional codebase.
- **Impact:** No automated validation of script functionality
- **Fix Approach:** Document manual testing procedures for critical scripts

### No Runbook for Common Operations

**Issue:** While maintenance schedule exists in `00_System/Policies/05_Maintenance.md`, specific runbooks for common operations are missing.
- **Impact:** Harder to onboard new operators or handle emergencies consistently
- **Fix Approach:** Create runbook documents for: restart services, check logs, run backups, verify pipeline

### VPS Access Credentials Not Centralized

**Issue:** Multiple SSH access docs scattered: `10_Infrastructure/VPS_Hostinger/VPS_ACCESS_REFERENCE.md`, `10_Infrastructure/Shared_Hosting/Hostinger/Access/*.md`
- **Impact:** Potential for credential drift or outdated access info
- **Fix Approach:** Consolidate to single access reference document

### Missing Dependency Documentation

**Issue:** No single document listing all external service dependencies and their health status.
- **Impact:** Difficult to quickly assess what services are required for pipeline to function
- **Fix Approach:** Create dependency matrix: Service, URL, Health Check Endpoint, Restart Procedure

---

## Pending TODO Items

From `10_Infrastructure/VPS_Hostinger/TODO.md`:

**High Priority:**
- Create multi-agent Obsidian sync system (assigned to agent-claude)
- Deploy monitoring on VPS (needs credentials)
- Configure cron for monitoring (every 5 min)

**Medium Priority:**
- Adjust monitoring thresholds (after 1 week observation)
- Disk optimization (Docker cleanup, log rotation)
- Add backup SSH key

**Low Priority:**
- Add application health checks (HTTP endpoints)
- Prometheus + Grafana integration
- Automatic snapshot cleanup (retention policies)
- Metrics history and analysis

---

## Risk Assessment Summary

| Category | Issue | Severity | Effort to Fix |
|----------|-------|----------|---------------|
| Security | 83 tables without RLS | CRITICAL | 2-4 hours |
| Security | Hardcoded IP (80+ locations) | HIGH | 1-2 days |
| Operations | Pipeline monitoring not enabled | HIGH | 2-3 hours |
| Operations | No backup system documented | HIGH | 4-8 hours |
| Performance | 5.4GB media on reflexion.asia | MEDIUM | 2-4 hours |
| Technical | jQuery error on reflexion.asia | MEDIUM | 1-2 hours |
| Technical | Deprecated Crawl4AI API references | MEDIUM | 4-8 hours |
| Architecture | Symlink outside vault | MEDIUM | 1-2 days |
| Completeness | Social media integration missing | MEDIUM | 4-8 hours |
| Completeness | Phase 1.5/2 data sources not built | LOW | Weeks |

---

*Concerns audit: 2026-04-13*