# Codebase Concerns

**Analysis Date:** 2026-04-21

## Tech Debt

**Reflexion Asia WordPress (92.113.28.34:65002):**
- Issue: jQuery is not defined - LiteSpeed JS Defer/Combine causing JS conflicts
- Files: `00_System/Audits/reflexion.asia.md`
- Impact: Broken JavaScript functionality, Lighthouse errors, potential UX failures
- Fix approach: Disable "Load JS Deferred" in LiteSpeed Cache, disable SG Security plugin

**Supabase Database Security:**
- Issue: RLS (Row-Level Security) coverage unknown - security audit tools created but not run
- Files: `10_Infrastructure/VPS_Hostinger/rls_security_audit.py`, `10_Infrastructure/VPS_Hostinger/rls_redundancy_audit.py`
- Impact: Tables exposed to PostgREST without RLS protection could allow unauthorized data access
- Fix approach: Run RLS security audit against Supabase PostgreSQL to identify unprotected tables

**Reflexion Asia Disk Space:**
- Issue: wp-content storage was 12GB, cleaned to 6.3GB but 5.4GB is still media uploads
- Files: `00_System/Audits/reflexion.asia.md`
- Impact: Continued growth will cause storage exhaustion
- Fix approach: Convert to WebP format, implement media optimization pipeline

**VPS Monitoring Not Deployed:**
- Issue: Monitoring system designed and planned but never deployed
- Files: `10_Infrastructure/VPS_Hostinger/TODO.md`, `10_Infrastructure/VPS_Hostinger/Plan_Action_Monitoring.md`
- Impact: No visibility into VPS health, services could fail unnoticed
- Fix approach: Deploy the monitoring scripts that were already created with cron configuration

**Multi-Agent Sync System:**
- Issue: "Create system synchronisation multi-agents Obsidian" listed as high priority but not completed
- Files: `10_Infrastructure/VPS_Hostinger/TODO.md`
- Impact: Agents operate without shared context, potential coordination failures
- Fix approach: Requires credentials and deployment steps documented in journal

## Known Bugs

**jQuery not defined on reflexion.asia:**
- Symptoms: Console error "jQuery is not defined", JS functionality broken
- Files: `00_System/Audits/reflexion.asia.md`
- Trigger: LiteSpeed Cache JS optimization + SG Security plugin conflict
- Workaround: Disabled SG Security and JS optimizations temporarily

**403 Forbidden on guest.vary.php:**
- Symptoms: Cloudflare/WAF blocking legitimate PHP file
- Files: `00_System/Audits/reflexion.asia.md`
- Trigger: WAF rule blocking guest.vary.php
- Workaround: Need to create Cloudflare WAF rule to allow the file

**SG Security Core Checksum Failure:**
- Symptoms: WordPress core file integrity checks failing
- Files: `00_System/Audits/reflexion.asia.md`
- Trigger: SG Security plugin blocking even legitimate core files
- Workaround: Disabled SG Security

## Security Considerations

**API Keys Management:**
- Risk: Keys stored in `.env.local` but documentation shows incomplete inventory
- Files: `00_System/Secrets/API_KEYS_MANAGEMENT.md`
- Current mitigation: .env.local ignored by git and Obsidian
- Recommendations: Complete the inventory checklist, ensure all missing keys are documented and rotated if exposed

**SSH Access to VPS (31.97.67.145):**
- Risk: No backup SSH key documented, single point of failure
- Files: `10_Infrastructure/VPS_Hostinger/TODO.md` (priority medium task)
- Current mitigation: SSH key-based auth
- Recommendations: Add backup SSH key as documented in TODO

**Cloudflare Monitoring:**
- Risk: Zone ID documented but no formal log monitoring schedule
- Files: `40_Context_Hub/CURRENT_CONTEXT.md`
- Current mitigation: Zone ID 714417ac4b11ad4380ee0692e8c535ae for Cloudflare logs
- Recommendations: Set up automated alerting for security events

**Supabase RLS Audit Not Run:**
- Risk: Database tables may be exposed without Row-Level Security
- Files: `10_Infrastructure/VPS_Hostinger/rls_security_audit.py`, `10_Infrastructure/VPS_Hostinger/rls_redundancy_audit.py`
- Impact: Unauthorized data access via PostgREST API
- Recommendations: Run security audits against production database

## Performance Bottlenecks

