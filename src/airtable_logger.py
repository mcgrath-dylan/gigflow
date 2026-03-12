import os
import requests
from datetime import date
from dotenv import load_dotenv

load_dotenv()

BASE_ID = os.getenv("AIRTABLE_BASE_ID")
PAT = os.getenv("AIRTABLE_PAT")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json",
}
TABLE_URL = f"https://api.airtable.com/v0/{BASE_ID}/Gigs"


def log_gig(post: dict) -> None:
    """Write a single gig record to the Airtable Gigs table."""
    record = {
        "fields": {
            "Gig Title": post.get("title", "")[:255],
            "Source": post.get("subreddit", "reddit"),
            "Gig Type": post.get("gig_type", ""),
            "Budget (stated)": post.get("budget", ""),
            "Recommendation": post.get("recommendation", ""),
            "Status": "Surfaced",
            "Post URL": post.get("url", ""),
            "Date Surfaced": date.today().isoformat(),
        }
    }

    resp = requests.post(TABLE_URL, headers=HEADERS, json=record)
    resp.raise_for_status()
    record_id = resp.json()["id"]
    print(f"  [airtable] Logged: {post['title'][:50]} ({record_id})")
