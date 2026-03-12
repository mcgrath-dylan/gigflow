import json
import re
import requests
from datetime import datetime
from pathlib import Path

ALGOLIA_API = "https://hn.algolia.com/api/v1"
STATE_FILE = Path("data/hn_state.json")


# --- Thread discovery ---

def find_monthly_thread():
    """
    Use Algolia's HN search API to find this month's 'Ask HN: Who is hiring?' thread.
    Uses search_by_date so the most recent thread comes first.
    Returns the thread ID as a string, or None if not found.
    """
    response = requests.get(
        f"{ALGOLIA_API}/search_by_date",
        params={
            "query": "Ask HN Who is hiring",
            "tags": "ask_hn",
            "hitsPerPage": 5,
        }
    )
    response.raise_for_status()

    current_month = datetime.now().strftime("%Y-%m")
    for hit in response.json()["hits"]:
        title = hit.get("title", "").lower()
        created = hit.get("created_at", "")
        if "who is hiring" in title and created.startswith(current_month):
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


# --- Comment search via Algolia ---

def strip_html(text):
    """HN API returns basic HTML. Convert <p> to newlines, strip all other tags."""
    text = re.sub(r"<p>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def search_thread_comments(thread_id, keywords, max_per_keyword=20):
    """
    Search within a thread's comments using Algolia's server-side search.
    Runs one query per keyword, deduplicates, and returns unique comment dicts.

    This replaces the old approach of fetching 200+ comments individually via
    Firebase — a handful of Algolia calls vs hundreds of HTTP requests.
    """
    seen_ids = set()
    comments = []

    for keyword in keywords:
        response = requests.get(
            f"{ALGOLIA_API}/search",
            params={
                "query": keyword,
                "tags": f"comment,story_{thread_id}",
                "hitsPerPage": max_per_keyword,
            }
        )
        response.raise_for_status()

        for hit in response.json()["hits"]:
            cid = hit["objectID"]
            if cid in seen_ids:
                continue
            seen_ids.add(cid)
            comments.append(hit)

    return comments


# --- Main entry point ---

def get_hn_gigs(keywords, max_comment_chars=800, require_terms=None, **_kwargs):
    """
    Find this month's HN 'Who is hiring?' thread, search for comments matching
    keywords via Algolia, and return them as a list of dicts — same shape as
    reddit_scraper output so the rest of the pipeline works unchanged.

    Returns [] immediately if the thread was already processed this month.
    """
    thread_id = find_monthly_thread()
    if not thread_id:
        print("HN: No 'Who is hiring?' thread found for this month.")
        return []

    if already_processed(thread_id):
        print(f"HN: Thread {thread_id} already processed this month. Skipping.")
        return []

    print(f"HN: Found thread {thread_id}. Searching comments by keyword...")
    comments = search_thread_comments(thread_id, keywords)
    print(f"HN: {len(comments)} unique comments matched across {len(keywords)} keywords.")

    gigs = []
    for hit in comments:
        raw_text = hit.get("comment_text", "") or ""
        if not raw_text:
            continue

        text = strip_html(raw_text)
        if len(text) < 50:
            continue

        if require_terms:
            text_lower = text.lower()
            if not any(t.lower() in text_lower for t in require_terms):
                continue

        first_line = text.split("\n")[0][:80]

        gigs.append({
            "id": f"hn_{hit['objectID']}",
            "title": f"[HN] {first_line}",
            "body": text[:max_comment_chars],
            "url": f"https://news.ycombinator.com/item?id={hit['objectID']}",
            "source": "hackernews",
            "created_utc": hit.get("created_at_i", 0),
        })

    save_state(thread_id)
    print(f"HN: {len(gigs)} posts passed to pipeline for scoring.")
    return gigs
