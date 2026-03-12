"""
Run once to create the Gigs table in your existing Airtable base.
Finds your base automatically, creates the tracking schema, and
prints the base ID to add to .env as AIRTABLE_BASE_ID.
"""

import os
import requests
from dotenv import load_dotenv

load_dotenv()

PAT = os.getenv("AIRTABLE_PAT")
HEADERS = {
    "Authorization": f"Bearer {PAT}",
    "Content-Type": "application/json",
}
META_URL = "https://api.airtable.com/v0/meta"


def get_base_id() -> str:
    """Find the first base in the account and return its ID."""
    resp = requests.get(f"{META_URL}/bases", headers=HEADERS)
    resp.raise_for_status()
    bases = resp.json().get("bases", [])
    if not bases:
        raise ValueError("No bases found. Create a base in Airtable first.")
    base = bases[0]
    print(f"Using base: {base['name']} ({base['id']})")
    return base["id"]


def create_gigs_table(base_id: str) -> None:
    """Create the Gigs tracking table inside the given base."""
    table_schema = {
        "name": "Gigs",
        "fields": [
            {"name": "Gig Title", "type": "singleLineText"},
            {"name": "Source", "type": "singleLineText"},
            {"name": "Gig Type", "type": "singleLineText"},
            {"name": "Budget (stated)", "type": "singleLineText"},
            {"name": "Recommendation", "type": "singleLineText"},
            {
                "name": "Status",
                "type": "singleSelect",
                "options": {
                    "choices": [
                        {"name": "Surfaced"},
                        {"name": "Applied"},
                        {"name": "Won"},
                        {"name": "Lost"},
                        {"name": "Completed"},
                        {"name": "Skipped"},
                    ]
                },
            },
            {"name": "Dylan Hours", "type": "number", "options": {"precision": 1}},
            {"name": "Revenue", "type": "currency", "options": {"precision": 2, "symbol": "$"}},
            {"name": "Post URL", "type": "url"},
            {"name": "Date Surfaced", "type": "date", "options": {"dateFormat": {"name": "iso"}}},
        ],
    }

    resp = requests.post(
        f"{META_URL}/bases/{base_id}/tables",
        headers=HEADERS,
        json=table_schema,
    )
    resp.raise_for_status()
    table_id = resp.json()["id"]
    print(f"Table created: Gigs ({table_id})")
    print(f"\nAdd this to your .env file:\n  AIRTABLE_BASE_ID={base_id}")


if __name__ == "__main__":
    base_id = get_base_id()
    create_gigs_table(base_id)
