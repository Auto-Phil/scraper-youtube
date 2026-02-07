"""
Lead management CLI for viewing, filtering, and updating channel statuses.

Usage:
    python manage_leads.py list [--status STATUS] [--niche NICHE] [--limit N]
    python manage_leads.py show CHANNEL_ID
    python manage_leads.py update CHANNEL_ID --status STATUS
    python manage_leads.py stats
"""

import sys
import argparse
from datetime import datetime
from tabulate import tabulate

import config
from utils import log, get_supabase_client, update_channel_status


def list_leads(status=None, niche=None, limit=50, sort_by="priority_score"):
    """List leads with optional filtering."""
    try:
        supabase = get_supabase_client()
        query = supabase.table("channels").select("*")
        
        if status:
            query = query.eq("status", status)
        if niche:
            query = query.ilike("primary_niche", f"%{niche}%")
        
        # Sort by priority score descending by default
        if sort_by == "priority_score":
            query = query.order("priority_score", desc=True)
        elif sort_by == "date":
            query = query.order("first_seen", desc=True)
        
        query = query.limit(limit)
        result = query.execute()
        
        if not result.data:
            print(f"No leads found{' with status=' + status if status else ''}")
            return
        
        # Format for display
        rows = []
        for lead in result.data:
            rows.append([
                lead["channel_id"][:12] + "...",
                lead["channel_name"][:30],
                f"{lead['subscriber_count']:,}",
                lead["shorts_count"],
                lead["longform_count"],
                f"{lead['priority_score']:.1f}",
                lead["primary_niche"][:20],
                lead["status"],
                "✓" if lead["contact_available"] else "✗",
            ])
        
        headers = ["ID", "Name", "Subs", "Shorts", "Long", "Score", "Niche", "Status", "Email"]
        print(f"\n{len(rows)} leads found:\n")
        print(tabulate(rows, headers=headers, tablefmt="simple"))
        print()
        
    except Exception as e:
        log.error("Error listing leads: %s", e)
        sys.exit(1)


def show_lead(channel_id):
    """Show detailed information for a single lead."""
    try:
        supabase = get_supabase_client()
        result = supabase.table("channels").select("*").eq("channel_id", channel_id).execute()
        
        if not result.data:
            print(f"Lead not found: {channel_id}")
            return
        
        lead = result.data[0]
        
        print(f"\n{'='*70}")
        print(f"Channel: {lead['channel_name']}")
        print(f"{'='*70}")
        print(f"Channel ID:       {lead['channel_id']}")
        print(f"URL:              {lead['channel_url']}")
        print(f"Subscribers:      {lead['subscriber_count']:,}")
        print(f"Total Views:      {lead['total_view_count']:,}")
        print(f"Total Videos:     {lead['total_video_count']}")
        print(f"  - Shorts:       {lead['shorts_count']}")
        print(f"  - Long-form:    {lead['longform_count']}")
        print(f"\nMetrics:")
        print(f"  Last Upload:    {lead['last_upload_date'][:10] if lead['last_upload_date'] else 'N/A'}")
        print(f"  Upload Freq:    {lead['upload_frequency']:.1f} videos/month")
        print(f"  Avg Views:      {lead['avg_views']:,}")
        print(f"  Avg Duration:   {lead['avg_duration_seconds'] // 60} min {lead['avg_duration_seconds'] % 60} sec")
        print(f"  Engagement:     {lead['engagement_rate']:.2f}%")
        print(f"\nScoring:")
        print(f"  Priority Score: {lead['priority_score']:.1f}/10")
        print(f"  Primary Niche:  {lead['primary_niche']}")
        print(f"\nLocation:")
        print(f"  Country:        {lead['country'] or 'N/A'}")
        print(f"  Language:       {lead['language'] or 'N/A'}")
        print(f"\nContact:")
        print(f"  Email:          {lead['contact_email'] or 'Not available'}")
        print(f"\nStatus:")
        print(f"  Current:        {lead['status']}")
        print(f"  First Seen:     {lead['first_seen'][:19] if lead['first_seen'] else 'N/A'}")
        print(f"  Last Scraped:   {lead['last_scraped'][:19] if lead['last_scraped'] else 'N/A'}")
        print(f"{'='*70}\n")
        
    except Exception as e:
        log.error("Error showing lead: %s", e)
        sys.exit(1)


