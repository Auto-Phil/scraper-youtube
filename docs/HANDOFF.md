# Project Handoff Document
**YouTube Channel Scraper for Shorts Repurposing Service**

Last Updated: February 10, 2026  
Author: Zack Whitlock (zack@auto-phil.com)  
Repository: https://github.com/Auto-Phil/ap-optimizedshorts  
**Status: ✅ FULLY OPERATIONAL - EMAILS SENT, PAYMENT PAGE LIVE**

---

## Project Overview

A production-ready YouTube scraper that identifies creators (10K-500K subscribers) who are ideal candidates for a shorts repurposing service. The system searches by niche, filters by content mix, scores leads by priority, and stores them in Supabase for lead management and future email automation.

### Business Context

**Service Offering:** We create 5 sample Shorts from a creator's existing long-form content and send them as a free gift to start the sales conversation.

**Target Audience:** YouTube creators with:
- 10K-500K subscribers
- Strong long-form content (20+ videos, 8+ min avg)
- Little to no Shorts presence (0-5 shorts)
- Active (uploaded within 30 days)
- English-speaking, primarily US/UK/CA/AU/NZ

**Niches:** 38 niches including business, finance, retro gaming, film essays, productivity, fitness, etc.

---

## Current State (As of Feb 10, 2026)

### ✅ What's Working

| Component | Status | Description |
|---|---|---|
| **YouTube API Integration** | ✅ Production | Search, channel details, video analysis with quota tracking |
| **Filtering & Scoring** | ✅ Production | Multi-criteria filtering, 1-10 priority scoring algorithm |
| **Supabase Data Storage** | ✅ Production | Replaced SQLite+Sheets with Supabase for lead storage |
| **CSV Export** | ✅ Production | Backup export to timestamped CSV files |
| **Lead Management CLI** | ✅ Production | `manage_leads.py` - list, filter, view, update lead statuses |
| **Deduplication** | ✅ Production | Prevents re-scraping same channels |
| **Daily Scheduler** | ✅ Production | Runs at 3 AM daily via `scheduler.py` |
| **Email Notifications** | ✅ Production | Daily summary emails (optional) |
| **Language/Region Filters** | ✅ Production | English-only, allowed countries list |
| **Cold Email Templates** | ✅ Complete | 5-email sequence in `email_sequences.md` (5-pack Shorts gift strategy) |
| **CSV Migration Tool** | ✅ Production | `migrate_csv_to_supabase.py` imports existing CSVs |
| **Email Outreach System** | ✅ Production | `send_outreach.py` - SMTP sending with Supabase tracking |
| **Payment Page** | ✅ Live | Stripe integration at https://ap-optimizedshorts.vercel.app |

### ✅ Recent Milestones (Feb 10, 2026)

