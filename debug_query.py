#!/usr/bin/env python3
"""Debug the lead query to see what's happening."""

from utils import get_supabase_client, log

supabase = get_supabase_client()

# Test the exact query from send_outreach.py
print("\n1. Testing query with contact_available = True:")
result = supabase.table('channels').select('*').eq('contact_available', True).limit(5).execute()
print(f"   Found {len(result.data)} channels")
for ch in result.data:
    print(f"   - {ch['channel_name']}: contact_available={ch.get('contact_available')}")

print("\n2. Testing query without contact_available filter:")
result2 = supabase.table('channels').select('channel_id, channel_name, contact_email, contact_available').limit(5).execute()
print(f"   Found {len(result2.data)} channels")
for ch in result2.data:
    print(f"   - {ch['channel_name']}: email={ch.get('contact_email')}, available={ch.get('contact_available')}")

print("\n3. Checking outreach table:")
outreach_result = supabase.table('outreach').select('*').execute()
print(f"   Found {len(outreach_result.data)} outreach records")
for rec in outreach_result.data:
    print(f"   - Channel: {rec['channel_id']}, Email #{rec['email_number']}")
