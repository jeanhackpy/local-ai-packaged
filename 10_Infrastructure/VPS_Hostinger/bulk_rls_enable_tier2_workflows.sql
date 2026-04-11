-- ============================================================================
-- TIER 2 RLS HARDENING: Workflow & n8n Execution Data
-- ============================================================================
-- Workflow execution, history, and automation data
-- Execute after Tier 1 (within 24-48 hours)
-- ============================================================================

BEGIN TRANSACTION;

-- Helper function to enable RLS with standard policies on workflow tables
-- Each table gets: SELECT (all/public), INSERT/UPDATE/DELETE (postgres only)

-- ============================================================================
-- Table 1: execution_data (1,276 rows, 34MB) - LARGEST
-- ============================================================================
ALTER TABLE execution_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY execution_data_select_all ON execution_data
    FOR SELECT USING (true);

CREATE POLICY execution_data_insert_postgres ON execution_data
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY execution_data_update_postgres ON execution_data
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY execution_data_delete_postgres ON execution_data
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 2: execution_entity (1,276 rows)
-- ============================================================================
ALTER TABLE execution_entity ENABLE ROW LEVEL SECURITY;

CREATE POLICY execution_entity_select_all ON execution_entity
    FOR SELECT USING (true);

CREATE POLICY execution_entity_insert_postgres ON execution_entity
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY execution_entity_update_postgres ON execution_entity
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY execution_entity_delete_postgres ON execution_entity
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 3: workflow_dependency (686 rows)
-- ============================================================================
ALTER TABLE workflow_dependency ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_dependency_select_all ON workflow_dependency
    FOR SELECT USING (true);

CREATE POLICY workflow_dependency_insert_postgres ON workflow_dependency
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_dependency_update_postgres ON workflow_dependency
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_dependency_delete_postgres ON workflow_dependency
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 4: workflow_publish_history (107 rows)
-- ============================================================================
ALTER TABLE workflow_publish_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_publish_history_select_all ON workflow_publish_history
    FOR SELECT USING (true);

CREATE POLICY workflow_publish_history_insert_postgres ON workflow_publish_history
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_publish_history_update_postgres ON workflow_publish_history
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_publish_history_delete_postgres ON workflow_publish_history
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 5: workflow_statistics (59 rows)
-- ============================================================================
ALTER TABLE workflow_statistics ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_statistics_select_all ON workflow_statistics
    FOR SELECT USING (true);

CREATE POLICY workflow_statistics_insert_postgres ON workflow_statistics
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_statistics_update_postgres ON workflow_statistics
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_statistics_delete_postgres ON workflow_statistics
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 6: insights_by_period (54 rows)
-- ============================================================================
ALTER TABLE insights_by_period ENABLE ROW LEVEL SECURITY;

CREATE POLICY insights_by_period_select_all ON insights_by_period
    FOR SELECT USING (true);

CREATE POLICY insights_by_period_insert_postgres ON insights_by_period
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY insights_by_period_update_postgres ON insights_by_period
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY insights_by_period_delete_postgres ON insights_by_period
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 7: workflow_entity (29 rows)
-- ============================================================================
ALTER TABLE workflow_entity ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_entity_select_all ON workflow_entity
    FOR SELECT USING (true);

CREATE POLICY workflow_entity_insert_postgres ON workflow_entity
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_entity_update_postgres ON workflow_entity
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_entity_delete_postgres ON workflow_entity
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 8: workflow_history (20 rows)
-- ============================================================================
ALTER TABLE workflow_history ENABLE ROW LEVEL SECURITY;

CREATE POLICY workflow_history_select_all ON workflow_history
    FOR SELECT USING (true);

CREATE POLICY workflow_history_insert_postgres ON workflow_history
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_history_update_postgres ON workflow_history
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY workflow_history_delete_postgres ON workflow_history
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 9: webhook_entity (9 rows)
-- ============================================================================
ALTER TABLE webhook_entity ENABLE ROW LEVEL SECURITY;

CREATE POLICY webhook_entity_select_all ON webhook_entity
    FOR SELECT USING (true);

CREATE POLICY webhook_entity_insert_postgres ON webhook_entity
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY webhook_entity_update_postgres ON webhook_entity
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY webhook_entity_delete_postgres ON webhook_entity
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 10: shared_workflow (6 rows)
-- ============================================================================
ALTER TABLE shared_workflow ENABLE ROW LEVEL SECURITY;

CREATE POLICY shared_workflow_select_all ON shared_workflow
    FOR SELECT USING (true);

CREATE POLICY shared_workflow_insert_postgres ON shared_workflow
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY shared_workflow_update_postgres ON shared_workflow
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY shared_workflow_delete_postgres ON shared_workflow
    FOR DELETE USING (current_user = 'postgres');

-- ============================================================================
-- Table 11: insights_metadata (5 rows) - BONUS
-- ============================================================================
ALTER TABLE insights_metadata ENABLE ROW LEVEL SECURITY;

CREATE POLICY insights_metadata_select_all ON insights_metadata
    FOR SELECT USING (true);

CREATE POLICY insights_metadata_insert_postgres ON insights_metadata
    FOR INSERT WITH CHECK (current_user = 'postgres');

CREATE POLICY insights_metadata_update_postgres ON insights_metadata
    FOR UPDATE USING (current_user = 'postgres') WITH CHECK (current_user = 'postgres');

CREATE POLICY insights_metadata_delete_postgres ON insights_metadata
    FOR DELETE USING (current_user = 'postgres');

COMMIT;

-- ============================================================================
-- VERIFICATION
-- ============================================================================
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    (SELECT COUNT(*) FROM pg_policies WHERE tablename = t.tablename) as policy_count
FROM pg_tables t
WHERE tablename IN (
    'execution_data', 'execution_entity', 'workflow_dependency',
    'workflow_publish_history', 'workflow_statistics', 'insights_by_period',
    'workflow_entity', 'workflow_history', 'webhook_entity', 
    'shared_workflow', 'insights_metadata'
)
    AND schemaname = 'public'
ORDER BY tablename;