**RLS Policy Redundancy:**
- Problem: Multiple permissive RLS policies on same table/action evaluated per query
- Files: `10_Infrastructure/VPS_Hostinger/rls_redundancy_audit.py`
- Cause: Multiple policies created for same role/action instead of consolidated
- Improvement path: Run redundancy audit, consolidate policies with OR conditions

**WordPress Media Storage (5.4GB):**
- Problem: Unoptimized images consuming storage and bandwidth
- Files: `00_System/Audits/reflexion.asia.md`
- Cause: No image optimization pipeline, PNG/JPG stored at original resolution
- Improvement path: Implement WebP conversion, lazy loading, CDN caching

**VPS Disk Space Management:**
- Problem: No automated cleanup of Docker, logs, backups
- Files: `10_Infrastructure/VPS_Hostinger/TODO.md`
- Cause: Docker containers and logs grow unbounded, no retention policy
- Improvement path: Configure Docker cleanup cron, log rotation, backup retention

## Fragile Areas

**Palanthai Pipeline Orchestrator:**
- Files: `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/content_flywheel.py`
- Why fragile: Single point of failure for multi-system data export (Supabase, Qdrant, Neo4j)
- Safe modification: Test with mock connections before running against production
- Test coverage: No tests detected in this repository

**VPS Monitoring Scripts:**
- Files: `10_Infrastructure/VPS_Hostinger/rls_security_audit.py`, `rls_redundancy_audit.py`
- Why fragile: Hardcoded connection parameters, docker exec assumptions
- Safe modification: Test against non-production database first, validate docker container names
- Test coverage: Unit tests mentioned in TODO but actual test files not found in this vault

**crawl_test.py Stub:**
- Files: `00_System/Scripts/crawl_test.py`
- Why fragile: Placeholder script with TODO comment, no actual implementation
- Safe modification: Replace with real crawler implementation before use
- Test coverage: N/A - stub only

## Scaling Limits

**WordPress (reflexion.asia / recall-agency.com):**
- Current capacity: Shared hosting on Hostinger, estimated ~10K visitors/month based on storage
- Limit: Shared resources (CPU, RAM) with no vertical scaling path
- Scaling path: Migrate to VPS with dedicated resources, implement CDN for static assets

**Supabase Database:**
- Current capacity: Unknown - no monitoring deployed
- Limit: Supabase free tier limits on storage and bandwidth
- Scaling path: Enable monitoring, track usage, upgrade plan as needed

**VPS (31.97.67.145):**
- Current capacity: Unknown - no metrics collected
- Limit: VPS plan resource limits (likely 2-4GB RAM, 2 vCPU)
- Scaling path: Upgrade Hostinger plan, optimize Docker container usage

## Dependencies at Risk

**Python Scripts (no requirements.txt):**
- Risk: No dependency pinning in this vault, scripts may break with library updates
- Impact: `rls_security_audit.py`, `rls_redundancy_audit.py`, `crawl_test.py` may fail
- Migration plan: Create requirements.txt for each script directory with pinned versions

**LiteSpeed Cache Plugin:**
- Risk: JS optimization features conflict with theme/plugin JS loading order
- Impact: JavaScript functionality breaks on reflexion.asia
- Migration plan: Test alternative caching plugins or disable problematic features

## Missing Critical Features

**VPS Monitoring:**
- Problem: No system monitoring, service health checks, or alerting
- Blocks: Proactive problem resolution, SLA guarantees, capacity planning

**Database RLS Audit:**
- Problem: Security audit never run, unknown exposure surface
- Blocks: Security compliance, data access control verification

**Multi-Agent Obsidian Sync:**
- Problem: Agents operate independently without shared context
- Blocks: Coordinated agent workflows, consistent context across sessions

**Backup System:**
- Problem: No documented backup strategy for vault content
- Blocks: Disaster recovery, content preservation

**Monitoring Dashboard:**
- Problem: No unified view of pipeline status across all services (Supabase, Qdrant, Neo4j, Ollama, n8n)
- Blocks: Quick status assessment, incident triage

## Test Coverage Gaps

**Python Scripts:**
- What's not tested: `rls_security_audit.py`, `rls_redundancy_audit.py` - no unit tests
- Files: `10_Infrastructure/VPS_Hostinger/`
- Risk: Security audit tools could miss vulnerabilities or produce false positives
- Priority: Medium - tools are already written but untested

**Vault-Wide:**
- What's not tested: No automated tests for any Obsidian vault functionality
- Risk: Broken links, outdated references, stale data could accumulate
- Priority: Low - this is a documentation vault, not a code project

---

*Concerns audit: 2026-04-21*