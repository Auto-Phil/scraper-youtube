#!/usr/bin/env python3
"""
Send cold email outreach to qualified YouTube creators.
Tracks emails in Supabase outreach table.
"""

import smtplib
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from datetime import datetime, timezone
from typing import List, Dict
import time

from config import (
    SMTP_HOST, SMTP_PORT, SMTP_USER, SMTP_PASSWORD,
    SUPABASE_URL, SUPABASE_KEY
)
from utils import get_supabase_client, log


def get_email_template(email_number: int, channel_data: dict) -> tuple[str, str]:
    """
    Get email subject and body for a given email number.
    Returns (subject, body) tuple.
    """
    channel_name = channel_data.get('channel_name', 'your channel')
    niche = channel_data.get('primary_niche', 'content')
    
    if email_number == 1:
        subject = f"Thinking about YouTube shorts for {channel_name}?"
        body = f"""Hello there!

Been watching your {niche} content for a while. We recently got to thinking, your long-form stuff has so many moments that would work perfectly as Shorts, but it looks like you haven't really leaned into them consistently.

We'd love to make you a pack of 5 Shorts from your existing videos, completely on us. Just reply to this email or shoot me a text at 484-889-1131 and we'll get started.

Either way, keep making great stuff.

Warmest Regards,
Zack

Zack Whitlock
Auto-Phil | Co-Founder, Head of Automations & AI
Email | zack@auto-phil.com
Mobile | 484-889-1131"""
    
    elif email_number == 2:
        subject = f"{niche} creators on shorts right now"
        body = f"""Hello there!

Quick thought I wanted to share.

Creators in {niche} with a similar sub count to yours are pulling 50K-200K views per Short, even when their long-form averages way less. The algorithm treats Shorts as a completely separate discovery channel.

Most of your catalog would translate really well. You're sitting on a lot of untapped reach.

The offer still stands. We'll make you 5 Shorts from your best clips at no cost. Just reply or text me at 484-889-1131.

Warmest Regards,
Zack

Zack Whitlock
Auto-Phil | Co-Founder, Head of Automations & AI
Email | zack@auto-phil.com
Mobile | 484-889-1131"""
    
    elif email_number == 3:
        subject = f"how a {niche} creator added 40k subs in 3 months"
        body = f"""Hello there!

One of the {niche} creators we work with had a similar setup to yours. Strong long-form library, solid engagement, zero Shorts. Within 3 months of posting repurposed clips, they added 40K subscribers and their long-form views actually went up too.

They didn't change anything about how they make videos. We just gave their existing content a second life.

If you want to see what that looks like for your channel, just reply or text me at 484-889-1131. The pack of 5 is still yours.

Warmest Regards,
Zack

Zack Whitlock
Auto-Phil | Co-Founder, Head of Automations & AI
Email | zack@auto-phil.com
Mobile | 484-889-1131"""
    
    elif email_number == 4:
        subject = f"last call for {channel_name}"
        body = f"""Hello there!

I know you're busy, so I'll keep this short.

The offer for 5 free Shorts from your best content is still on the table, but I'm wrapping up this batch of creators this week.

If you want in, just reply or text 484-889-1131 by Friday. If not, no worries—I'll stop reaching out.

Warmest Regards,
Zack

Zack Whitlock
Auto-Phil | Co-Founder, Head of Automations & AI
Email | zack@auto-phil.com
Mobile | 484-889-1131"""
    
    else:  # email_number == 5
        subject = f"closing the door on this"
        body = f"""Hello there!

This is my last email. I wanted to give you one more chance to grab those 5 free Shorts before I move on to the next batch of creators.

If you're interested, reply or text 484-889-1131 before end of day. If I don't hear from you, I'll assume it's not a fit right now and I won't reach out again.

Either way, best of luck with {channel_name}.

Warmest Regards,
Zack

Zack Whitlock
Auto-Phil | Co-Founder, Head of Automations & AI
Email | zack@auto-phil.com
Mobile | 484-889-1131"""
    
    return subject, body


def send_email(to_email: str, subject: str, body: str) -> bool:
    """
    Send a plain text email via SMTP.
    Returns True if successful, False otherwise.
    """
    if not all([SMTP_HOST, SMTP_USER, SMTP_PASSWORD]):
        log.error("SMTP credentials not configured in .env file")
        return False
    
    try:
        msg = MIMEMultipart('alternative')
        msg['Subject'] = subject
        msg['From'] = f"Zack Whitlock <{SMTP_USER}>"
        msg['To'] = to_email
        
        # Plain text version
        text_part = MIMEText(body, 'plain')
        msg.attach(text_part)
        
        # Send via SMTP
        with smtplib.SMTP(SMTP_HOST, SMTP_PORT) as server:
            server.starttls()
            server.login(SMTP_USER, SMTP_PASSWORD)
            server.send_message(msg)
        
        log.info(f"✓ Email sent to {to_email}")
        return True
        
    except Exception as e:
        log.error(f"✗ Failed to send email to {to_email}: {e}")
        return False


