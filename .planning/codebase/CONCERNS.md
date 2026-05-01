# Codebase Concerns

**Analysis Date:** 2026-05-01

## Infrastructure Critical Issues

### 1. VPS Disk Space Crisis
- **Issue:** Disk at 83% capacity (80G/96G used)
- **Impact:** Risk of service failure, Docker container crashes
- **Files:** `10_Infrastructure/VPS_Hostinger/`
- **Fix approach:** Docker cleanup (`docker system prune`), log rotation, large file deletion

### 2. Neo4j Graph Database Inactive
- **Issue:** Neo4j container not running, service marked INACTIVE
- **Impact:** NAGA module (graph analytics, entity resolution) non-functional. Developer ↔ SET ticker matching blocked.
- **Files:** `/home/phil/palanthai/phase1-project-directory/neo4j_ingestor.py`
- **Fix approach:** Start Neo4j container or implement alternative graph solution

### 3. Ollama Local LLM Stopped
- **Issue:** Ollama container exited 17 hours ago
- **Impact:** Local embedding/LLM inference unavailable, must rely on external APIs (Groq, NVIDIA, OpenRouter)
- **Files:** VPS Docker container
- **Fix approach:** `docker start ollama` or investigate crash reason

### 4. open-webui Container Exited
- **Issue:** Container exited with code 137 (likely OOM kill or crash)
- **Impact:** Web UI for local Ollama models unavailable
- **Files:** VPS Docker container
- **Fix approach:** Restart container with memory limits adjusted

---

## Deployment & Sync Issues

### 5. Syncthing Mac/VPS Conflicts
- **Issue:** Bidirectional sync creates conflicts. Mac modifies files that conflict with VPS versions.
- **Impact:** Architecture docs may be out of sync, manual reconciliation needed
- **Files:** Obsidian vault between Mac and VPS
- **Fix approach:** Work directly on VPS via SSH (as decided in Sprint 1). Cloudflare Tunnel alternative planned but not implemented.

### 6. Sprint 1 Deployment Incomplete
- **Issue:** Multiple Sprint 1 items planned but not executed on VPS
- **Location:** `/home/phil/palanthai/`
- **Missing items:**
  - [ ] `content_flywheel.py` not yet SCP'd to VPS
  - [ ] `prompt_versions` SQL table not created
  - [ ] `prompt_performance` view not created
  - [ ] 6 new endpoints not added to `palanthai_api.py`
  - [ ] WF-021 and WF-020 not imported into n8n
  - [ ] `palanthai-sync.service` not restarted after updates
- **Files:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/SPRINT1_ACTION_PLAN.md`
- **Fix approach:** Follow deployment order in SPRINT2_IMPROVEMENTS.md

### 7. content_flywheel.py v2.0.0 Lives on Mac Only
- **Issue:** Latest version exists on Mac but VPS has older version
- **Impact:** New endpoints (`/content/write`, `/content/humanize`, `/content/critique`, `/content/qc`, `/rag/query`, `/rag/ingest`) unavailable on production
- **Files:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/content_flywheel.py`
- **Fix approach:** SCP to VPS and integrate into `palanthai_api.py`

### 8. reflexion_kb_clean.json Stale Data
- **Issue:** 203 entries, last updated **2026-03-20** (41 days ago)
- **Impact:** RAG knowledge base has outdated information
- **Files:** `/home/phil/palanthai/reflexion_kb_clean.json`
- **Fix approach:** Trigger WF-020 Obsidian RAG sync to refresh Qdrant collection

---

## Data Pipeline Issues

### 9. 422 Error on /api/v1/source/units
- **Issue:** n8n workflow failing with HTTP 422 when calling unit source endpoint
- **Impact:** Unit-level data crawling not functioning since 2026-04-19
- **Files:** `20_Projects/20_Reflexion_Asia/02_Technical/Palanthai_Core/02_Pipeline_Status.md` (line 65-72)
- **Fix approach:** Investigate payload format in n8n workflow logs, fix UnitSourceRequest model validation

### 10. Units Batch Embedding Mode Confusion
- **Issue:** Two modes (TRICKLE/BURST) with different batch sizes and pauses - not clear which runs on schedule
- **Impact:** Potential over/under-embedding of unit data
- **Files:** `/home/phil/palanthai/phase1-project-directory/bulk_embed_units.py`
- **Fix approach:** Document which mode is scheduled, ensure BURST runs during off-peak only

