-- ============================================================================
-- TIER 1 RLS HARDENING: CRITICAL Security-Sensitive Tables
-- ============================================================================
-- Tables with credentials, tokens, and keys
-- Execute immediately - these are HIGHEST PRIORITY
-- ============================================================================

BEGIN TRANSACTION;

-- ============================================================================
-- Table 1: user_api_keys
-- Risk: API authentication credentials
-- ============================================================================
ALTER TABLE user_api_keys ENABLE ROW LEVEL SECURITY;

CREATE POLICY user_api_keys_select_postgres ON user_api_keys
    FOR SELECT 
    USING (current_user = 'postgres');

CREATE POLICY user_api_keys_insert_postgres ON user_api_keys
    FOR INSERT 
    WITH CHECK (current_user = 'postgres');

CREATE POLICY user_api_keys_update_postgres ON user_api_keys
    FOR UPDATE 
    USING (current_user = 'postgres')
    WITH CHECK (current_user = 'postgres');

CREATE POLICY user_api_keys_delete_postgres ON user_api_keys
    FOR DELETE 
    USING (current_user = 'postgres');

-- ============================================================================
-- Table 2: oauth_access_tokens
-- Risk: OAuth tokens, refresh tokens
-- ============================================================================
ALTER TABLE oauth_access_tokens ENABLE ROW LEVEL SECURITY;

CREATE POLICY oauth_access_tokens_select_postgres ON oauth_access_tokens
    FOR SELECT 
    USING (current_user = 'postgres');

CREATE POLICY oauth_access_tokens_insert_postgres ON oauth_access_tokens
    FOR INSERT 
    WITH CHECK (current_user = 'postgres');

CREATE POLICY oauth_access_tokens_update_postgres ON oauth_access_tokens
    FOR UPDATE 
    USING (current_user = 'postgres')
    WITH CHECK (current_user = 'postgres');

CREATE POLICY oauth_access_tokens_delete_postgres ON oauth_access_tokens
    FOR DELETE 
    USING (current_user = 'postgres');

-- ============================================================================
-- Table 3: binary_data
-- Risk: Could contain sensitive files (96MB!)
-- ============================================================================
ALTER TABLE binary_data ENABLE ROW LEVEL SECURITY;

CREATE POLICY binary_data_select_postgres ON binary_data
    FOR SELECT 
    USING (current_user = 'postgres');

CREATE POLICY binary_data_insert_postgres ON binary_data
    FOR INSERT 
    WITH CHECK (current_user = 'postgres');

CREATE POLICY binary_data_update_postgres ON binary_data
    FOR UPDATE 
    USING (current_user = 'postgres')
    WITH CHECK (current_user = 'postgres');

CREATE POLICY binary_data_delete_postgres ON binary_data
    FOR DELETE 
    USING (current_user = 'postgres');

-- ============================================================================
-- Table 4: refresh_tokens (if exists)
-- Risk: JWT refresh tokens
-- ============================================================================
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'refresh_tokens') THEN
        EXECUTE 'ALTER TABLE refresh_tokens ENABLE ROW LEVEL SECURITY';
        
        EXECUTE 'CREATE POLICY refresh_tokens_select_postgres ON refresh_tokens
            FOR SELECT 
            USING (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY refresh_tokens_insert_postgres ON refresh_tokens
            FOR INSERT 
            WITH CHECK (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY refresh_tokens_update_postgres ON refresh_tokens
            FOR UPDATE 
            USING (current_user = ''postgres'')
            WITH CHECK (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY refresh_tokens_delete_postgres ON refresh_tokens
            FOR DELETE 
            USING (current_user = ''postgres'')';
    END IF;
END $$;

-- ============================================================================
-- Table 5: sessions (if exists)
-- Risk: Session management
-- ============================================================================
DO $$
BEGIN
    IF EXISTS (SELECT 1 FROM pg_tables WHERE tablename = 'sessions') THEN
        EXECUTE 'ALTER TABLE sessions ENABLE ROW LEVEL SECURITY';
        
        EXECUTE 'CREATE POLICY sessions_select_postgres ON sessions
            FOR SELECT 
            USING (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY sessions_insert_postgres ON sessions
            FOR INSERT 
            WITH CHECK (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY sessions_update_postgres ON sessions
            FOR UPDATE 
            USING (current_user = ''postgres'')
            WITH CHECK (current_user = ''postgres'')';
        
        EXECUTE 'CREATE POLICY sessions_delete_postgres ON sessions
            FOR DELETE 
            USING (current_user = ''postgres'')';
    END IF;
END $$;

COMMIT;

-- ============================================================================
-- VERIFICATION
-- ============================================================================
SELECT 
    tablename,
    rowsecurity as rls_enabled,
    (SELECT COUNT(*) FROM pg_policies WHERE tablename = t.tablename) as policy_count
FROM pg_tables t
WHERE tablename IN ('user_api_keys', 'oauth_access_tokens', 'binary_data', 'refresh_tokens', 'sessions')
    AND schemaname = 'public'
ORDER BY tablename;
