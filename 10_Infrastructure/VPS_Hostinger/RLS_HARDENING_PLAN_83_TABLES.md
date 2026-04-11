# RLS Hardening Plan: Securing 83 Unprotected Tables
## Generated: 2026-04-03
## Priority Action Items

---

## CRITICAL PRIORITY (Enable RLS Immediately)

### Tier 1: Security-Sensitive Tables (5 tables)
These contain credentials, tokens, and keys that should never be exposed:

- **user_api_keys** (1 row) - [HIGH] User authentication credentials
- **oauth_access_tokens** (7 rows) - [HIGH] OAuth tokens/refresh tokens
- **binary_data** (50 rows, 96MB) - [HIGH] Could contain sensitive files
- **sessions** - [HIGH] Session management data
- **refresh_tokens** - [HIGH] JWT refresh tokens

**Action**: Enable RLS with restrictive policies (owner-only access, no public read)

---

### Tier 2: Workflow Automation Data (10 tables)
n8n execution and workflow data - should be protected:

- **execution_data** (1,276 rows, 34MB) - Workflow execution results
- **execution_entity** (1,276 rows) - Execution metadata
- **workflow_dependency** (686 rows) - Workflow dependencies
- **workflow_publish_history** (107 rows) - Publishing history
- **workflow_statistics** (59 rows) - Execution stats
- **workflow_entity** (29 rows) - Workflow definitions
- **workflow_history** (20 rows) - Workflow version history
- **webhook_entity** (9 rows) - Webhook configurations
- **shared_workflow** (6 rows) - Shared workflow references
- **insights_by_period** (54 rows) - Analytics data

**Action**: Enable RLS with role-based access (owner/admin only)

---

### Tier 3: General Data Tables (68 tables)
Remaining public tables without RLS. These are lower risk but should still be protected:

Including: districts, provinces, regions, cities, etc. (reference data)

---

## EXECUTION PLAN

### Step 1: Enable RLS on Sensitive Tables (Tier 1)
```sql
-- User API Keys - OWNER ONLY
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;
CREATE POLICY user_api_keys_select_owner ON user_api_keys
    FOR SELECT USING (current_user = 'postgres' OR current_user_id = auth.uid());
CREATE POLICY user_api_keys_admin_access ON user_api_keys
    FOR ALL USING (current_user = 'postgres');

-- OAuth Tokens - OWNER ONLY
ALTER TABLE oauth_access_tokens ENABLE ROW LEVEL SECURITY;
CREATE POLICY oauth_access_tokens_select_owner ON oauth_access_tokens
    FOR SELECT USING (current_user = 'postgres');
CREATE POLICY oauth_access_tokens_admin_access ON oauth_access_tokens
    FOR ALL USING (current_user = 'postgres');

-- Binary Data - ADMIN ONLY
ALTER TABLE binary_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY binary_data_select_admin ON binary_data
    FOR SELECT USING (current_user = 'postgres');
CREATE POLICY binary_data_admin_access ON binary_data
    FOR ALL USING (current_user = 'postgres');
```

### Step 2: Enable RLS on Workflow Tables (Tier 2)
```sql
-- Execution Data
ALTER TABLE execution_data ENABLE ROW LEVEL SECURITY;
CREATE POLICY execution_data_select_all ON execution_data
    FOR SELECT USING (true);
CREATE POLICY execution_data_admin ON execution_data
    FOR ALL USING (current_user = 'postgres');

-- [Repeat for workflow_dependency, workflow_entity, etc.]
```

### Step 3: Bulk Enable RLS on Remaining Tables (Tier 3)
```sql
-- Generic policy for reference data
-- ALTER TABLE [table_name] ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY [table_name]_select_all ON [table_name] FOR SELECT USING (true);
-- CREATE POLICY [table_name]_admin ON [table_name] FOR ALL USING (current_user = 'postgres');
```

---

## RISK ASSESSMENT

| Category | Tables | Rows | Risk Level | Action |
|----------|--------|------|-----------|--------|
| Security-Sensitive | 5 | ~100 | 🔴 CRITICAL | Enable RLS TODAY |
| Workflow Data | 10 | ~3,400 | 🟠 HIGH | Enable RLS THIS WEEK |
| Reference Data | 68 | ~100 | 🟡 MEDIUM | Enable RLS IN PROGRESS |
| **TOTAL UNPROTECTED** | **83** | **3,585+** | **🔴 CRITICAL** | **→ Action Required** |

---

## IMPLEMENTATION OPTIONS

### Option A: Fast Track (24 hours)
1. Enable RLS on Tier 1 (Security-Sensitive) - 1 hour
2. Enable RLS on Tier 2 (Workflow) - 2-3 hours  
3. Schedule Tier 3 (Reference Data) - This week

### Option B: Comprehensive (48 hours)
1. Audit all 83 tables for dependencies
2. Create consolidated policies per table purpose
3. Enable RLS on all tables in batches
4. Test with role-based access

### Option C: Automated Bulk Enable
Use batch SQL script to enable RLS on all tables (generic policies):
- Fast but less granular
- Can refine policies later per business logic
- Reduces exposure immediately

---

## GENERATED REMEDIATION SCRIPTS

See accompanying files:
- `bulk_rls_enable_all_tables.sql` - Enable RLS on all 83 unprotected tables
- `bulk_rls_enable_tier1_critical.sql` - Enable only Tier 1 (immediate action)
- `bulk_rls_enable_tier2_workflows.sql` - Enable Tier 2 (workflow data)

---

## NEXT STEPS

**Recommended**: Choose Option A (Fast Track) and execute Tier 1 immediately while Tier 2 is scheduled.

**Questions to clarify**:
1. Should public have READ access to reference data (districts, provinces)?
2. Are there specific role-based requirements beyond admin/public?
3. Should workflow execution data be shareable between teams?

