-- Supabase SQL Schema for YouTube Scraper
-- Run this in your Supabase SQL Editor to create the tables

-- ============================================================================
-- CHANNELS TABLE
-- Stores all scraped YouTube channel leads with metadata and status
-- ============================================================================
CREATE TABLE IF NOT EXISTS channels (
    id BIGSERIAL PRIMARY KEY,
    channel_id TEXT UNIQUE NOT NULL,
    channel_name TEXT NOT NULL,
    channel_url TEXT NOT NULL,
    
    -- Channel stats
    subscriber_count INTEGER NOT NULL,
    total_view_count BIGINT NOT NULL,
    total_video_count INTEGER NOT NULL,
    shorts_count INTEGER NOT NULL DEFAULT 0,
    longform_count INTEGER NOT NULL DEFAULT 0,
    
    -- Activity metrics
    last_upload_date TIMESTAMPTZ,
    upload_frequency NUMERIC(5,1) DEFAULT 0,
    avg_views INTEGER DEFAULT 0,
    avg_duration_seconds INTEGER DEFAULT 0,
    engagement_rate NUMERIC(6,4) DEFAULT 0,
    
    -- Scoring and categorization
    priority_score NUMERIC(3,1) NOT NULL,
    primary_niche TEXT NOT NULL,
    
    -- Location and language
    country TEXT DEFAULT '',
    language TEXT DEFAULT '',
    
    -- Contact info
    contact_email TEXT DEFAULT '',
    contact_available BOOLEAN DEFAULT FALSE,
    
    -- Top performing videos (JSON array)
    top_videos JSONB DEFAULT '[]'::jsonb,
    
    -- Lead status tracking
    status TEXT DEFAULT 'new' CHECK (status IN ('new', 'contacted', 'replied', 'converted', 'rejected', 'paused')),
    
    -- Timestamps
    first_seen TIMESTAMPTZ DEFAULT NOW(),
    last_scraped TIMESTAMPTZ DEFAULT NOW(),
    created_at TIMESTAMPTZ DEFAULT NOW(),
    updated_at TIMESTAMPTZ DEFAULT NOW()
);

-- Indexes for common queries
CREATE INDEX IF NOT EXISTS idx_channels_status ON channels(status);
CREATE INDEX IF NOT EXISTS idx_channels_priority_score ON channels(priority_score DESC);
CREATE INDEX IF NOT EXISTS idx_channels_niche ON channels(primary_niche);
CREATE INDEX IF NOT EXISTS idx_channels_first_seen ON channels(first_seen DESC);
CREATE INDEX IF NOT EXISTS idx_channels_contact_available ON channels(contact_available);

-- ============================================================================
-- OUTREACH TABLE
-- Tracks email sequence state for each lead
-- ============================================================================
CREATE TABLE IF NOT EXISTS outreach (
    id BIGSERIAL PRIMARY KEY,
    channel_id TEXT NOT NULL REFERENCES channels(channel_id) ON DELETE CASCADE,
    
    -- Email sequence tracking
    email_number INTEGER NOT NULL CHECK (email_number BETWEEN 1 AND 5),
    sent_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Email metadata
    subject TEXT NOT NULL,
    body TEXT NOT NULL,
    
    -- Response tracking
    opened BOOLEAN DEFAULT FALSE,
    replied BOOLEAN DEFAULT FALSE,
    reply_received_at TIMESTAMPTZ,
    reply_text TEXT,
    
    -- Timestamps
    created_at TIMESTAMPTZ DEFAULT NOW(),
    
    -- Ensure we don't send the same email twice
    UNIQUE(channel_id, email_number)
);

-- Indexes for outreach queries
CREATE INDEX IF NOT EXISTS idx_outreach_channel_id ON outreach(channel_id);
CREATE INDEX IF NOT EXISTS idx_outreach_sent_at ON outreach(sent_at DESC);
CREATE INDEX IF NOT EXISTS idx_outreach_replied ON outreach(replied);

-- ============================================================================
-- HELPER FUNCTIONS
-- ============================================================================

-- Auto-update updated_at timestamp
CREATE OR REPLACE FUNCTION update_updated_at_column()
RETURNS TRIGGER 
SECURITY DEFINER
SET search_path = public
AS $$
BEGIN
    NEW.updated_at = NOW();
    RETURN NEW;
END;
$$ LANGUAGE plpgsql;

CREATE TRIGGER update_channels_updated_at
    BEFORE UPDATE ON channels
    FOR EACH ROW
    EXECUTE FUNCTION update_updated_at_column();

-- ============================================================================
-- ROW LEVEL SECURITY (Optional - enable if you want multi-user access control)
-- ============================================================================
-- ALTER TABLE channels ENABLE ROW LEVEL SECURITY;
-- ALTER TABLE outreach ENABLE ROW LEVEL SECURITY;

-- Example policy: Allow service role full access
-- CREATE POLICY "Service role has full access to channels"
--     ON channels FOR ALL
--     TO service_role
--     USING (true)
--     WITH CHECK (true);

-- CREATE POLICY "Service role has full access to outreach"
--     ON outreach FOR ALL
--     TO service_role
--     USING (true)
--     WITH CHECK (true);

-- ============================================================================
-- SAMPLE QUERIES
-- ============================================================================

-- Get all new leads with contact info, sorted by priority
-- SELECT * FROM channels 
-- WHERE status = 'new' AND contact_available = true 
-- ORDER BY priority_score DESC, first_seen DESC;

-- Get leads ready for email 2 (sent email 1 at least 2 days ago, no email 2 yet)
-- SELECT c.* FROM channels c
-- INNER JOIN outreach o ON c.channel_id = o.channel_id AND o.email_number = 1
-- LEFT JOIN outreach o2 ON c.channel_id = o2.channel_id AND o2.email_number = 2
-- WHERE o.sent_at < NOW() - INTERVAL '2 days'
--   AND o2.id IS NULL
--   AND c.status NOT IN ('converted', 'rejected');

-- Get reply rate by email number
-- SELECT 
--     email_number,
--     COUNT(*) as sent,
--     SUM(CASE WHEN replied THEN 1 ELSE 0 END) as replies,
--     ROUND(100.0 * SUM(CASE WHEN replied THEN 1 ELSE 0 END) / COUNT(*), 2) as reply_rate_pct
-- FROM outreach
-- GROUP BY email_number
-- ORDER BY email_number;