def update_lead_status(channel_id, new_status):
    """Update the status of a lead."""
    try:
        update_channel_status(channel_id, new_status)
        print(f"✓ Updated {channel_id} to status '{new_status}'")
    except Exception as e:
        log.error("Error updating lead status: %s", e)
        sys.exit(1)


def show_stats():
    """Show summary statistics about all leads."""
    try:
        supabase = get_supabase_client()
        
        # Total leads
        total = supabase.table("channels").select("id", count="exact").execute()
        
        # By status
        statuses = ["new", "contacted", "replied", "converted", "rejected", "paused"]
        status_counts = {}
        for status in statuses:
            result = supabase.table("channels").select("id", count="exact").eq("status", status).execute()
            status_counts[status] = result.count or 0
        
        # With contact info
        with_email = supabase.table("channels").select("id", count="exact").eq("contact_available", True).execute()
        
        # Top niches
        all_leads = supabase.table("channels").select("primary_niche").execute()
        niche_counts = {}
        for lead in all_leads.data:
            niche = lead["primary_niche"]
            niche_counts[niche] = niche_counts.get(niche, 0) + 1
        top_niches = sorted(niche_counts.items(), key=lambda x: x[1], reverse=True)[:10]
        
        print(f"\n{'='*70}")
        print("LEAD STATISTICS")
        print(f"{'='*70}")
        print(f"Total Leads:          {total.count or 0}")
        print(f"With Contact Email:   {with_email.count or 0}")
        print(f"\nBy Status:")
        for status in statuses:
            count = status_counts[status]
            bar = "█" * (count // 5) if count > 0 else ""
            print(f"  {status:12} {count:4}  {bar}")
        
        print(f"\nTop 10 Niches:")
        for niche, count in top_niches:
            print(f"  {niche:30} {count:3}")
        print(f"{'='*70}\n")
        
    except Exception as e:
        log.error("Error showing stats: %s", e)
        sys.exit(1)


def main():
    parser = argparse.ArgumentParser(description="Manage YouTube scraper leads")
    subparsers = parser.add_subparsers(dest="command", help="Command to run")
    
    # List command
    list_parser = subparsers.add_parser("list", help="List leads")
    list_parser.add_argument("--status", help="Filter by status")
    list_parser.add_argument("--niche", help="Filter by niche (partial match)")
    list_parser.add_argument("--limit", type=int, default=50, help="Max results (default: 50)")
    list_parser.add_argument("--sort", choices=["priority_score", "date"], default="priority_score", help="Sort by")
    
    # Show command
    show_parser = subparsers.add_parser("show", help="Show detailed info for a lead")
    show_parser.add_argument("channel_id", help="Channel ID to show")
    
    # Update command
    update_parser = subparsers.add_parser("update", help="Update lead status")
    update_parser.add_argument("channel_id", help="Channel ID to update")
    update_parser.add_argument("--status", required=True, 
                               choices=["new", "contacted", "replied", "converted", "rejected", "paused"],
                               help="New status")
    
    # Stats command
    subparsers.add_parser("stats", help="Show summary statistics")
    
    args = parser.parse_args()
    
    if not args.command:
        parser.print_help()
        sys.exit(1)
    
    if args.command == "list":
        list_leads(status=args.status, niche=args.niche, limit=args.limit, sort_by=args.sort)
    elif args.command == "show":
        show_lead(args.channel_id)
    elif args.command == "update":
        update_lead_status(args.channel_id, args.status)
    elif args.command == "stats":
        show_stats()


if __name__ == "__main__":
    main()
