"""
Migrate existing CSV leads to Supabase.

This script reads all CSV files in the current directory and imports them into Supabase.
It handles deduplication automatically via the upsert logic.

Usage:
    python migrate_csv_to_supabase.py [csv_file1.csv csv_file2.csv ...]
    
    If no files specified, it will import all leads_*.csv files in the directory.
"""

import sys
import csv
from pathlib import Path
from datetime import datetime

import config
from utils import log, get_supabase_client, upsert_channel


def migrate_csv_file(csv_path: Path) -> tuple[int, int]:
    """
    Migrate a single CSV file to Supabase.
    Returns (rows_processed, rows_imported).
    """
    rows_processed = 0
    rows_imported = 0
    
    log.info("Processing %s ...", csv_path.name)
    
    try:
        with open(csv_path, 'r', encoding='utf-8') as f:
            reader = csv.DictReader(f)
            
            for row in reader:
                rows_processed += 1
                
                channel_id = row.get('channel_id')
                channel_name = row.get('channel_name')
                
                if not channel_id or not channel_name:
                    log.warning("  Row %d: Missing channel_id or channel_name, skipping", rows_processed)
                    continue
                
                try:
                    # Convert numeric fields
                    data = {
                        'channel_id': channel_id,
                        'channel_name': channel_name,
                        'channel_url': row.get('channel_url', ''),
                        'subscriber_count': int(row.get('subscriber_count', 0) or 0),
                        'total_view_count': int(row.get('total_view_count', 0) or 0),
                        'total_video_count': int(row.get('total_video_count', 0) or 0),
                        'shorts_count': int(row.get('shorts_count', 0) or 0),
                        'longform_count': int(row.get('longform_count', 0) or 0),
                        'last_upload_date': row.get('last_upload_date', ''),
                        'upload_frequency': float(row.get('upload_frequency', 0) or 0),
                        'avg_views': int(row.get('avg_views', 0) or 0),
                        'avg_duration_seconds': int(row.get('avg_duration_seconds', 0) or 0),
                        'engagement_rate': float(row.get('engagement_rate', 0) or 0),
                        'priority_score': float(row.get('priority_score', 0) or 0),
                        'primary_niche': row.get('primary_niche', ''),
                        'country': row.get('country', ''),
                        'language': row.get('language', ''),
                        'contact_email': row.get('contact_email', ''),
                        'top_video_1_title': row.get('top_video_1_title', ''),
                        'top_video_1_url': row.get('top_video_1_url', ''),
                        'top_video_2_title': row.get('top_video_2_title', ''),
                        'top_video_2_url': row.get('top_video_2_url', ''),
                        'top_video_3_title': row.get('top_video_3_title', ''),
                        'top_video_3_url': row.get('top_video_3_url', ''),
                        'status': row.get('status', 'new'),
                    }
                    
                    upsert_channel(channel_id, channel_name, data)
                    rows_imported += 1
                    
                    if rows_imported % 10 == 0:
                        log.info("  Imported %d/%d rows...", rows_imported, rows_processed)
                    
                except Exception as e:
                    log.error("  Row %d (%s): Error importing - %s", rows_processed, channel_id, e)
                    continue
        
        log.info("✓ %s: %d/%d rows imported", csv_path.name, rows_imported, rows_processed)
        return rows_processed, rows_imported
        
    except Exception as e:
        log.error("Error reading %s: %s", csv_path, e)
        return 0, 0


def main():
    log.info("=" * 70)
    log.info("CSV to Supabase Migration")
    log.info("=" * 70)
    
    # Verify Supabase connection
    try:
        supabase = get_supabase_client()
        result = supabase.table("channels").select("id", count="exact").limit(1).execute()
        log.info("Supabase connected (%d existing channels)", result.count or 0)
    except Exception as e:
        log.error("Failed to connect to Supabase: %s", e)
        log.error("Make sure SUPABASE_URL and SUPABASE_KEY are set in .env")
        log.error("And that you've run supabase_schema.sql in your Supabase SQL Editor")
        sys.exit(1)
    
    # Get CSV files to process
    if len(sys.argv) > 1:
        csv_files = [Path(f) for f in sys.argv[1:]]
    else:
        # Find all leads_*.csv files
        csv_files = sorted(Path('.').glob('leads_*.csv'))
    
    if not csv_files:
        log.warning("No CSV files found to import")
        log.info("Usage: python migrate_csv_to_supabase.py [file1.csv file2.csv ...]")
        sys.exit(0)
    
    log.info("Found %d CSV file(s) to import", len(csv_files))
    print()
    
    total_processed = 0
    total_imported = 0
    
    for csv_file in csv_files:
        if not csv_file.exists():
            log.warning("File not found: %s", csv_file)
            continue
        
        processed, imported = migrate_csv_file(csv_file)
        total_processed += processed
        total_imported += imported
    
    print()
    log.info("=" * 70)
    log.info("Migration Complete")
    log.info("  Total rows processed: %d", total_processed)
    log.info("  Total rows imported:  %d", total_imported)
    log.info("  Skipped/errors:       %d", total_processed - total_imported)
    log.info("=" * 70)
    
    # Show final count
    try:
        result = supabase.table("channels").select("id", count="exact").limit(1).execute()
        log.info("Total channels in Supabase: %d", result.count or 0)
    except:
        pass


if __name__ == "__main__":
    main()
