"""
Add request_status column to tier1 table for tracking upload lifecycle
Run this SQL in Supabase SQL Editor
"""

-- Add status column to track request lifecycle
ALTER TABLE request_logs_tier1 
ADD COLUMN IF NOT EXISTS request_status VARCHAR(20) DEFAULT 'processing';

-- Add index for status queries
CREATE INDEX IF NOT EXISTS idx_tier1_request_status ON request_logs_tier1(request_status);

-- Valid statuses (USER-FACING):
-- 'processing' - Upload started, analyzing in progress (loading screen)
-- 'completed_not_viewed' - Backend finished processing but user hasn't seen result yet (response in transit)
-- 'completed' - User saw the explanation (frontend sent acknowledgment)
-- 'invalid_file' - Wrong file type, too many pages, file too large (validation error)
-- 'unreadable_document' - Cannot extract text (poor scan, corrupted, image quality)
-- 'rejected_by_sachadvisor' - Not an insurance document (AI classified as non-insurance)
-- 'abandoned_by_user' - User closed window/tab during loading
-- 'system_error' - Backend error (API failure, unexpected exception)

COMMENT ON COLUMN request_logs_tier1.request_status IS 
'User-facing status: processing, completed_not_viewed, completed, invalid_file, unreadable_document, rejected_by_sachadvisor, abandoned_by_user, system_error';