### 11. Qdrant Collection Schema Mismatch
- **Issue:** Qdrant collection `units` uses 768 dimensions but `content_flywheel.py` default embed is 384
- **Impact:** Cannot directly query `units` collection with standard embedder
- **Files:** Qdrant `units` collection vs `content_flywheel.py` EMBED_DIM = 384
- **Fix approach:** Use separate embedder config for `units` collection (BGE-M3 1024 dims) vs general RAG (MiniLM 384)

---

## Security Concerns

### 12. Database Credentials in Multiple Locations
- **Issue:** Credentials appear in multiple documents (`.env`, audit docs, Supabase audit report)
- **Files:** `SUPABASE_RLS_AUDIT_2026-04-03.md` contains raw credentials (password, JWT secret, anon key)
- **Impact:** If any document is compromised, database access is at risk
- **Fix approach:** Never store actual credentials in markdown files. Use secret manager.

### 13. RLS Audit Not Run Since April 3
- **Issue:** RLS was fully enabled (89 tables) but no ongoing monitoring
- **Files:** `10_Infrastructure/VPS_Hostinger/rls_security_audit.py`, `10_Infrastructure/VPS_Hostinger/rls_redundancy_audit.py`
- **Impact:** New tables created after audit may lack RLS protection
- **Fix approach:** Re-run security audit periodically, automate RLS check in CI

### 14. No Backup SSH Key
- **Issue:** Single SSH key access to VPS, no backup key documented
- **Files:** `TODO.md` (priority medium task incomplete)
- **Impact:** Lockout risk if primary key lost or compromised
- **Fix approach:** Add backup SSH key as documented in TODO

---

## Integration Gaps

### 15. Social Media Workflows Inactive
- **Issue:** WF-011 and WF-012 exist in n8n but not activated
- **Impact:** Buffer API not connected, social distribution pipeline non-functional
- **Files:** SPRINT2_IMPROVEMENTS.md section 6
- **Fix approach:** Create Buffer account, connect LinkedIn/X, add `BUFFER_ACCESS_TOKEN` to `.env`

### 16. LinkedIn OAuth Token Expiry
- **Issue:** OAuth tokens expire every 60 days, no refresh mechanism documented
- **Impact:** Social posting stops working after 60 days without token refresh
- **Files:** SPRINT1_ACTION_PLAN.md lines 72-82
- **Fix approach:** Use Buffer which handles OAuth automatically

### 17. Cross-Encoder Reranker Not Implemented
- **Issue:** RAG query returns candidates but no reranking to select top results
- **Impact:** Lower quality RAG results than potential
- **Files:** `content_flywheel.py` - planned in SPRINT2_IMPROVEMENTS.md P1 item 3
- **Fix approach:** Add `cross-encoder/ms-marco-MiniLM-L-6-v2`, implement optional `rerank=true` parameter

### 18. Hybrid Search (Neo4j) Not Implemented
- **Issue:** Vector search misses relational context, graph enrichment planned but not built
- **Impact:** "Projects near Phuket beach" type queries less accurate
- **Files:** SPRINT2_IMPROVEMENTS.md P1 item 2
- **Fix approach:** Implement `_neo4j_query()` parallel query for entity enrichment

---

## Technical Debt

### 19. Two API Servers Coexist
- **Issue:** Both `palanthai_api.py` (32KB, old) and `sync_service.py` (port 8500, systemd) are running
- **Impact:** Unclear which is authoritative, potential route conflicts
- **Files:** `/home/phil/palanthai/palanthai_api.py` vs `/home/phil/palanthai/sync_service.py`
- **Fix approach:** Consolidate to single FastAPI instance, migrate endpoints to unified router

### 20. Patrimonasia Brand Voice Unfinished
- **Issue:** `BRAND_PROMPTS["patrimonasia"]` uses placeholder text
- **Impact:** Content for Patrimonasia will have generic brand voice
- **Files:** `content_flywheel.py` lines 211-219
- **Fix approach:** Write full brand voice prompts before deploying Patrimonasia

### 21. Pattiasia.com Not Built
- **Issue:** Project exists in planning but no actual development
- **Files:** CLAUDE.md, `00_COMMAND_CENTER.md` (line 22-25)
- **Impact:** Third brand not launched, blocks full market coverage
- **Fix approach:** Skip until reflexion + recall stable per operating rules

---

## Content Pipeline Risks

