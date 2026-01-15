-- Neural Anchor Vector Table Migration for Supabase
CREATE TABLE neural_anchors (
    id uuid PRIMARY KEY DEFAULT gen_random_uuid(),
    anchor_name text NOT NULL,
    anchor_vector vector(1536) NOT NULL,
    created_at timestamptz DEFAULT now(),
    metadata jsonb
);

-- Index for fast vector search
CREATE INDEX idx_neural_anchors_vector ON neural_anchors USING ivfflat (anchor_vector vector_l2_ops);

-- Example insert
-- INSERT INTO neural_anchors (anchor_name, anchor_vector, metadata) VALUES ('Genesis Memory', '[0.1, 0.2, ...]', '{"source": "Sarah Core"}');
