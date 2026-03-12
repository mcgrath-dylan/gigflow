from reddit_scraper import load_config, fetch_posts, filter_posts, pre_screen, load_seen_ids, save_seen_ids
from scorer import score_post
from proposer import draft_proposal
from notifier import send_digest
from airtable_logger import log_gig


def run():
    print("--- GigFlow pipeline starting ---")

    config = load_config()
    seen_ids = load_seen_ids()

    # Extract
    all_posts = []
    for subreddit in config["subreddits"]:
        posts = fetch_posts(subreddit)
        print(f"r/{subreddit}: {len(posts)} posts fetched")
        all_posts.extend(posts)

    # Filter + deduplicate
    matched = filter_posts(all_posts, config, seen_ids)
    print(f"\n{len(all_posts)} total fetched, {len(matched)} new matches after filtering.")

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