### 22. QC Retry Loop Has No Retry Limit Enforcement
- **Issue:** QC can return NEEDS_REVISION multiple times, no enforced limit prevents infinite loop
- **Impact:** Article could cycle indefinitely through writer → humanizer → critic → QC
- **Files:** `content_flywheel.py` QC endpoint, n8n WF-021
- **Fix approach:** Add `max_revisions` parameter (default 3), escalate after limit

### 23. RAG Recency Boost May Exclude Valid Content
- **Issue:** `recency_boost_days=90` filters out older documents that may be relevant
- **Impact:** Evergreen content hidden from results
- **Files:** `content_flywheel.py` `/rag/query` endpoint line 539
- **Fix approach:** Boost score rather than filter exclusion

### 24. Experience Signals Not Guaranteed
- **Issue:** Brand voice instructions say to cite vault data but no guaranteed pipeline to provide it
- **Impact:** Writer agent may produce content without real experience signals
- **Files:** `content_flywheel.py` Writer prompt (line 653)
- **Fix approach:** Ensure WF-020 runs before content generation, verify RAG context injection

---

## Known Bugs (from previous audit)

### 25. jQuery not defined on reflexion.asia
- **Symptoms:** Console error "jQuery is not defined", JS functionality broken
- **Files:** `00_System/Audits/reflexion.asia.md`
- **Trigger:** LiteSpeed Cache JS optimization + SG Security plugin conflict
- **Workaround:** Disabled SG Security and JS optimizations temporarily

### 26. 403 Forbidden on guest.vary.php
- **Symptoms:** Cloudflare/WAF blocking legitimate PHP file
- **Files:** `00_System/Audits/reflexion.asia.md`
- **Trigger:** WAF rule blocking guest.vary.php
- **Workaround:** Need to create Cloudflare WAF rule to allow the file

### 27. Supabase Studio DNS Error
- **Symptoms:** Analytics service missing, shows DNS resolution error
- **Impact:** Cannot use Supabase dashboard for analytics
- **Workaround:** Use direct PostgreSQL queries instead

---

## Monitoring & Operational Gaps

### 28. No Prometheus/Grafana Monitoring
- **Issue:** Planned but never implemented
- **Impact:** No visibility into service health, no alerting
- **Files:** `TODO.md` P3 items incomplete
- **Fix approach:** Add Prometheus endpoint exporter, Grafana dashboard

### 29. Backup Strategy Not Verified
- **Issue:** VPS backup infrastructure documented but actual backups not verified
- **Impact:** Data loss risk
- **Files:** `VPS_BACKUP_INFRASTRUCTURE.md`
- **Fix approach:** Verify backup scripts, test restore procedure

### 30. VPS Monitoring Scripts Not Deployed
- **Issue:** Monitoring system designed and planned but never deployed
- **Files:** `TODO.md` (high priority incomplete), `Plan_Action_Monitoring.md`
- **Impact:** No visibility into VPS health, services could fail unnoticed
- **Fix approach:** Deploy the monitoring scripts that were already created with cron configuration

### 31. No Health Check for Palanthai API
- **Issue:** `/flywheel/health` exists in content_flywheel but `/api/v1/` endpoints have no health check
- **Impact:** Cannot detect API failure without manual curl
- **Files:** `palanthai_api.py`, `sync_service.py`
- **Fix approach:** Add `/api/v1/health` endpoint returning service status

---

## Missing Critical Features

### 32. Multi-Tenant Access Control Not Implemented
- **Issue:** RLS enabled but role-based access (Investor/Developer/Admin) not built
- **Impact:** Cannot give investors access to their region/projects only
- **Files:** SUPABASE_RLS_AUDIT_2026-04-03.md (lines 217-251)
- **Fix approach:** Add JWT custom claims, create investor/developer role policies

### 33. No Chaos Testing Performed
- **Issue:** Anti-fragile loop requires chaos testing, but none documented
- **Files:** SPRINT2_IMPROVEMENTS.md lines 165-177 (test scenarios listed but none executed)
- **Fix approach:** Implement test scenarios: GSC empty, vault partial, LLM failure, Qdrant down

### 34. Incremental Obsidian Sync Unclear
- **Issue:** WF-020 planned to use `find -newer` for diff-only indexing but actual implementation unclear
- **Impact:** Full re-indexing may cause performance issues and duplicate entries
- **Files:** WF-020_obsidian_rag_sync.json
- **Fix approach:** Verify `find -newer` logic, add content hash dedup

---

*Concerns audit: 2026-05-01*
