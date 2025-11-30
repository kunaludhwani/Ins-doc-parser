"""
Create daily analytics summary table
This provides a simple daily dashboard view of key metrics
"""

-- Create daily analytics summary table
CREATE TABLE IF NOT EXISTS daily_analytics (
    date DATE PRIMARY KEY,
    total_uploads INTEGER DEFAULT 0,
    unique_users INTEGER DEFAULT 0,
    completed_count INTEGER DEFAULT 0,
    abandoned_count INTEGER DEFAULT 0,
    wrong_doc_count INTEGER DEFAULT 0,
    success_rate DECIMAL(5,2),
    created_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata'),
    updated_at TIMESTAMP WITH TIME ZONE DEFAULT (NOW() AT TIME ZONE 'Asia/Kolkata')
);

-- Create index for date range queries
CREATE INDEX IF NOT EXISTS idx_daily_analytics_date ON daily_analytics(date DESC);

-- Add comments
COMMENT ON TABLE daily_analytics IS 'Daily aggregated analytics for dashboard view';
COMMENT ON COLUMN daily_analytics.date IS 'Date of the analytics (YYYY-MM-DD)';
COMMENT ON COLUMN daily_analytics.total_uploads IS 'Total number of upload attempts';
COMMENT ON COLUMN daily_analytics.unique_users IS 'Count of unique users (by user_id)';
COMMENT ON COLUMN daily_analytics.completed_count IS 'Successful uploads (completed)';
COMMENT ON COLUMN daily_analytics.abandoned_count IS 'Users who abandoned (abandoned_by_user)';
COMMENT ON COLUMN daily_analytics.wrong_doc_count IS 'Wrong documents (invalid_file + unreadable_document + rejected_by_sachadvisor)';
COMMENT ON COLUMN daily_analytics.success_rate IS 'Percentage of successful uploads';

-- Create function to refresh daily analytics
CREATE OR REPLACE FUNCTION refresh_daily_analytics(target_date DATE DEFAULT CURRENT_DATE)
RETURNS void AS $$
BEGIN
    INSERT INTO daily_analytics (
        date,
        total_uploads,
        unique_users,
        completed_count,
        abandoned_count,
        wrong_doc_count,
        success_rate
    )
    SELECT 
        target_date,
        COUNT(*) as total_uploads,
        COUNT(DISTINCT user_id) as unique_users,
        COUNT(*) FILTER (WHERE request_status IN ('completed', 'completed_not_viewed')) as completed_count,
        COUNT(*) FILTER (WHERE request_status = 'abandoned_by_user') as abandoned_count,
        COUNT(*) FILTER (WHERE request_status IN ('invalid_file', 'unreadable_document', 'rejected_by_sachadvisor')) as wrong_doc_count,
        ROUND(
            100.0 * COUNT(*) FILTER (WHERE request_status IN ('completed', 'completed_not_viewed')) / 
            NULLIF(COUNT(*), 0), 
            2
        ) as success_rate
    FROM request_logs_tier1
    WHERE DATE(timestamp) = target_date
    ON CONFLICT (date) 
    DO UPDATE SET
        total_uploads = EXCLUDED.total_uploads,
        unique_users = EXCLUDED.unique_users,
        completed_count = EXCLUDED.completed_count,
        abandoned_count = EXCLUDED.abandoned_count,
        wrong_doc_count = EXCLUDED.wrong_doc_count,
        success_rate = EXCLUDED.success_rate,
        updated_at = NOW();
END;
$$ LANGUAGE plpgsql;

-- Create function to get last 30 days analytics
CREATE OR REPLACE FUNCTION get_last_30_days_analytics()
RETURNS TABLE (
    date DATE,
    total_uploads INTEGER,
    unique_users INTEGER,
    completed_count INTEGER,
    abandoned_count INTEGER,
    wrong_doc_count INTEGER,
    success_rate DECIMAL(5,2)
) AS $$
BEGIN
    RETURN QUERY
    SELECT 
        da.date,
        da.total_uploads,
        da.unique_users,
        da.completed_count,
        da.abandoned_count,
        da.wrong_doc_count,
        da.success_rate
    FROM daily_analytics da
    WHERE da.date >= CURRENT_DATE - INTERVAL '30 days'
    ORDER BY da.date DESC;
END;
$$ LANGUAGE plpgsql;

-- Backfill last 30 days
DO $$
DECLARE
    target_date DATE;
BEGIN
    FOR target_date IN 
        SELECT generate_series(
            CURRENT_DATE - INTERVAL '30 days',
            CURRENT_DATE,
            '1 day'::interval
        )::DATE
    LOOP
        PERFORM refresh_daily_analytics(target_date);
    END LOOP;
END $$;

-- Grant permissions (adjust as needed)
-- GRANT SELECT ON daily_analytics TO your_read_only_user;
-- GRANT EXECUTE ON FUNCTION get_last_30_days_analytics() TO your_read_only_user;

-- Example queries:

-- Get last 30 days
-- SELECT * FROM get_last_30_days_analytics();

-- Get today's stats
-- SELECT * FROM daily_analytics WHERE date = CURRENT_DATE;

-- Refresh today's analytics (run this periodically or via cron)
-- SELECT refresh_daily_analytics(CURRENT_DATE);

-- Get weekly summary
-- SELECT 
--     DATE_TRUNC('week', date) as week,
--     SUM(total_uploads) as weekly_uploads,
--     SUM(unique_users) as weekly_users,
--     SUM(completed_count) as weekly_success,
--     ROUND(AVG(success_rate), 2) as avg_success_rate
-- FROM daily_analytics
-- WHERE date >= CURRENT_DATE - INTERVAL '30 days'
-- GROUP BY week
-- ORDER BY week DESC;
