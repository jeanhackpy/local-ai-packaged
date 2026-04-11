-- ============================================================================
-- BULK RLS ENABLEMENT: All Unprotected Tables (Automated)
-- ============================================================================
-- This script enables RLS on ALL remaining tables in public schema
-- that don't already have RLS enabled
-- 
-- Strategy: Enable RLS with generic policies:
--   - SELECT: Allow all (public browsing)
--   - INSERT/UPDATE/DELETE: Postgres role only (admin/service operations)
-- 
-- Timing: Execute after backup. Can take 1-2 minutes on 83 tables.
-- ============================================================================

BEGIN TRANSACTION;

-- Generate and execute dynamic SQL for each unprotected table
DO $$
DECLARE
    v_table record;
    v_policy_select text;
    v_policy_insert text;
    v_policy_update text;
    v_policy_delete text;
BEGIN
    -- Loop through all tables without RLS in public schema
    FOR v_table IN
        SELECT tablename
        FROM pg_tables
        WHERE schemaname = 'public'
            AND NOT rowsecurity
            AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
        ORDER BY tablename
    LOOP
        RAISE NOTICE 'Enabling RLS on table: %', v_table.tablename;
        
        -- Enable RLS
        EXECUTE format('ALTER TABLE %I ENABLE ROW LEVEL SECURITY', v_table.tablename);
        
        -- Create SELECT policy (public read)
        v_policy_select := format(
            'CREATE POLICY %I ON %I FOR SELECT USING (true)',
            v_table.tablename || '_select_all',
            v_table.tablename
        );
        EXECUTE v_policy_select;
        
        -- Create INSERT policy (admin only)
        v_policy_insert := format(
            'CREATE POLICY %I ON %I FOR INSERT WITH CHECK (current_user = ''postgres'')',
            v_table.tablename || '_insert_postgres',
            v_table.tablename
        );
        EXECUTE v_policy_insert;
        
        -- Create UPDATE policy (admin only)
        v_policy_update := format(
            'CREATE POLICY %I ON %I FOR UPDATE USING (current_user = ''postgres'') WITH CHECK (current_user = ''postgres'')',
            v_table.tablename || '_update_postgres',
            v_table.tablename
        );
        EXECUTE v_policy_update;
        
        -- Create DELETE policy (admin only)
        v_policy_delete := format(
            'CREATE POLICY %I ON %I FOR DELETE USING (current_user = ''postgres'')',
            v_table.tablename || '_delete_postgres',
            v_table.tablename
        );
        EXECUTE v_policy_delete;
        
    END LOOP;
    
    RAISE NOTICE 'RLS enablement complete!';
END $$;

COMMIT;

-- ============================================================================
-- VERIFICATION: Count tables now with RLS
-- ============================================================================
SELECT 
    COUNT(*) as total_public_tables,
    SUM(CASE WHEN rowsecurity THEN 1 ELSE 0 END) as now_protected,
    SUM(CASE WHEN NOT rowsecurity THEN 1 ELSE 0 END) as still_unprotected
FROM pg_tables
WHERE schemaname = 'public'
    AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns');

-- ============================================================================
-- DETAILED VERIFICATION: Status of all tables
-- ============================================================================
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    (SELECT COUNT(*) FROM pg_policies WHERE tablename = t.tablename) as policy_count,
    CASE 
        WHEN rowsecurity THEN '✅ PROTECTED'
        ELSE '❌ UNPROTECTED'
    END as status
FROM pg_tables t
WHERE schemaname = 'public'
    AND tablename NOT IN ('spatial_ref_sys', 'geometry_columns')
ORDER BY rls_enabled DESC, tablename;
