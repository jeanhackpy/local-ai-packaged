-- ============================================================================
-- RLS POLICY REDUNDANCY AUDIT: Detect Duplicate Permissive Policies
-- ============================================================================
-- Purpose: Identify tables with multiple permissive RLS policies for the same
--          role and action (e.g., multiple SELECT, INSERT policies)
-- Problem: Each policy must be evaluated, causing performance degradation
-- Solution: Consolidate into single policy with OR conditions
-- ============================================================================

\set QUIET on
\pset format aligned
\pset border 2

\echo ''
\echo '╔════════════════════════════════════════════════════════════════════════╗'
\echo '║  RLS POLICY REDUNDANCY AUDIT — Multiple Permissive Policies          ║'
\echo '║  Report Date: ' || to_char(now(), 'YYYY-MM-DD HH24:MI:SS') || '                                    ║'
\echo '╚════════════════════════════════════════════════════════════════════════╝'
\echo ''

-- SECTION 1: Identify tables with multiple permissive policies for same action
\echo '┌─ CRITICAL: Tables with Redundant Permissive Policies ─┐'
\echo ''

WITH policy_counts AS (
    SELECT 
        schemaname,
        tablename,
        cmd,  -- SELECT, INSERT, UPDATE, DELETE, ALL
        COUNT(*) as policy_count,
        string_agg(policyname, ', ' ORDER BY policyname) as policy_names,
        CASE 
            WHEN COUNT(*) > 1 THEN '🔴 REDUNDANT'
            ELSE '✅ OK'
        END as status
    FROM pg_policies
    WHERE permissive = true  -- Only check permissive policies
    GROUP BY schemaname, tablename, cmd
    HAVING COUNT(*) > 1  -- Only show tables with >1 policy for same action
)
SELECT 
    schemaname,
    tablename,
    cmd as policy_action,
    policy_count as duplicate_policies,
    status,
    policy_names
FROM policy_counts
ORDER BY tablename, cmd;

\echo ''

-- SECTION 2: Detailed breakdown by table
\echo '┌─ DETAILED: Policy Distribution by Table ─┐'
\echo ''

SELECT 
    schemaname,
    tablename,
    COUNT(*) as total_policies,
    COUNT(DISTINCT cmd) as distinct_commands,
    COALESCE(
        (SELECT COUNT(*) FROM pg_policies p2 
         WHERE p2.schemaname = pg_policies.schemaname 
         AND p2.tablename = pg_policies.tablename 
         AND p2.permissive = true 
         GROUP BY p2.cmd HAVING COUNT(*) > 1),
        0
    ) as redundant_policy_groups
FROM pg_policies
WHERE permissive = true
GROUP BY schemaname, tablename
HAVING COUNT(*) > 0
ORDER BY tablename;

\echo ''

-- SECTION 3: Per-table policy matrix (ACTION vs POLICY_COUNT)
\echo '┌─ POLICY MATRIX: Actions vs Count ─┐'
\echo ''

SELECT 
    tablename,
    SUM(CASE WHEN cmd = 'SELECT' THEN 1 ELSE 0 END) as select_policies,
    SUM(CASE WHEN cmd = 'INSERT' THEN 1 ELSE 0 END) as insert_policies,
    SUM(CASE WHEN cmd = 'UPDATE' THEN 1 ELSE 0 END) as update_policies,
    SUM(CASE WHEN cmd = 'DELETE' THEN 1 ELSE 0 END) as delete_policies,
    SUM(CASE WHEN cmd = 'ALL' THEN 1 ELSE 0 END) as all_policies,
    COUNT(*) as total_policies
FROM pg_policies
WHERE schemaname = 'public' AND permissive = true
GROUP BY tablename
ORDER BY total_policies DESC, tablename;

\echo ''

-- SECTION 4: Policy details for tables with redundancy
\echo '┌─ POLICY DETAILS: Policies Involved in Redundancy ─┐'
\echo ''

SELECT 
    p.tablename,
    p.cmd as action,
    p.policyname,
    CASE WHEN p.qual IS NULL THEN 'N/A' ELSE p.qual::text END as using_condition,
    CASE WHEN p.with_check IS NULL THEN 'N/A' ELSE p.with_check::text END as with_check_condition,
    p.roles::text as applicable_roles
FROM pg_policies p
WHERE p.schemaname = 'public' 
    AND p.permissive = true
    AND (p.tablename, p.cmd) IN (
        SELECT tablename, cmd 
        FROM pg_policies 
        WHERE schemaname = 'public' AND permissive = true
        GROUP BY tablename, cmd 
        HAVING COUNT(*) > 1
    )
ORDER BY p.tablename, p.cmd, p.policyname;

\echo ''

-- SECTION 5: Consolidation recommendations
\echo '┌─ RECOMMENDATIONS: Policy Consolidation ─┐'
\echo ''

WITH redundant_policies AS (
    SELECT 
        schemaname,
        tablename,
        cmd,
        COUNT(*) as policy_count,
        string_agg(policyname, ' OR ' ORDER BY policyname) as policies_to_merge
    FROM pg_policies
    WHERE permissive = true
    GROUP BY schemaname, tablename, cmd
    HAVING COUNT(*) > 1
)
SELECT 
    tablename,
    cmd as action,
    policy_count as policies_to_consolidate,
    'Consolidate ' || policy_count || ' ' || cmd || ' policies into 1' as recommendation,
    policies_to_merge as affected_policies
FROM redundant_policies
ORDER BY tablename, cmd;

\echo ''

-- SECTION 6: Summary statistics
\echo '┌─ SUMMARY STATISTICS ─┐'
\echo ''

SELECT 
    (SELECT COUNT(DISTINCT tablename) FROM pg_policies WHERE schemaname = 'public') as tables_with_policies,
    (SELECT COUNT(*) FROM pg_policies WHERE schemaname = 'public' AND permissive = true) as total_permissive_policies,
    (SELECT COUNT(DISTINCT (tablename, cmd)) 
     FROM pg_policies 
     WHERE schemaname = 'public' AND permissive = true) as unique_action_groups,
    (SELECT COUNT(DISTINCT (tablename, cmd)) 
     FROM pg_policies 
     WHERE schemaname = 'public' AND permissive = true
     GROUP BY tablename, cmd HAVING COUNT(*) > 1) as redundant_action_groups;

\echo ''
\echo '✅ Audit Complete'
\echo ''
