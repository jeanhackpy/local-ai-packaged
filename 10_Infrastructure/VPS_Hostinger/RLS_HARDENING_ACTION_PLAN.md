# RLS Security Hardening: Complete Action Plan
**Generated**: 2026-04-03  
**Status**: Ready for Implementation

---

## Executive Summary

Your PostgreSQL database has **83 unprotected tables** with **3,585+ exposed rows** exposed to PostgREST API. This represents a significant security gap.

**Current State:**
- ✅ 7 tables protected with RLS
- ❌ 83 tables exposed (public API access)
- 🔴 5 tables contain credentials/tokens (CRITICAL)
- 🟠 11 tables contain workflow execution data (HIGH)
- 🟡 68+ tables contain reference data (MEDIUM)

---

## Critical Findings

### Tier 1: Security-Sensitive (5 tables - CRITICAL)
These should be protected immediately:

| Table | Rows | Data Type | Risk | Action |
|-------|------|-----------|------|--------|
| **user_api_keys** | 1 | API credentials | 🔴 CRITICAL | `bulk_rls_enable_tier1_critical.sql` |
| **oauth_access_tokens** | 7 | OAuth tokens | 🔴 CRITICAL | `bulk_rls_enable_tier1_critical.sql` |
| **binary_data** | 50 | Unknown files | 🔴 CRITICAL | `bulk_rls_enable_tier1_critical.sql` |
| **refresh_tokens** | ? | JWT tokens | 🔴 CRITICAL | `bulk_rls_enable_tier1_critical.sql` |
| **sessions** | ? | Session data | 🔴 CRITICAL | `bulk_rls_enable_tier1_critical.sql` |

### Tier 2: Workflow Data (11 tables - HIGH)
n8n execution and automation data - 3,400+ rows:

| Table | Rows | Status | Action |
|-------|------|--------|--------|
| execution_data | 1,276 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| execution_entity | 1,276 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| workflow_dependency | 686 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| workflow_publish_history | 107 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| workflow_statistics | 59 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| insights_by_period | 54 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| workflow_entity | 29 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| workflow_history | 20 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| webhook_entity | 9 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| shared_workflow | 6 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |
| insights_metadata | 5 | 🟠 HIGH | `bulk_rls_enable_tier2_workflows.sql` |

### Tier 3: Reference Data (67+ tables - MEDIUM)
Districts, provinces, regions, cities, etc.:
- Action: `bulk_rls_enable_all_remaining_tables.sql`

---

## Implementation Guide

### Option 1: Fast Track (Recommended) - **Total Time: 1-2 hours**

```bash
# Step 1: Enable Tier 1 (Critical) - 5-10 minutes
ssh phil@31.97.67.145
docker exec supabase-db psql -U postgres -d postgres -f /path/to/bulk_rls_enable_tier1_critical.sql

# Step 2: Enable Tier 2 (Workflows) - 5-10 minutes  
docker exec supabase-db psql -U postgres -d postgres -f /path/to/bulk_rls_enable_tier2_workflows.sql

# Step 3: Enable Tier 3 (All remaining) - 1 minute
docker exec supabase-db psql -U postgres -d postgres -f /path/to/bulk_rls_enable_all_remaining_tables.sql

# Step 4: Verify
docker exec supabase-db psql -U postgres -d postgres -c "
SELECT 
    COUNT(*) as total,
    SUM(CASE WHEN rowsecurity THEN 1 ELSE 0 END) as protected,
    SUM(CASE WHEN NOT rowsecurity THEN 1 ELSE 0 END) as unprotected
FROM pg_tables WHERE schemaname = 'public';
"
```

Expected output: `90 | 90 | 0` (all protected)

### Option 2: Conservative - **Total Time: 2-4 hours**

Execute only Tier 1 and Tier 2 today, schedule Tier 3 for tomorrow:

```bash
# Today: Execute Tier 1 + Tier 2
ssh phil@31.97.67.145
docker exec supabase-db psql -U postgres -d postgres -f bulk_rls_enable_tier1_critical.sql
docker exec supabase-db psql -U postgres -d postgres -f bulk_rls_enable_tier2_workflows.sql

# Tomorrow: Execute Tier 3
docker exec supabase-db psql -U postgres -d postgres -f bulk_rls_enable_all_remaining_tables.sql
```

### Option 3: Automated (Fastest) - **Total Time: 2-5 minutes**

Execute all in one shot:

```bash
ssh phil@31.97.67.145
docker exec supabase-db psql -U postgres -d postgres -f bulk_rls_enable_all_remaining_tables.sql
```

---

## Script Files Created

| File | Purpose | Tables | Time |
|------|---------|--------|------|
| `bulk_rls_enable_tier1_critical.sql` | Enable RLS on security-sensitive tables | 5 | 2-3 min |
| `bulk_rls_enable_tier2_workflows.sql` | Enable RLS on workflow automation data | 11 | 3-5 min |
| `bulk_rls_enable_all_remaining_tables.sql` | Enable RLS on all 83+ unprotected tables | 83 | 1-2 min |
| `RLS_HARDENING_PLAN_83_TABLES.md` | Complete hardening strategy | - | Reference |

