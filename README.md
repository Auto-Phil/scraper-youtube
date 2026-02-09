# YouTube Channel Scraper

**Status: ✅ Fully Operational & Tested**

Finds YouTube creators who are good candidates for a shorts creation service. Searches by niche, filters by subscriber count and content mix, scores leads, and exports to Supabase (with CSV backup).

## Quick Start

```bash
# 1. Install dependencies
pip install -r requirements.txt

# 2. Configure .env with your API keys (see Setup below)

# 3. Test with a single niche
python scraper.py "retro gaming review"

# 4. View your leads
python manage_leads.py list
```

## Setup

### 1. Get a YouTube Data API Key

1. Go to [Google Cloud Console](https://console.cloud.google.com/)
2. Create a new project (or select an existing one)
3. Enable **YouTube Data API v3** under APIs & Services → Library
4. Go to APIs & Services → Credentials → Create Credentials → API Key
5. Copy the key

### 2. Install Dependencies

```bash
pip install -r requirements.txt
```

### 3. Set Up Supabase

1. Go to [supabase.com](https://supabase.com) and create a free account
2. Create a new project
3. Go to Project Settings → API
4. Copy your **Project URL** (format: `https://xxxxx.supabase.co`) and **service_role key** (secret key)
5. Go to the SQL Editor and run the contents of `supabase_schema.sql` to create tables

**Important:** Use the API URL format `https://xxxxx.supabase.co`, NOT the dashboard URL

### 4. Configure Environment

```bash
cp .env.example .env
```

Edit `.env` and add your credentials:

```
YOUTUBE_API_KEY=your_youtube_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_key
```

### 5. Migrate Existing Data (Optional)

If you have existing CSV exports to import:

```bash
python migrate_csv_to_supabase.py
```

## Usage

### Run the Scraper

**All niches:**
```bash
python scraper.py
```

**Specific niches:**
```bash
python scraper.py "fitness training" "cooking recipes"
```

**Daily scheduler:**
```bash
python scheduler.py
```

This runs the scraper immediately, then again every day at 3:00 AM (configurable in `config.py`).

### Manage Leads

**List all leads:**
```bash
python manage_leads.py list
```

**Filter by status:**
```bash
python manage_leads.py list --status new
python manage_leads.py list --status contacted
```

**Filter by niche:**
```bash
python manage_leads.py list --niche "retro gaming"
```

**Show detailed info:**
```bash
python manage_leads.py show UCxxxxxxxxxxxxxxxxxx
```

**Update lead status:**
```bash
python manage_leads.py update UCxxxxxxxxxxxxxxxxxx --status contacted
```

**View statistics:**
```bash
python manage_leads.py stats
```

### Windows Task Scheduler Alternative

1. Open Task Scheduler
2. Create Basic Task → set daily trigger
3. Action: Start a Program
   - Program: `python`
   - Arguments: `scraper.py`
   - Start in: `C:\Users\whitl\_dev\yt scraper`

### Linux/Mac Cron Alternative

```bash
crontab -e
```

Add:

```
0 3 * * * cd /path/to/yt-scraper && python scraper.py >> logs/cron.log 2>&1
```

## Configuration

All settings are in `config.py`:

| Setting | Default | Description |
|---|---|---|
| `MIN_SUBSCRIBERS` | 10,000 | Minimum subscriber count |
| `MAX_SUBSCRIBERS` | 500,000 | Maximum subscriber count |
| `MAX_SHORTS_COUNT` | 5 | Max shorts a channel can have |
| `MIN_LONGFORM_COUNT` | 20 | Min long-form videos required |
| `MAX_DAYS_SINCE_UPLOAD` | 30 | Must have uploaded within N days |
| `MIN_AVG_DURATION_SECONDS` | 480 | Preferred avg video length (8 min) |
| `SEARCH_NICHES` | 38 niches | List of search keywords |
| `MAX_CHANNELS_PER_RUN` | 100 | Max channels to analyze per run |
| `SCHEDULE_TIME` | "03:00" | Daily run time (24h format) |

### Priority Score Weights

The 1-10 priority score uses these weights:

- Subscriber count: 30%
- Engagement rate: 25%
- Upload consistency: 20%
- Views/subscriber ratio: 15%
- Niche fit: 10%

## Output

### Supabase Tables

**`channels` table** - All scraped leads with full metadata
**`outreach` table** - Email sequence tracking (for future email automation)

You can view and manage leads via:
- Supabase dashboard (web UI)
- `manage_leads.py` CLI tool
- CSV backups in the project directory

### CSV Backup Columns

| Column | Description |
|---|---|
| `timestamp` | When the channel was scraped |
| `channel_id` | YouTube channel ID |
| `channel_name` | Channel display name |
| `channel_url` | Direct link to the channel |
| `subscriber_count` | Current subscribers |
| `total_view_count` | Lifetime views |
| `shorts_count` | Videos under 60 seconds |
| `longform_count` | Videos over 60 seconds |
| `last_upload_date` | Date of most recent upload |
| `upload_frequency` | Videos per month |
| `avg_views` | Avg views on last 10 videos |
| `engagement_rate` | (likes + comments) / views % |
| `priority_score` | 1-10 lead quality score |
| `primary_niche` | Search niche that found this channel |
| `contact_email` | Email if publicly available |
| `contact_available` | yes/no |
| `top_video_1-3_title` | Top 3 video titles by views |
| `top_video_1-3_url` | Top 3 video URLs |
| `status` | new / contacted / converted / rejected |

## API Quota

YouTube Data API v3 has a 10,000 unit daily quota. Approximate costs:

| Operation | Cost | Usage |
|---|---|---|
| `search.list` | 100 units | Finding channels by keyword |
| `channels.list` | 1 unit | Getting channel stats |
| `playlistItems.list` | 1 unit | Listing uploads |
| `videos.list` | 1 unit | Getting video details |

A typical run searching 11 niches uses ~1,100 units on search alone, leaving ~8,400 for channel analysis. Each channel costs roughly 5-10 units to fully analyze, so expect 50-100 channels per day.

## File Structure

```
youtube_scraper/
├── .env                          # API keys (not in git)
├── .env.example                  # Template
├── .gitignore
├── requirements.txt
├── config.py                     # All configurable settings
├── scraper.py                    # Main entry point
├── youtube_api.py                # YouTube API wrapper
├── data_processor.py             # Filtering and scoring
├── export.py                     # Supabase / CSV export
├── scheduler.py                  # Daily automation
├── utils.py                      # Logging, Supabase client, helpers
├── manage_leads.py               # CLI for lead management
├── migrate_csv_to_supabase.py    # CSV import tool
├── supabase_schema.sql           # Database schema
├── email_sequences.md            # Cold outreach templates
├── logs/                         # Daily log files
└── cache/                        # (unused, kept for compatibility)
```

## Troubleshooting

**"YOUTUBE_API_KEY is not set"**
- Make sure `.env` exists and contains your key
- Make sure `python-dotenv` is installed

**"quotaExceeded" errors**
- You've hit the daily 10,000 unit limit
- Wait until midnight Pacific time for quota reset
- Or request a quota increase in Google Cloud Console

**Supabase connection fails**
- Verify `SUPABASE_URL` and `SUPABASE_KEY` are set in `.env`
- Make sure you've run `supabase_schema.sql` in the Supabase SQL Editor
- Check that your Supabase project is active (free tier doesn't pause)

**No channels found**
- Try broader search terms in `config.py` → `SEARCH_NICHES`
- Loosen filter criteria (lower `MIN_LONGFORM_COUNT`, raise `MAX_SHORTS_COUNT`)
- Check logs in the `logs/` directory for details

**Rate limiting / 503 errors**
- The scraper automatically retries up to 3 times with backoff
- If persistent, reduce `MAX_CHANNELS_PER_RUN`