def record_outreach(channel_id: str, email_number: int, subject: str, body: str, success: bool):
    """
    Record the outreach attempt in Supabase.
    """
    try:
        supabase = get_supabase_client()
        
        record = {
            'channel_id': channel_id,
            'email_number': email_number,
            'subject': subject,
            'body': body,
            'sent_at': datetime.now(timezone.utc).isoformat() if success else None,
        }
        
        supabase.table('outreach').upsert(record, on_conflict='channel_id,email_number').execute()
        log.debug(f"Recorded outreach for channel {channel_id}, email #{email_number}")
        
    except Exception as e:
        log.error(f"Failed to record outreach in Supabase: {e}")


def get_leads_to_email(email_number: int = 1, limit: int = None) -> List[Dict]:
    """
    Get leads that are ready for outreach.
    - Must have contact_email
    - Must not have already received this email_number
    - Ordered by priority_score DESC
    """
    try:
        supabase = get_supabase_client()
        
        # Get all channels with email that haven't been contacted for this email_number
        query = supabase.table('channels').select('*').eq('contact_available', True)
        
        if limit:
            query = query.limit(limit)
        
        result = query.order('priority_score', desc=True).execute()
        
        # Filter out channels that already received this email
        leads = []
        for channel in result.data:
            # Check if this email was already sent
            outreach_check = supabase.table('outreach').select('id').eq('channel_id', channel['channel_id']).eq('email_number', email_number).execute()
            
            if len(outreach_check.data) == 0:
                leads.append(channel)
        
        return leads
        
    except Exception as e:
        log.error(f"Error fetching leads: {e}")
        return []


def send_outreach_batch(email_number: int = 1, limit: int = None, dry_run: bool = False):
    """
    Send outreach emails to a batch of leads.
    
    Args:
        email_number: Which email in the sequence (1-5)
        limit: Max number of emails to send (None = all)
        dry_run: If True, don't actually send emails, just show what would be sent
    """
    log.info(f"{'[DRY RUN] ' if dry_run else ''}Starting outreach batch for email #{email_number}")
    
    leads = get_leads_to_email(email_number, limit)
    
    if not leads:
        log.info("No leads found for outreach")
        return
    
    log.info(f"Found {len(leads)} leads to email")
    
    sent_count = 0
    failed_count = 0
    
    for i, lead in enumerate(leads, 1):
        channel_id = lead['channel_id']
        channel_name = lead['channel_name']
        email = lead['contact_email']
        
        # Prepare channel data for template
        channel_data = {
            'channel_name': channel_name,
            'primary_niche': lead.get('primary_niche', 'content'),
        }
        
        # Get email content
        subject, body = get_email_template(email_number, channel_data)
        
        log.info(f"\n[{i}/{len(leads)}] {channel_name}")
        log.info(f"  Email: {email}")
        log.info(f"  Subject: {subject}")
        
        if dry_run:
            log.info(f"  [DRY RUN] Would send email here")
            log.info(f"  Preview:\n{body[:200]}...")
            success = True
        else:
            # Send the email
            success = send_email(email, subject, body)
            
            # Record in Supabase
            record_outreach(channel_id, email_number, subject, body, success)
            
            if success:
                sent_count += 1
                # Small delay to avoid rate limiting
                time.sleep(2)
            else:
                failed_count += 1
    
    log.info(f"\n{'[DRY RUN] ' if dry_run else ''}Outreach batch complete:")
    log.info(f"  Sent: {sent_count}")
    log.info(f"  Failed: {failed_count}")


if __name__ == "__main__":
    import argparse
    
    parser = argparse.ArgumentParser(description='Send cold email outreach to YouTube creators')
    parser.add_argument('--email-number', type=int, default=1, choices=[1, 2, 3, 4, 5],
                        help='Which email in the sequence to send (1-5)')
    parser.add_argument('--limit', type=int, default=None,
                        help='Maximum number of emails to send')
    parser.add_argument('--dry-run', action='store_true',
                        help='Preview emails without actually sending them')
    
    args = parser.parse_args()
    
    send_outreach_batch(
        email_number=args.email_number,
        limit=args.limit,
        dry_run=args.dry_run
    )
