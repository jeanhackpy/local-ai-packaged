-- ============================================================================
-- RLS SECURITY AUDIT: Detect Tables Without Row-Level Security
-- ============================================================================
-- Purpose: Identify tables exposed to PostgREST API that lack RLS protection
-- Usage: psql -U postgres -d postgres -f rls_security_audit.sql
-- ============================================================================

\set QUIET on
\pset format aligned
\pset border 2

-- Summary: Tables WITHOUT RLS in PostgREST-exposed schemas
\echo ''
\echo '╔════════════════════════════════════════════════════════════════════════╗'
\echo '║  RLS SECURITY AUDIT — Tables Without Row-Level Security              ║'
\echo '║  Report Date: ' || to_char(now(), 'YYYY-MM-DD HH24:MI:SS') || '                                    ║'
\echo '╚════════════════════════════════════════════════════════════════════════╝'
\echo ''

-- SECTION 1: Critical Gaps - Public schema (Default PostgREST exposure)
\echo '┌─ CRITICAL: Tables Without RLS in PUBLIC Schema (PostgREST Default) ─┐'
\echo ''

SELECT 
    schemaname,
    tablename,
    CASE 
        WHEN rowsecurity = false THEN '❌ RLS DISABLED'
        WHEN rowsecurity = true THEN '✅ RLS ENABLED'
    END as rls_status,
    (SELECT count(*) FROM information_schema.columns WHERE table_schema = schemaname AND table_name = tablename) as column_count,
    pg_size_pretty(pg_total_relation_size(to_regclass(schemaname||'.'||tablename))) as size
FROM pg_tables
WHERE schemaname = 'public' 
    AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
    AND rowsecurity = false
ORDER BY tablename;

\echo ''

-- SECTION 2: RLS Policy Summary
\echo '┌─ POLICY COUNT: RLS Policies by Table ─┐'
\echo ''

SELECT 
    t.tablename,
    COUNT(p.policyname) as policy_count,
    CASE 
        WHEN COUNT(p.policyname) = 0 THEN '❌ NO POLICIES'
        WHEN COUNT(p.policyname) < 3 THEN '⚠️  MINIMAL POLICIES'
        ELSE '✅ ADEQUATE POLICIES'
    END as policy_adequacy,
    string_agg(p.policyname, ', ' ORDER BY p.policyname) as policy_names
FROM pg_tables t
LEFT JOIN pg_policies p ON t.tablename = p.tablename AND t.schemaname = p.schemaname
WHERE t.schemaname = 'public' 
    AND t.tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
GROUP BY t.tablename
ORDER BY policy_count ASC, t.tablename;

\echo ''

-- SECTION 3: Data Exposure Risk
\echo '┌─ RISK ASSESSMENT: Row Count & Exposure ─┐'
\echo ''

SELECT 
    schemaname,
    tablename,
    rowsecurity::text as rls_enabled,
    n_live_tup as row_count,
    pg_size_pretty(pg_total_relation_size(to_regclass(schemaname||'.'||tablename))) as table_size,
    CASE 
        WHEN rowsecurity = true THEN '🔒 PROTECTED'
        WHEN rowsecurity = false AND n_live_tup > 1000 THEN '🔴 CRITICAL - UNPROTECTED & LARGE'
        WHEN rowsecurity = false AND n_live_tup > 100 THEN '🟠 HIGH - UNPROTECTED'
        WHEN rowsecurity = false THEN '🟡 MEDIUM - UNPROTECTED'
        ELSE '⚪ UNKNOWN'
    END as risk_level
FROM pg_stat_user_tables
WHERE schemaname = 'public'
ORDER BY n_live_tup DESC, rls_enabled ASC;

\echo ''

-- SECTION 4: Detailed View - Tables Missing RLS
\echo '┌─ DETAILED: All Tables Missing RLS in Public Schema ─┐'
\echo ''

SELECT 
    t.tablename as table_name,
    'public' as schema_name,
    'false' as rls_enabled,
    COALESCE(s.n_live_tup, 0) as row_count,
    (SELECT count(*) FROM information_schema.columns WHERE table_schema = 'public' AND table_name = t.tablename) as columns,
    string_agg(DISTINCT c.column_name, ', ' ORDER BY c.column_name) as column_list
FROM pg_tables t
LEFT JOIN pg_stat_user_tables s ON t.tablename = s.relname AND t.schemaname = s.schemaname
LEFT JOIN information_schema.columns c ON t.tablename = c.table_name AND t.schemaname = c.table_schema
WHERE t.schemaname = 'public' 
    AND t.tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
    AND t.rowsecurity = false
GROUP BY t.tablename, s.n_live_tup
ORDER BY COALESCE(s.n_live_tup, 0) DESC;

\echo ''

-- SECTION 5: Remediation Script Template
\echo '┌─ REMEDIATION: SQL Commands to Enable RLS ─┐'
\echo ''

SELECT 
    'ALTER TABLE ' || schemaname || '.' || tablename || ' ENABLE ROW LEVEL SECURITY;' as enable_rls_command
FROM pg_tables
WHERE schemaname = 'public' 
    AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
    AND rowsecurity = false
ORDER BY tablename;

\echo ''

-- SECTION 6: Summary Statistics
\echo '┌─ SUMMARY STATISTICS ─┐'
\echo ''

SELECT 
    (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as total_public_tables,
    (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = true AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as tables_with_rls,
    (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = false AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) as tables_without_rls,
    ROUND(100.0 * (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND rowsecurity = true AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')) / 
          (SELECT count(*) FROM pg_tables WHERE schemaname = 'public' AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')), 2) as rls_coverage_percent;

\echo ''
\echo '✅ Audit Complete'
\echo ''
