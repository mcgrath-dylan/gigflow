"""One-time OAuth2 setup for Gmail API access.

Run this script interactively to authorize GigFlow to create Gmail drafts.
It will open your browser for Google sign-in, then save a refresh token
to data/gmail_token.json for the pipeline to use automatically.

Prerequisites:
  1. Create a Google Cloud project at https://console.cloud.google.com
  2. Enable the Gmail API
  3. Create OAuth 2.0 credentials (Desktop app type)
  4. Download the JSON and save it as config/gmail_credentials.json
"""

from pathlib import Path
from google_auth_oauthlib.flow import InstalledAppFlow

PROJECT_ROOT = Path(__file__).parent.parent
CREDENTIALS_FILE = PROJECT_ROOT / "config" / "gmail_credentials.json"
TOKEN_FILE = PROJECT_ROOT / "data" / "gmail_token.json"

# Only request permission to compose/create drafts, not read all mail
SCOPES = ["https://www.googleapis.com/auth/gmail.compose"]


def main():
    if not CREDENTIALS_FILE.exists():
        print(f"Missing credentials file: {CREDENTIALS_FILE}")
        print("Download your OAuth client JSON from Google Cloud Console")
        print("and save it as config/gmail_credentials.json")
        return

    flow = InstalledAppFlow.from_client_secrets_file(str(CREDENTIALS_FILE), SCOPES)
    creds = flow.run_local_server(port=0)

    TOKEN_FILE.write_text(creds.to_json())
    print(f"Token saved to {TOKEN_FILE}")
    print("Gmail API is now authorized. The pipeline can create drafts.")


if __name__ == "__main__":
    main()
