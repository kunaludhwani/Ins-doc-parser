"""
Add result_viewed column to track if user actually saw the explanation
Run this SQL in Supabase SQL Editor after migration_add_status.sql
"""

-- Add result_viewed column to track user acknowledgment
ALTER TABLE user_behavior_tier2 
ADD COLUMN IF NOT EXISTS result_viewed BOOLEAN DEFAULT FALSE;

-- Add index for queries filtering by result_viewed
CREATE INDEX IF NOT EXISTS idx_tier2_result_viewed ON user_behavior_tier2(result_viewed);

COMMENT ON COLUMN user_behavior_tier2.result_viewed IS 
'TRUE if user actually saw the explanation (frontend sent acknowledgment), FALSE if they closed browser before result displayed';
