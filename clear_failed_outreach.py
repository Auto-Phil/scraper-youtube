#!/usr/bin/env python3
"""Clear failed outreach attempts so we can retry sending."""

from utils import get_supabase_client, log

supabase = get_supabase_client()

# Get all outreach records where sent_at is NULL (failed sends)
result = supabase.table('outreach').select('*').is_('sent_at', 'null').execute()

log.info(f"Found {len(result.data)} failed outreach records")

if len(result.data) > 0:
    # Delete them
    supabase.table('outreach').delete().is_('sent_at', 'null').execute()
    log.info(f"Deleted {len(result.data)} failed outreach records")
    log.info("You can now retry sending emails")
else:
    log.info("No failed records to clean up")
