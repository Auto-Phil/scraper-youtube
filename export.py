"""
Export results to Supabase (primary) or CSV (fallback).
"""

import csv
from datetime import datetime
from pathlib import Path
from typing import Optional

import config
from utils import log, upsert_channel


# Column order for export
COLUMNS = [
    "timestamp",
    "channel_id",
    "channel_name",
    "channel_url",
    "subscriber_count",
    "total_view_count",
    "total_video_count",
    "shorts_count",
    "longform_count",
    "last_upload_date",
    "upload_frequency",
    "avg_views",
    "avg_duration_seconds",
    "engagement_rate",
    "priority_score",
    "primary_niche",
    "country",
    "language",
    "contact_email",
    "contact_available",
    "top_video_1_title",
    "top_video_1_url",
    "top_video_2_title",
    "top_video_2_url",
    "top_video_3_title",
    "top_video_3_url",
    "status",
]


def build_row(channel: dict, analysis: dict, score: float, niche: str) -> dict:
    """Build a flat dict ready for export from channel + analysis data."""
    top3 = analysis.get("top_3_videos", [])

    # Merge emails: prefer channel about-page email, fall back to description emails
    email = channel.get("contact_email", "")
    if not email:
        desc_emails = analysis.get("emails_from_descriptions", [])
        email = desc_emails[0] if desc_emails else ""

    row = {
        "timestamp": datetime.now().strftime("%Y-%m-%d %H:%M:%S"),
        "channel_id": channel["channel_id"],
        "channel_name": channel["channel_name"],
        "channel_url": channel["channel_url"],
        "subscriber_count": channel["subscriber_count"],
        "total_view_count": channel["total_view_count"],
        "total_video_count": channel["total_video_count"],
        "shorts_count": analysis["shorts_count"],
        "longform_count": analysis["longform_count"],
        "last_upload_date": analysis["last_upload_date"],
        "upload_frequency": analysis["upload_frequency"],
        "avg_views": analysis["avg_views"],
        "avg_duration_seconds": analysis["avg_duration_seconds"],
        "engagement_rate": analysis["engagement_rate"],
        "priority_score": score,
        "primary_niche": niche,
        "country": channel.get("country", ""),
        "language": channel.get("default_language", ""),
        "contact_email": email,
        "contact_available": "yes" if email else "no",
        "top_video_1_title": top3[0]["title"] if len(top3) > 0 else "",
        "top_video_1_url": top3[0]["url"] if len(top3) > 0 else "",
        "top_video_2_title": top3[1]["title"] if len(top3) > 1 else "",
        "top_video_2_url": top3[1]["url"] if len(top3) > 1 else "",
        "top_video_3_title": top3[2]["title"] if len(top3) > 2 else "",
        "top_video_3_url": top3[2]["url"] if len(top3) > 2 else "",
        "status": "new",
    }
    return row


def export_to_supabase(rows: list[dict]) -> bool:
    """Export rows to Supabase. Returns True on success."""
    if not config.SUPABASE_URL or not config.SUPABASE_KEY:
        log.warning("Supabase not configured — falling back to CSV")
        return False

    try:
        for row in rows:
            channel_id = row.get("channel_id")
            channel_name = row.get("channel_name")
            if not channel_id or not channel_name:
                log.warning("Skipping row with missing channel_id or channel_name")
                continue
            
            # Use the existing upsert_channel function from utils
            upsert_channel(channel_id, channel_name, row)
        
        log.info("Exported %d rows to Supabase", len(rows))
        return True

    except Exception as e:
        log.error("Supabase export failed: %s", e)
        return False


def export_to_csv(rows: list[dict]) -> str:
    """Append rows to a timestamped CSV file. Returns the file path."""
    date_str = datetime.now().strftime("%Y%m%d")
    csv_path = config.EXPORT_DIR / f"leads_{date_str}.csv"

    file_exists = csv_path.exists()

    with open(csv_path, "a", newline="", encoding="utf-8") as f:
        writer = csv.DictWriter(f, fieldnames=COLUMNS, extrasaction="ignore")
        if not file_exists:
            writer.writeheader()
        for row in rows:
            writer.writerow(row)

    log.info("Exported %d rows to %s", len(rows), csv_path)
    return str(csv_path)


def export(rows: list[dict]) -> str:
    """
    Try Supabase first; fall back to CSV.
    Returns a description of where the data was exported.
    """
    if not rows:
        log.info("No rows to export")
        return "No data to export"

    if export_to_supabase(rows):
        # Also export to CSV as backup
        csv_path = export_to_csv(rows)
        return f"Supabase (backup CSV: {csv_path})"

    # Fallback if Supabase fails
    path = export_to_csv(rows)
    return f"CSV file: {path}"
