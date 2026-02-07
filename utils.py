"""
Helper utilities: logging, quota tracking, database, and email.
"""

import logging
import smtplib
import json
from datetime import datetime, timezone
from email.mime.text import MIMEText
from pathlib import Path
from typing import Optional

from supabase import create_client, Client

import config


# ── Logging ──────────────────────────────────────────────────────────────────

def setup_logger(name: str = "yt_scraper") -> logging.Logger:
    logger = logging.getLogger(name)
    if logger.handlers:
        return logger

    logger.setLevel(logging.DEBUG)

    # Console handler (INFO+)
    ch = logging.StreamHandler()
    ch.setLevel(logging.INFO)
    ch.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(message)s", "%H:%M:%S"))
    logger.addHandler(ch)

    # File handler (DEBUG+)
    log_file = config.LOGS_DIR / f"scraper_{datetime.now().strftime('%Y%m%d')}.log"
    fh = logging.FileHandler(log_file, encoding="utf-8")
    fh.setLevel(logging.DEBUG)
    fh.setFormatter(logging.Formatter("%(asctime)s  %(levelname)-8s  %(name)s  %(message)s"))
    logger.addHandler(fh)

    return logger


log = setup_logger()


# ── Quota tracker ────────────────────────────────────────────────────────────

class QuotaTracker:
    """Tracks YouTube API quota usage for the current day."""

    def __init__(self):
        self._used = 0
        self._limit = config.API_QUOTA_LIMIT - config.API_QUOTA_SAFETY_MARGIN

    @property
    def used(self) -> int:
        return self._used

    @property
    def remaining(self) -> int:
        return max(0, self._limit - self._used)

    def consume(self, endpoint: str, count: int = 1):
        cost = config.QUOTA_COST.get(endpoint, 1) * count
        self._used += cost
        log.debug("Quota: +%d (%s) → %d / %d used", cost, endpoint, self._used, self._limit)

    def can_afford(self, endpoint: str, count: int = 1) -> bool:
        cost = config.QUOTA_COST.get(endpoint, 1) * count
        return (self._used + cost) <= self._limit

    def summary(self) -> str:
        return f"Quota used: {self._used} / {self._limit} ({self.remaining} remaining)"


# ── Supabase client for data storage ────────────────────────────────────────

def get_supabase_client() -> Client:
    """Get or create Supabase client instance."""
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        raise RuntimeError(
            "SUPABASE_URL and SUPABASE_KEY must be set in .env file. "
            "Get them from: https://supabase.com/dashboard/project/_/settings/api"
        )
    return create_client(config.SUPABASE_URL, config.SUPABASE_KEY)


def init_db():
    """Verify Supabase connection. Tables should already exist (run supabase_schema.sql first)."""
    try:
        supabase = get_supabase_client()
        # Test connection by counting channels
        result = supabase.table("channels").select("id", count="exact").limit(1).execute()
        log.info("Supabase connection verified (%d channels in database)", result.count or 0)
    except Exception as e:
        log.error("Supabase connection failed: %s", e)
        log.error("Make sure you've run supabase_schema.sql in your Supabase SQL Editor")
        raise


def channel_exists(channel_id: str) -> bool:
    """Check if a channel already exists in the database."""
    try:
        supabase = get_supabase_client()
        result = supabase.table("channels").select("id").eq("channel_id", channel_id).limit(1).execute()
        return len(result.data) > 0
    except Exception as e:
        log.error("Error checking if channel exists: %s", e)
        return False