---

## What These Scripts Do

### Tier 1 Script (tier1_critical.sql)
```sql
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_api_keys_select_postgres ON user_api_keys
    FOR SELECT USING (current_user = 'postgres');
-- ... (admin-only policies for INSERT/UPDATE/DELETE)
```

**Policy Strategy:**
- ❌ Public CANNOT read (role = 'postgres' only)
- ✅ Postgres role can do everything
- Result: Credentials 100% protected

### Tier 2 Script (tier2_workflows.sql)
```sql
ALTER TABLE execution_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY execution_data_select_all ON execution_data
    FOR SELECT USING (true);
-- ... (admin-only write policies)
```

**Policy Strategy:**
- ✅ Public CAN read (browsing/auditing)
- ✅ Postgres role can INSERT/UPDATE/DELETE
- Result: Data visible but protected from modification

### Tier 3 Script (all_remaining.sql)
```sql
-- Dynamic: For each unprotected table
ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;
CREATE POLICY [table_name]_select_all ON [table_name] FOR SELECT USING (true);
CREATE POLICY [table_name]_insert_postgres ON [table_name] FOR INSERT 
    WITH CHECK (current_user = 'postgres');
-- ... (similar for UPDATE/DELETE)
```

**Policy Strategy:**
- Same as Tier 2 (public read, admin write)
- Applied to all 67+ remaining tables

---

## Pre-Execution Checklist

Before running any script:

- [ ] **Backup**: `pg_dump` your database
- [ ] **Test**: Run on staging first
- [ ] **SSH Ready**: Verify VPS connectivity
- [ ] **Docker Running**: Confirm Supabase containers are up
- [ ] **Read Only**: Consider temporarily blocking writes during execution

```bash
# Quick backup (optional)
ssh phil@31.97.67.145 "docker exec supabase-db pg_dump -U postgres postgres > /tmp/backup_2026-04-03.sql"

# Verify DB is ready
ssh phil@31.97.67.145 "docker exec supabase-db psql -U postgres -d postgres -c 'SELECT version();'"
```

---

## Post-Execution Verification

After running scripts, verify:

```bash
ssh phil@31.97.67.145 "docker exec supabase-db psql -U postgres -d postgres -c \"
SELECT 
    COUNT(*) as total_tables,
    SUM(CASE WHEN rowsecurity THEN 1 ELSE 0 END) as protected,
    SUM(CASE WHEN NOT rowsecurity THEN 1 ELSE 0 END) as unprotected
FROM pg_tables 
WHERE schemaname = 'public'
    AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns');
\""
```

**Expected result after all 3 scripts:**
```
90 | 90 | 0
```

---

## Rollback Plan

If something goes wrong:

```bash
# Disable RLS on a single table
docker exec supabase-db psql -U postgres -d postgres -c "ALTER TABLE [table_name] DISABLE ROW LEVEL SECURITY;"

# Drop all policies on a table
docker exec supabase-db psql -U postgres -d postgres -c "
SELECT 'DROP POLICY ' || policyname || ' ON ' || tablename || ';'
FROM pg_policies
WHERE tablename = '[table_name]';"

# Full rollback (restore from backup)
docker exec supabase-db psql -U postgres -d postgres < /tmp/backup_2026-04-03.sql
```

---

## Next Steps

### Immediate (Today)
1. Review this plan and choose an option
2. Run chosen script(s)
3. Verify all tables now have RLS enabled

### Short Term (This Week)
- Test PostgREST API access (should fail for sensitive tables)
- Update application code if hardcoded row access
- Document any role-based policy customizations needed

### Medium Term (This Month)
- Refine policies based on application requirements
- Implement multi-tenant role-based access (if needed)
- Add JWT custom claims for row-level filtering
- Set up monitoring for RLS policy violations

---

## Support Files

You also have these audit tools available:

```bash
# Detect tables without RLS
python3 rls_security_audit.py --docker supabase-db

# Detect redundant policies (performance issue)
python3 rls_redundancy_audit.py --docker supabase-db

# Run as SQL
docker exec supabase-db psql -U postgres -d postgres -f rls_security_audit.sql
docker exec supabase-db psql -U postgres -d postgres -f rls_redundancy_audit.sql
```

---

## Questions?

If you need to:
- **Skip certain tables** → Modify the DO loop in `bulk_rls_enable_all_remaining_tables.sql`
- **Custom policies** → Edit the policy creation statements  
- **Role-based access** → Add JWT custom claims to GoTrue auth configuration
- **Specific table policies** → Reference tier1/tier2 scripts as templates

**Recommended next action**: Execute Option 1 (Fast Track) now, or let me know which tables need different policy strategies.

