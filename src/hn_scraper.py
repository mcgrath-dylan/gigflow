import json
import re
import requests
from datetime import datetime
from pathlib import Path

HN_API = "https://hacker-news.firebaseio.com/v0"
ALGOLIA_API = "https://hn.algolia.com/api/v1"
STATE_FILE = Path("data/hn_state.json")


# --- Thread discovery ---

def find_monthly_thread():
    """
    Use Algolia's HN search API to find this month's
    'Ask HN: Freelancer? Seeking freelancer?' thread.
    Returns the thread ID as a string, or None if not found.
    """
    response = requests.get(
        f"{ALGOLIA_API}/search",
        params={
            "query": "Ask HN Freelancer Seeking Freelancer",
            "tags": "ask_hn",
            "hitsPerPage": 10,
        }
    )
    response.raise_for_status()

    current_month = datetime.now().strftime("%Y-%m")
    for hit in response.json()["hits"]:
        title = hit.get("title", "").lower()
        created = hit.get("created_at", "")  # ISO string: "2026-03-01T..."
        if "freelancer" in title and "seeking" in title and created.startswith(current_month):
            return str(hit["objectID"])

    return None


# --- State management ---

def already_processed(thread_id):
    """Return True if we've already run against this thread ID this month."""
    if not STATE_FILE.exists():
        return False
    state = json.loads(STATE_FILE.read_text())
    return state.get("last_thread_id") == thread_id


def save_state(thread_id):
    STATE_FILE.parent.mkdir(exist_ok=True)
    STATE_FILE.write_text(json.dumps({
        "last_thread_id": thread_id,
        "last_run": datetime.now().isoformat(),
    }, indent=2))


# --- Comment fetching ---

def fetch_comment_ids(thread_id):
    """Return the list of top-level comment IDs on the thread."""
    response = requests.get(f"{HN_API}/item/{thread_id}.json")
    response.raise_for_status()
    return response.json().get("kids", [])


def fetch_comment(comment_id):
    response = requests.get(f"{HN_API}/item/{comment_id}.json")
    response.raise_for_status()
    return response.json()


# --- Comment filtering ---

def strip_html(text):
    """HN API returns basic HTML. Convert <p> to newlines, strip all other tags."""
    text = re.sub(r"<p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def is_seeking_post(text):
    """
    HN's freelancer thread has a loose convention:
      SEEKING  — client looking to hire
      AVAILABLE — freelancer advertising themselves

    We only want SEEKING posts. Any post not starting with SEEKING is skipped.
    """
    if not text:
        return False
    first_line = text.strip().split("\n")[0].upper()
    return first_line.startswith("SEEKING")


def matches_keywords(text, keywords):
    text_lower = text.lower()
    return any(kw.lower() in text_lower for kw in keywords)


# --- Main entry point ---

def get_hn_gigs(keywords, max_comment_chars=800, max_comments=200):
    """
    Find this month's HN freelancer thread, fetch SEEKING posts that match
    keywords, and return them as a list of dicts — same shape as reddit_scraper
    output so the rest of the pipeline works unchanged.

    Returns [] immediately if the thread was already processed this month.
    """
    thread_id = find_monthly_thread()
    if not thread_id:
        print("HN: No thread found for this month.")
        return []

    if already_processed(thread_id):
        print(f"HN: Thread {thread_id} already processed this month. Skipping.")
        return []

    print(f"HN: Found thread {thread_id}. Fetching up to {max_comments} comments...")
    comment_ids = fetch_comment_ids(thread_id)[:max_comments]

    gigs = []
    for cid in comment_ids:
        comment = fetch_comment(cid)

        raw_text = comment.get("text", "")
        if not raw_text:
            continue

        text = strip_html(raw_text)

        if not is_seeking_post(text):
            continue

        if not matches_keywords(text, keywords):
            continue

        first_line = text.split("\n")[0][:80]

        gigs.append({
            "id": f"hn_{cid}",
            "title": f"[HN] {first_line}",
            "text": text[:max_comment_chars],
            "url": f"https://news.ycombinator.com/item?id={cid}",
            "source": "hackernews",
            "created_utc": comment.get("time", 0),
        })

    save_state(thread_id)
    print(f"HN: {len(gigs)} matching SEEKING posts after keyword filter.")
    return gigs
