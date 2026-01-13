-- Ace Tokens Table Migration for Supabase
CREATE TABLE ace_tokens (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    token text NOT NULL,
    timestamp timestamptz DEFAULT now(),
    metadata jsonb
);

-- Example insert
-- INSERT INTO ace_tokens (token, metadata) VALUES ('Genesis_10x_AceToken', '{"source": "Sarah Core"}');
