import anthropic
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

TEMPLATES_DIR = Path(__file__).parent.parent / "config" / "templates"
VALID_TYPES = {"data-cleanup", "doc-writing", "analysis", "general-short"}

client = anthropic.Anthropic()


def load_template(gig_type: str) -> str:
    if gig_type not in VALID_TYPES:
        gig_type = "general-short"
    return (TEMPLATES_DIR / f"{gig_type}.txt").read_text()


def draft_proposal(post: dict) -> str:
    """Fill in the appropriate template using details from the gig posting."""
    gig_type = post.get("gig_type", "general-short")
    template = load_template(gig_type)
    gig_text = f"Title: {post['title']}\n\nBody:\n{post['body'] or '(no body text)'}"

    message = client.messages.create(
        model="claude-haiku-4-5-20251001",
        max_tokens=300,
        system=(
            "You are filling in a proposal template for a freelancer named Dylan. "
            "Replace every bracketed placeholder with specific details from the gig posting. "
            "Keep the total proposal under 150 words. Be direct and specific — no filler phrases. "
            "Return only the filled-in proposal text, nothing else."
        ),
        messages=[
            {"role": "user", "content": f"Gig posting:\n{gig_text}\n\nTemplate:\n{template}"}
        ],
    )

    return message.content[0].text.strip()


if __name__ == "__main__":
    test_post = {
        "id": "test123",
        "title": "[Hiring] Need someone to clean and format a messy Excel spreadsheet ($50)",
        "body": "I have a 500-row Excel file with inconsistent formatting, duplicate entries, and merged cells. Need it cleaned up and delivered as a proper CSV. One-time job, budget is $50.",
        "author": "test_user",
        "url": "https://reddit.com/test",
        "created_utc": "2026-03-11T12:00:00+00:00",
        "subreddit": "forhire",
        "recommendation": "BID",
        "gig_type": "data-cleanup",
    }

    print("Drafting proposal...\n")
    proposal = draft_proposal(test_post)
    print(proposal)
