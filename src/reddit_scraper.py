import requests
import yaml
import json
from datetime import datetime, timezone, timedelta
from pathlib import Path

HEADERS = {"User-Agent": "gigflow/0.1"}
SEEN_POSTS_FILE = Path(__file__).parent.parent / "data" / "seen_posts.json"


def load_config() -> dict:
    config_path = Path(__file__).parent.parent / "config" / "config.yaml"
    with open(config_path) as f:
        return yaml.safe_load(f)


def load_seen_ids() -> set:
    if SEEN_POSTS_FILE.exists():
        return set(json.loads(SEEN_POSTS_FILE.read_text()))
    return set()


def save_seen_ids(ids: set) -> None:
    SEEN_POSTS_FILE.parent.mkdir(exist_ok=True)
    SEEN_POSTS_FILE.write_text(json.dumps(list(ids)))


def fetch_posts(subreddit: str, limit: int = 25) -> list[dict]:
    url = f"https://www.reddit.com/r/{subreddit}/new.json?limit={limit}"
    response = requests.get(url, headers=HEADERS)
    response.raise_for_status()

    posts = []
    for child in response.json()["data"]["children"]:
        d = child["data"]
        posts.append({
            "id": d["id"],
            "title": d["title"],
            "author": d["author"],
            "url": f"https://reddit.com{d['permalink']}",
            "body": d.get("selftext", ""),
            "created_utc": datetime.fromtimestamp(d["created_utc"], tz=timezone.utc).isoformat(),
            "subreddit": d["subreddit"],
        })
    return posts


def is_hiring_post(post: dict, tag: str) -> bool:
    return post["title"].lower().startswith(tag)


def is_recent(post: dict, hours: int) -> bool:
    cutoff = datetime.now(tz=timezone.utc) - timedelta(hours=hours)
    return datetime.fromisoformat(post["created_utc"]) >= cutoff


def matches_keywords(post: dict, keywords: list[str]) -> bool:
    text = (post["title"] + " " + post["body"]).lower()
    return any(kw in text for kw in keywords)


def pre_screen(post: dict, config: dict) -> tuple[bool, str]:
    """Cheap local check before hitting the Claude API. Returns (passes, reason)."""
    cfg = config.get("pre_screen", {})
    text = (post["title"] + " " + post["body"]).lower()

    word_count = len(post["body"].split())
    min_words = cfg.get("min_body_words", 30)
    if word_count < min_words:
        return False, f"body too short ({word_count} words)"

    for phrase in cfg.get("skip_phrases", []):
        if phrase in text:
            return False, f"skip phrase matched: '{phrase}'"

    return True, "ok"


def filter_posts(posts: list[dict], config: dict, seen_ids: set) -> list[dict]:
    tag = config["filters"]["min_title_tag"]
    hours = config["filters"]["max_age_hours"]
    keywords = config["keywords"]
    return [
        p for p in posts
        if p["id"] not in seen_ids
        and is_hiring_post(p, tag)
        and is_recent(p, hours)
        and matches_keywords(p, keywords)
    ]


if __name__ == "__main__":
    config = load_config()
    seen_ids = load_seen_ids()
    all_posts = []

    for subreddit in config["subreddits"]:
        posts = fetch_posts(subreddit)
        print(f"r/{subreddit}: fetched {len(posts)} posts")
        all_posts.extend(posts)

    filtered = filter_posts(all_posts, config, seen_ids)
    print(f"\nTotal: {len(all_posts)} fetched, {len(filtered)} new matches.\n")

    for p in filtered:
        print(f"[r/{p['subreddit']}] {p['title']}")
        print(f"  {p['url']}\n")

    # Mark all fetched post IDs as seen (not just matches)
    new_ids = {p["id"] for p in all_posts}
    save_seen_ids(seen_ids | new_ids)
    print(f"State updated: {len(seen_ids | new_ids)} total seen post IDs.")
