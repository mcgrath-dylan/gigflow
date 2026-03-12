from reddit_scraper import load_config, fetch_posts, filter_posts, pre_screen, load_seen_ids, save_seen_ids
from hn_scraper import get_hn_gigs
from scorer import score_post
from proposer import draft_proposal
from notifier import send_digest
from airtable_logger import log_gig


def run():
    print("--- GigFlow pipeline starting ---")

    config = load_config()
    seen_ids = load_seen_ids()

    # Extract: Reddit
    reddit_posts = []
    for subreddit in config["subreddits"]:
        posts = fetch_posts(subreddit)
        print(f"r/{subreddit}: {len(posts)} posts fetched")
        reddit_posts.extend(posts)

    # Filter + deduplicate Reddit posts (checks [hiring] tag, age, keywords, seen_ids)
    matched = filter_posts(reddit_posts, config, seen_ids)

    # Extract: HN (monthly — skips automatically if already run this month)
    # HN posts are pre-filtered in hn_scraper, so they bypass filter_posts
    hn_posts = []
    if config.get("hn", {}).get("enabled", False):
        hn_posts = get_hn_gigs(
            keywords=config["keywords"],
            max_comment_chars=config["hn"].get("max_comment_chars", 800),
            max_comments=config["hn"].get("max_comments", 200),
            require_terms=config["hn"].get("require_terms"),
        )
        hn_posts = [p for p in hn_posts if p["id"] not in seen_ids]

    all_posts = reddit_posts + hn_posts
    matched = matched + hn_posts
    print(f"\n{len(reddit_posts)} Reddit + {len(hn_posts)} HN fetched, {len(matched)} new matches after filtering.")

    # Pre-screen: cheap local filter before hitting Claude API
    to_score = []
    for post in matched:
        passes, reason = pre_screen(post, config)
        if passes:
            to_score.append(post)
        else:
            print(f"  [pre-screen skip] {post['title'][:60]} — {reason}")

    print(f"{len(to_score)} posts pass pre-screen ({len(matched) - len(to_score)} cut).\n")

    # Score each match
    scored = []
    for post in to_score:
        print(f"Scoring: {post['title'][:60]}...")
        result = score_post(post)
        scored.append(result)
        print(f"  → {result['recommendation']} (clarity {result['clarity_score']}, ai {result['ai_deliverability_score']})")

    # Sort: BID first, then MAYBE, then SKIP
    order = {"BID": 0, "MAYBE": 1, "SKIP": 2}
    scored.sort(key=lambda p: order.get(p["recommendation"], 3))

    # Draft proposals + log to Airtable: BID and MAYBE = auto, SKIP = none
    for post in scored:
        if post["recommendation"] in ("BID", "MAYBE"):
            print(f"Drafting proposal for: {post['title'][:60]}...")
            post["proposal"] = draft_proposal(post)
            log_gig(post)
        else:
            post["proposal"] = None

    # Notify
    send_digest(scored)
    print("\nDigest sent to Discord.")

    # Update state
    new_ids = {p["id"] for p in all_posts}
    save_seen_ids(seen_ids | new_ids)
    print(f"State updated: {len(seen_ids | new_ids)} total seen IDs.")
    print("--- GigFlow pipeline complete ---")


if __name__ == "__main__":
    run()