- **10 cold emails sent** to top-scoring leads (Email #1 of sequence)
- **Payment page deployed** to Vercel with 4 pricing tiers (50% discount)
- **32 qualified leads** in database ready for outreach
- **Email tracking operational** - all sends recorded in `outreach` table

### 🚧 What's Not Done

| Feature | Priority | Notes |
|---|---|---|
| **Automated Email Scheduling** | Medium | Email sending works but requires manual trigger for each sequence number |
| **Reply Detection** | Low | No automated tracking of email replies (manual monitoring only) |
| **Testing** | Medium | No automated tests. Manual testing only |
| **Web Dashboard** | Low | Nice-to-have from original spec |

---

## Changes Made in This Session

### Major Migration: SQLite + Google Sheets → Supabase

**Why:** Better security, scalability, querying, and sets up email sequence tracking.

**Files Modified:**
- `config.py` - Removed Google Sheets config, added Supabase config
- `.env` / `.env.example` - Replaced Sheets credentials with Supabase URL/key
- `utils.py` - Completely rewritten database functions to use Supabase client
- `export.py` - Replaced Google Sheets export with Supabase upsert (CSV as backup)
- `requirements.txt` - Added `supabase==2.11.0`, `tabulate==0.9.0`, removed `gspread`

**Files Created:**
- `supabase_schema.sql` - Database schema (channels + outreach tables)
- `manage_leads.py` - CLI for lead management
- `migrate_csv_to_supabase.py` - CSV import tool

**Files Updated:**
- `README.md` - Completely rewritten with Supabase setup instructions
- `config.py` - Expanded `SEARCH_NICHES` from 11 to 38 niches (added retro gaming, film essays, etc.)

### Git Repository Setup

- Initialized Git repository
- Configured remote: `https://github.com/Auto-Phil/scraper-youtube`
- Author: `zack@auto-phil.com`
- Pushed 4 commits to `master` branch
- `.gitignore` protects `.env` file

### Supabase Setup & Testing (Feb 9, 2026)

- ✅ Supabase project created
- ✅ SQL schema executed successfully
- ✅ API credentials configured in `.env`
- ✅ Test scrape completed: 3 qualified channels found from "retro gaming review" niche
- ✅ Data successfully exported to Supabase and CSV backup
- ✅ Lead management CLI tested and working
- ✅ Quota tracking operational (214/9,500 units used in test)

**Test Results:**
- Searched: 50 channels
- Analyzed: 10 candidates  
- Qualified: 3 leads (e.g., Joey's Retro Handhelds - 80.5K subs, score 8.9/10)
- Export: Supabase ✓, CSV backup ✓
- Performance: 22 seconds total runtime

### Email Template Finalization

User finalized `email_sequences.md` with 5-pack Shorts gift strategy (not just 1 Short). All 5 emails reference the pack of 5 consistently.

### Email Outreach System Built (Feb 10, 2026)

**Files Created:**
- `send_outreach.py` - Main email sending script with 5-email sequence templates
- `check_leads.py` - Utility to verify lead data and contact_available flags
- `clear_failed_outreach.py` - Clean up failed send attempts for retry
- `debug_query.py` - Debug tool for troubleshooting Supabase queries

**Features:**
- SMTP integration via Gmail App Password
- Personalized email templates with channel name and niche
- Automatic deduplication (won't send same email twice)
- Supabase tracking in `outreach` table (sent_at, subject, body)
- Rate limiting (2-second delay between sends)
- Manual trigger for each email number (no automation)
- Dry-run mode for previewing emails before sending

**Email Sequence:**
- Email #1: "The Observation" - Free 5-pack offer
- Email #2: "The Insight" - Shorts performance data (send 2-3 days later)
- Email #3: "The Bridge" - Social proof case study (send 4 days later)
- Email #4: "The Proof" - Specific channel analysis (send 4 days later)
- Email #5: "The Breakup" - Final offer (send 5 days later)

**First Campaign Results:**
- 10 emails sent successfully on Feb 10, 2026
- Recipients: Top 10 leads by priority_score
- All tracked in Supabase `outreach` table
- Zero failures after Gmail App Password configuration

### Payment Page Built (Feb 10, 2026)

**Deployment:**
- Live at: https://ap-optimizedshorts.vercel.app
- Deployed via Vercel (auto-deploys from GitHub)
- Custom domain ready (instructions in payment/README.md)

**Features:**
- 4 pricing tiers: 10-pack ($199), 25-pack ($449), 50-pack ($849), 100-pack ($1,599)
- 50% discount applied via Stripe Payment Links
- Countdown timer (expires Feb 28, 2026)
- Responsive design with horizontal card layout
- Heroicons SVG icons (professional, no emojis)
- Success/cancel pages for post-checkout flow

**Files:**
- `payment/index.html` - Main payment page
- `payment/styles.css` - Responsive styling
- `payment/script.js` - Stripe Payment Links integration
- `payment/success.html` - Post-purchase confirmation
- `payment/cancel.html` - Checkout cancellation page
- `payment/README.md` - Setup and deployment guide

**Stripe Integration:**
- Using Stripe Payment Links (no backend required)
- 4 products configured with 50% discount
- Live mode enabled and tested
- Payment Links stored in `script.js`

### Documentation Added

- `docs/HANDOFF.md` - Complete project handoff document (this file)
- `docs/ARCHITECTURE.md` - System architecture diagrams (Mermaid)
- `docs/CLIP_SELECTION_PROMPT.md` - Viral clip selection prompt for Claude Opus

---

## Architecture

### System Components

```
┌─────────────────────────────────────────────────────────────┐
│                     YouTube Data API v3                      │
│                  (10,000 units/day quota)                    │
└─────────────────────────────────────────────────────────────┘
                              ▲
                              │
                    ┌─────────┴─────────┐
                    │   youtube_api.py   │
                    │  (API wrapper +    │
                    │   quota tracker)   │
                    └─────────┬─────────┘
                              │
                    ┌─────────▼─────────┐
                    │    scraper.py      │
                    │  (orchestration)   │
                    └─────────┬─────────┘
                              │
              ┌───────────────┼───────────────┐
              │               │               │
    ┌─────────▼────────┐ ┌───▼────────┐ ┌───▼────────┐
    │ data_processor.py│ │ export.py  │ │  utils.py  │
    │ (filter & score) │ │ (Supabase) │ │ (DB client)│
    └──────────────────┘ └────┬───────┘ └─────┬──────┘
                              │               │
                              └───────┬───────┘
                                      │
                          ┌───────────▼───────────┐
                          │   Supabase Database   │
                          │  - channels table     │
                          │  - outreach table     │
                          └───────────────────────┘
                                      ▲
                                      │
                    ┌─────────────────┼─────────────────┐
                    │                 │                 │
        ┌───────────▼───────┐ ┌───────▼────────┐ ┌────▼────────┐
        │ manage_leads.py   │ │send_outreach.py│ │ Payment Page│
        │ (CLI interface)   │ │(email sending) │ │  (Vercel)   │
        └───────────────────┘ └────────┬───────┘ └─────────────┘
                                       │
                              ┌────────▼────────┐
                              │  Gmail SMTP     │
                              │ (App Password)  │
                              └─────────────────┘
```

### Data Flow

1. **Search Phase:** `scraper.py` → `youtube_api.py` → YouTube API (search channels by niche)
2. **Analysis Phase:** For each channel → fetch videos → `data_processor.py` filters & scores
3. **Export Phase:** Qualified leads → `export.py` → Supabase (+ CSV backup)
4. **Management:** User runs `manage_leads.py` to view/update lead statuses
5. **Outreach Phase:** User runs `send_outreach.py` → Gmail SMTP → tracks in `outreach` table
6. **Conversion Phase:** Leads click payment link → Stripe Checkout → purchase complete

### Key Files

| File | Purpose | Lines |
|---|---|---|
| `scraper.py` | Main orchestration, runs full scrape cycle | 197 |
| `youtube_api.py` | YouTube API wrapper with quota tracking | 196 |
| `data_processor.py` | Filtering logic, priority scoring algorithm | 207 |
| `export.py` | Supabase export + CSV backup | 148 |
| `utils.py` | Supabase client, logging, quota tracker, email | 237 |
| `config.py` | All configurable settings (niches, filters, weights) | 137 |
| `manage_leads.py` | CLI for lead management | 235 |
| `scheduler.py` | Daily automation wrapper | 43 |
| `send_outreach.py` | Email sending with 5-email sequence | 294 |
| `check_leads.py` | Lead verification utility | 35 |
| `clear_failed_outreach.py` | Clean up failed sends | 20 |
| `payment/index.html` | Payment page (Stripe integration) | 214 |
| `payment/script.js` | Payment Links redirect logic | 98 |

---

## Configuration

### Environment Variables (`.env`)

```bash
# Required
YOUTUBE_API_KEY=your_youtube_api_key
SUPABASE_URL=https://your-project.supabase.co
SUPABASE_KEY=your_supabase_anon_or_service_role_key

# Required for email outreach (Gmail App Password)
SMTP_HOST=smtp.gmail.com
SMTP_PORT=587
SMTP_USER=
SMTP_PASSWORD=your_16_char_app_password  # Generate at myaccount.google.com/apppasswords

# Optional (email notifications for scraper)
NOTIFICATION_EMAIL=your_email@gmail.com
```

### Key Settings (`config.py`)

| Setting | Value | Notes |
|---|---|---|
| `MIN_SUBSCRIBERS` | 10,000 | Lower bound |
| `MAX_SUBSCRIBERS` | 500,000 | Upper bound |
| `MAX_SHORTS_COUNT` | 5 | Max shorts allowed |
| `MIN_LONGFORM_COUNT` | 20 | Min long-form videos |
| `MAX_DAYS_SINCE_UPLOAD` | 30 | Must be active |
| `MIN_AVG_DURATION_SECONDS` | 480 | 8 minutes preferred |
| `ALLOWED_COUNTRIES` | US, GB, CA, AU, NZ, IE | ISO codes |
| `ALLOWED_LANGUAGES` | en | Language prefix |
| `SEARCH_NICHES` | 38 niches | See config.py for full list |
| `MAX_CHANNELS_PER_RUN` | 500 | Daily processing limit |
| `SCHEDULE_TIME` | "03:00" | Daily run time |

### Priority Score Weights

```python
SCORE_WEIGHT_SUBSCRIBERS = 0.30   # Sweet spot: 50K-200K
SCORE_WEIGHT_ENGAGEMENT = 0.25    # (likes + comments) / views
SCORE_WEIGHT_CONSISTENCY = 0.20   # Upload frequency
SCORE_WEIGHT_VIEWS_RATIO = 0.15   # Avg views / subscribers
SCORE_WEIGHT_NICHE_FIT = 0.10     # Keyword match in description
```

---

## Supabase Schema

### `channels` Table

Stores all scraped leads with metadata and status tracking.

**Key Columns:**
- `channel_id` (TEXT, unique) - YouTube channel ID
- `channel_name`, `channel_url`, `subscriber_count`, etc.
- `priority_score` (NUMERIC) - 1-10 lead quality score
- `status` (TEXT) - `new`, `contacted`, `replied`, `converted`, `rejected`, `paused`
- `contact_email` (TEXT) - Extracted from About page or video descriptions
- `top_videos` (JSONB) - Top 3 performing videos
- `first_seen`, `last_scraped`, `created_at`, `updated_at` - Timestamps

**Indexes:**
- `status`, `priority_score`, `primary_niche`, `first_seen`, `contact_available`

### `outreach` Table

Tracks email sequence state for each lead. Used by `send_outreach.py`.

**Key Columns:**
- `channel_id` (FK to channels) - Links to channel being contacted
- `email_number` (1-5) - Which email in the sequence
- `sent_at` (TIMESTAMPTZ) - When email was sent (NULL if failed)
- `subject`, `body` (TEXT) - Email content for record-keeping
- `opened`, `replied` (BOOLEAN) - Response tracking (manual update)
- `reply_received_at`, `reply_text` (TEXT) - Reply details (manual entry)

**Constraints:**
- UNIQUE(channel_id, email_number) - Prevents duplicate sends

**Current Data:**
- 10 records from Feb 10, 2026 email campaign (Email #1)

---

## Usage

### Daily Scraper Run

```bash
# Manual run (all niches)
python scraper.py

# Specific niches
python scraper.py "retro gaming review" "film analysis essay"

# Automated daily (runs at 3 AM)
python scheduler.py
```

### Lead Management

```bash
# List all new leads with contact info
python manage_leads.py list --status new

# Filter by niche
python manage_leads.py list --niche "retro gaming"

# Show detailed info
python manage_leads.py show UCxxxxxxxxxxxxxxxxxx

# Update status
python manage_leads.py update UCxxxxxxxxxxxxxxxxxx --status contacted

# View statistics
python manage_leads.py stats
```

### CSV Migration

```bash
# Import all leads_*.csv files
python migrate_csv_to_supabase.py

# Import specific files
python migrate_csv_to_supabase.py leads_20260206.csv leads_20260207.csv
```

### Email Outreach

```bash
# Preview emails before sending (dry run)
python send_outreach.py --email-number 1 --limit 10 --dry-run

# Send Email #1 to top 10 leads
python send_outreach.py --email-number 1 --limit 10

# Send Email #2 to all eligible leads (2-3 days after Email #1)
python send_outreach.py --email-number 2

# Send to unlimited leads (all eligible)
python send_outreach.py --email-number 1

# Check lead status and fix contact_available flags
python check_leads.py

# Clean up failed send attempts
python clear_failed_outreach.py
```

**Email Sequence Timing:**
- Email #1: Day 1 (initial contact)
- Email #2: Day 3 (2 days later)
- Email #3: Day 7 (4 days later)
- Email #4: Day 11 (4 days later)
- Email #5: Day 16 (5 days later)

**Important Notes:**
- Requires Gmail App Password (not regular password)
- Script automatically skips leads who already received that email number
- All sends tracked in `outreach` table
- 2-second delay between sends to avoid rate limiting
- Max 50 emails/day recommended per Gmail account

---

## API Quota Management

**Daily Limit:** 10,000 units  
**Typical Usage:** ~1,100 units for search (11 niches × 100), ~8,400 for analysis

**Cost Per Operation:**
- `search.list` - 100 units
- `channels.list` - 1 unit
- `playlistItems.list` - 1 unit
- `videos.list` - 1 unit

**Per Channel:** ~5-10 units (1 for channel details, 1-2 for playlist items, 1-5 for video details)

**Expected Output:** 50-100 qualified channels per day

---

## Next Steps for Future Development

### 1. Automated Email Scheduling (Medium Priority)

**What's Done:**
- ✅ SMTP integration with Gmail
- ✅ Template rendering with personalization
- ✅ Sequence state tracking in `outreach` table
- ✅ Rate limiting (2-second delays)
- ✅ Manual trigger for each email number

**What's Needed:**
- Automated scheduler that checks `outreach` table daily
- Sends Email #2 to leads who received Email #1 2+ days ago
- Sends Email #3 to leads who received Email #2 4+ days ago
- Etc. through Email #5

**Suggested Approach:**
- Create `email_scheduler.py`:
  - Query `outreach` table for leads ready for next email
  - Calculate days since last email
  - Call `send_outreach.py` functions programmatically
  - Run daily via cron or `scheduler.py`
- Add to existing `scheduler.py` as second daily task

### 2. Testing

- Unit tests for scoring algorithm
- Integration tests for YouTube API wrapper
- Mock Supabase for testing without live DB

### 3. Monitoring & Alerts

- Track daily scrape success/failure
- Alert on quota exhaustion
- Monitor Supabase usage

### 4. Web Dashboard (Low Priority)

- View leads in a table
- Filter/sort by status, niche, score
- Update statuses via UI
- View email sequence history per lead

---

## Known Issues & Gotchas

### Gmail App Password Required

⚠️ Email sending requires a Gmail App Password, not your regular Gmail password. Generate one at https://myaccount.google.com/apppasswords (requires 2FA enabled).

### Windows `nul` File

A file called `nul` appeared during development (Windows reserved name). It's excluded from Git but may reappear. Safe to ignore.

### Supabase Setup Required

The code won't run until:
1. User creates Supabase project
2. Runs `supabase_schema.sql` in SQL Editor (including the security fix for `update_updated_at_column`)
3. Adds `SUPABASE_URL` and `SUPABASE_KEY` to `.env`

### CSV Backups

Even with Supabase, CSV files are still created as backups. This is intentional for data redundancy.

### Email Sequence is Manual

Email follow-ups (Email #2-5) require manual triggering. There's no automated scheduler yet. User must run `send_outreach.py --email-number 2` manually after 2-3 days.

### Stripe Payment Links

The payment page uses Stripe Payment Links (not Checkout Sessions API). This means:
- No backend required
- Discount must be configured in Stripe Dashboard when creating the Payment Link
- URLs are hardcoded in `payment/script.js`

---

## Dependencies

```
google-api-python-client==2.108.0  # YouTube API
google-auth-oauthlib==1.2.0        # YouTube API auth
google-auth==2.25.2                # YouTube API auth
python-dotenv==1.0.0               # Environment variables
pandas==2.1.4                      # Data processing
schedule==1.2.1                    # Daily scheduler
requests==2.31.0                   # HTTP requests
supabase==2.11.0                   # Supabase client
tabulate==0.9.0                    # CLI table formatting
```

---

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
├── send_outreach.py              # Email sending with 5-email sequence
├── check_leads.py                # Lead verification utility
├── clear_failed_outreach.py      # Clean up failed sends
├── debug_query.py                # Supabase query debugging
├── supabase_schema.sql           # Database schema
├── email_sequences.md            # Cold outreach templates (5-email sequence)
├── payment/                      # Payment page (deployed to Vercel)
│   ├── index.html                # Main payment page
│   ├── styles.css                # Responsive styling
│   ├── script.js                 # Stripe Payment Links
│   ├── success.html              # Post-purchase page
│   ├── cancel.html               # Checkout cancellation
│   ├── README.md                 # Setup guide
│   └── SETUP_GUIDE.md            # Deployment instructions
├── docs/
│   ├── HANDOFF.md                # This file
│   ├── ARCHITECTURE.md           # System architecture diagram
│   └── CLIP_SELECTION_PROMPT.md  # Viral clip selection prompt
├── logs/                         # Daily log files
└── cache/                        # (unused, kept for compatibility)
```

---

## Contact & Resources

- **Repository:** https://github.com/Auto-Phil/ap-optimizedshorts
- **Payment Page:** https://ap-optimizedshorts.vercel.app
- **Author:** Zack Whitlock (zack@auto-phil.com, 484-889-1131)
- **Supabase Dashboard:** https://supabase.com/dashboard
- **YouTube API Console:** https://console.cloud.google.com/apis/credentials
- **Vercel Dashboard:** https://vercel.com/dashboard
- **Gmail App Passwords:** https://myaccount.google.com/apppasswords
- **Email Templates:** See `email_sequences.md` for full 5-email sequence with personalization guide

---

## Quick Start for Next Developer

1. **Clone repo:**
   ```bash
   git clone https://github.com/Auto-Phil/ap-optimizedshorts.git
   cd ap-optimizedshorts
   ```

2. **Install dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

3. **Set up Supabase:**
   - Create project at supabase.com
   - Run `supabase_schema.sql` in SQL Editor
   - Copy URL + key

4. **Configure `.env`:**
   ```bash
   cp .env.example .env
   # Edit .env with your keys (YouTube API, Supabase, Gmail App Password)
   ```

5. **Test scraper:**
   ```bash
   python scraper.py "retro gaming review"
   ```

6. **View results:**
   ```bash
   python manage_leads.py list
   ```

7. **Send test email:**
   ```bash
   python send_outreach.py --email-number 1 --limit 1 --dry-run
   ```

8. **View payment page:**
   - Visit https://ap-optimizedshorts.vercel.app
   - Or run locally: `cd payment && python -m http.server 8000`

9. **Next feature:** Build automated email scheduler (see "Next Steps" above)

---

**End of Handoff Document**
