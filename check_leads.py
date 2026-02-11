#!/usr/bin/env python3
"""
Quick script to check leads in database and fix contact_available flag.
"""

from utils import get_supabase_client, log

def check_and_fix_leads():
    """Check leads and fix contact_available flag if needed."""
    supabase = get_supabase_client()
    
    # Get all channels with contact_email
    result = supabase.table('channels').select('channel_id, channel_name, contact_email, contact_available').execute()
    
    channels_with_email = [ch for ch in result.data if ch.get('contact_email')]
    
    log.info(f"Found {len(channels_with_email)} channels with email addresses")
    
    # Fix any that have contact_available = False
    fixed_count = 0
    for channel in channels_with_email:
        if not channel.get('contact_available'):
            log.info(f"Fixing contact_available for: {channel['channel_name']}")
            supabase.table('channels').update({'contact_available': True}).eq('channel_id', channel['channel_id']).execute()
            fixed_count += 1
    
    log.info(f"Fixed {fixed_count} channels")
    
    # Show the leads ready for outreach
    ready_leads = supabase.table('channels').select('channel_name, contact_email, priority_score').eq('contact_available', True).order('priority_score', desc=True).execute()
    
    log.info(f"\n{len(ready_leads.data)} leads ready for outreach:")
    for i, lead in enumerate(ready_leads.data[:10], 1):
        log.info(f"  {i}. {lead['channel_name']} - {lead['contact_email']} (score: {lead['priority_score']:.1f})")

if __name__ == "__main__":
    check_and_fix_leads()
