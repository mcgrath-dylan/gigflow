from reddit_scraper import load_config, fetch_posts, filter_posts, load_seen_ids, save_seen_ids
from scorer import score_post
from notifier import send_digest


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

    # Score each match
    scored = []
    for post in matched:
        print(f"Scoring: {post['title'][:60]}...")
        result = score_post(post)
        scored.append(result)
        print(f"  → {result['recommendation']} (clarity {result['clarity_score']}, ai {result['ai_deliverability_score']})")

    # Sort: BID first, then MAYBE, then SKIP
    order = {"BID": 0, "MAYBE": 1, "SKIP": 2}
    scored.sort(key=lambda p: order.get(p["recommendation"], 3))

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
