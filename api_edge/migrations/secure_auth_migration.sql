-- Zone 1: API Edge - Secure Authentication Migration
-- This migration creates a secure authentication table for the Sovereign Stack

CREATE TABLE IF NOT EXISTS secure_auth (
    id UUID PRIMARY KEY DEFAULT gen_random_uuid(),
    username TEXT NOT NULL UNIQUE,
    password_hash TEXT NOT NULL,
    created_at TIMESTAMP DEFAULT NOW(),
    last_login TIMESTAMP,
    is_active BOOLEAN DEFAULT TRUE
);

-- Add index for fast lookup
CREATE INDEX IF NOT EXISTS idx_secure_auth_username ON secure_auth(username);

-- For Supabase: ensure RLS is enabled and only trusted roles can access
-- ALTER TABLE secure_auth ENABLE ROW LEVEL SECURITY;
-- CREATE POLICY "Allow trusted" ON secure_auth FOR SELECT USING (is_active = TRUE);