def upsert_channel(channel_id: str, channel_name: str, data: dict):
    """Insert or update a channel record in Supabase."""
    try:
        supabase = get_supabase_client()
        
        # Prepare the record
        record = {
            "channel_id": channel_id,
            "channel_name": channel_name,
            "channel_url": data.get("channel_url", ""),
            "subscriber_count": data.get("subscriber_count", 0),
            "total_view_count": data.get("total_view_count", 0),
            "total_video_count": data.get("total_video_count", 0),
            "shorts_count": data.get("shorts_count", 0),
            "longform_count": data.get("longform_count", 0),
            "last_upload_date": data.get("last_upload_date"),
            "upload_frequency": data.get("upload_frequency", 0),
            "avg_views": data.get("avg_views", 0),
            "avg_duration_seconds": data.get("avg_duration_seconds", 0),
            "engagement_rate": data.get("engagement_rate", 0),
            "priority_score": data.get("priority_score", 0),
            "primary_niche": data.get("primary_niche", ""),
            "country": data.get("country", ""),
            "language": data.get("language", ""),
            "contact_email": data.get("contact_email", ""),
            "contact_available": bool(data.get("contact_email")),
            "top_videos": json.dumps([
                {"title": data.get("top_video_1_title", ""), "url": data.get("top_video_1_url", "")},
                {"title": data.get("top_video_2_title", ""), "url": data.get("top_video_2_url", "")},
                {"title": data.get("top_video_3_title", ""), "url": data.get("top_video_3_url", "")},
            ]),
            "status": data.get("status", "new"),
            "last_scraped": datetime.now(timezone.utc).isoformat(),
        }
        
        # Upsert (insert or update on conflict)
        supabase.table("channels").upsert(record, on_conflict="channel_id").execute()
        log.debug("Upserted channel %s to Supabase", channel_id)
        
    except Exception as e:
        log.error("Error upserting channel %s: %s", channel_id, e)
        raise


def update_channel_status(channel_id: str, status: str):
    """Update the status of a channel."""
    valid_statuses = ['new', 'contacted', 'replied', 'converted', 'rejected', 'paused']
    if status not in valid_statuses:
        raise ValueError(f"Invalid status '{status}'. Must be one of: {valid_statuses}")
    
    try:
        supabase = get_supabase_client()
        supabase.table("channels").update({"status": status}).eq("channel_id", channel_id).execute()
        log.info("Updated channel %s status to '%s'", channel_id, status)
    except Exception as e:
        log.error("Error updating channel status: %s", e)
        raise


def get_all_channel_ids() -> set:
    """Get all channel IDs from the database for deduplication."""
    try:
        supabase = get_supabase_client()
        result = supabase.table("channels").select("channel_id").execute()
        return {row["channel_id"] for row in result.data}
    except Exception as e:
        log.error("Error fetching channel IDs: %s", e)
        return set()


# ── Email notification ───────────────────────────────────────────────────────

def send_email_report(subject: str, body: str):
    if not all([config.SMTP_HOST, config.SMTP_USER, config.SMTP_PASSWORD, config.NOTIFICATION_EMAIL]):
        log.debug("Email not configured — skipping notification")
        return

    msg = MIMEText(body)
    msg["Subject"] = subject
    msg["From"] = config.SMTP_USER
    msg["To"] = config.NOTIFICATION_EMAIL

    try:
        with smtplib.SMTP(config.SMTP_HOST, config.SMTP_PORT) as server:
            server.starttls()
            server.login(config.SMTP_USER, config.SMTP_PASSWORD)
            server.send_message(msg)
        log.info("Email report sent to %s", config.NOTIFICATION_EMAIL)
    except Exception as e:
        log.error("Failed to send email: %s", e)


# ── Misc helpers ─────────────────────────────────────────────────────────────

def iso_to_seconds(duration_iso: str) -> int:
    """Convert ISO 8601 duration (PT#H#M#S) to total seconds."""
    duration_iso = duration_iso.replace("PT", "")
    hours = minutes = seconds = 0
    if "H" in duration_iso:
        h_part, duration_iso = duration_iso.split("H")
        hours = int(h_part)
    if "M" in duration_iso:
        m_part, duration_iso = duration_iso.split("M")
        minutes = int(m_part)
    if "S" in duration_iso:
        s_part = duration_iso.replace("S", "")
        seconds = int(s_part)
    return hours * 3600 + minutes * 60 + seconds


def days_since(date_str: str) -> int:
    """Return number of days between an ISO date string and now."""
    dt = datetime.fromisoformat(date_str.replace("Z", "+00:00"))
    return (datetime.now(timezone.utc) - dt).days
