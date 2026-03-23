"""Create Gmail drafts for BID proposals.

Uses the Gmail API to create a draft email that Dylan can review
and send manually from Gmail. Requires a token file created by
scripts/gmail_setup.py.
"""

import base64
import json
from email.mime.text import MIMEText
from pathlib import Path

from google.oauth2.credentials import Credentials
from google.auth.transport.requests import Request
from googleapiclient.discovery import build

TOKEN_FILE = Path(__file__).parent.parent / "data" / "gmail_token.json"
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def _get_gmail_service():
    """Load credentials and return an authenticated Gmail API service."""
    if not TOKEN_FILE.exists():
        raise FileNotFoundError(
            f"Gmail token not found at {TOKEN_FILE}. "
            "Run 'python scripts/gmail_setup.py' first."
        )

    creds = Credentials.from_authorized_user_info(
        json.loads(TOKEN_FILE.read_text()), SCOPES
    )

    # Refresh the token if it's expired
    if creds.expired and creds.refresh_token:
        creds.refresh(Request())
        TOKEN_FILE.write_text(creds.to_json())

    return build("gmail", "v1", credentials=creds)


def create_draft(to_email: str, subject: str, body: str) -> str:
    """Create a Gmail draft and return the draft ID."""
    service = _get_gmail_service()

    message = MIMEText(body)
    message["to"] = to_email
    message["subject"] = subject

    raw = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft = service.users().drafts().create(
        userId="me",
        body={"message": {"raw": raw}},
    ).execute()

    return draft["id"]
