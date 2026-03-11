import anthropic
import json
from pathlib import Path
from dotenv import load_dotenv

load_dotenv()

PROMPT_FILE = Path(__file__).parent.parent / "config" / "scoring_prompt.txt"
client = anthropic.Anthropic()


def load_prompt() -> str:
    return PROMPT_FILE.read_text()


def score_post(post: dict) -> dict:
    """Send a post to Claude for scoring. Returns the post with scores added."""
    system_prompt = load_prompt()
    gig_text = f"Title: {post['title']}\n\nBody:\n{post['body'] or '(no body text)'}"

    message = client.messages.create(
        model="claude-sonnet-4-6",
        max_tokens=512,
        messages=[
            {"role": "user", "content": gig_text}
        ],
        system=system_prompt,
    )

    raw = message.content[0].text.strip().removeprefix("```json").removeprefix("```").removesuffix("```").strip()
    scores = json.loads(raw)
    return {**post, **scores}


if __name__ == "__main__":
    # Test with a fake post so we can verify scoring without waiting for real matches
    test_post = {
        "id": "test123",
        "title": "[Hiring] Need someone to clean and format a messy Excel spreadsheet ($50)",
        "body": "I have a 500-row Excel file with inconsistent formatting, duplicate entries, and merged cells. Need it cleaned up and delivered as a proper CSV. One-time job, budget is $50.",
        "author": "test_user",
        "url": "https://reddit.com/test",
        "created_utc": "2026-03-11T12:00:00+00:00",
        "subreddit": "forhire",
    }

    print("Scoring test post...\n")
    result = score_post(test_post)

    print(f"Title: {result['title']}")
    print(f"Clarity:          {result['clarity_score']}/10")
    print(f"AI Deliverability:{result['ai_deliverability_score']}/10")
    print(f"Dylan hours:      {result['estimated_dylan_hours']}")
    print(f"Budget mentioned: {result['budget_mentioned']}")
    print(f"Red flags:        {result['red_flags']}")
    print(f"Recommendation:   {result['recommendation']}")
    print(f"Reasoning:        {result['reasoning']}")
