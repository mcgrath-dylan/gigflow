from pathlib import Path
from dotenv import load_dotenv

# Load .env from project root before any module imports that need API keys
load_dotenv(Path(__file__).parent.parent / ".env", override=True)

from reddit_scraper import load_config, fetch_posts, filter_posts, pre_screen, load_seen_ids, save_seen_ids
from hn_scraper import get_hn_gigs
from freelancer_scraper import get_freelancer_gigs
from google_alerts_scraper import get_google_alerts_gigs
from scorer import score_post
from proposer import draft_proposal
from notifier import send_digest
from airtable_logger import log_gig
from email_extractor import extract_email

try:
    from gmail_drafter import create_draft
    GMAIL_AVAILABLE = True
except ImportError:
    GMAIL_AVAILABLE = False


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

    # Extract: Freelancer.com (daily — API returns active projects, dedup via seen_ids)
    fl_posts = get_freelancer_gigs(config)
    fl_posts = [p for p in fl_posts if p["id"] not in seen_ids]

    # Extract: Google Alerts (daily — RSS feeds, dedup via seen_ids)
    ga_posts = get_google_alerts_gigs(config)
    ga_posts = [p for p in ga_posts if p["id"] not in seen_ids]

    all_posts = reddit_posts + hn_posts + fl_posts + ga_posts
    matched = matched + hn_posts + fl_posts + ga_posts
    print(f"\n{len(reddit_posts)} Reddit + {len(hn_posts)} HN + {len(fl_posts)} Freelancer + {len(ga_posts)} Google Alerts fetched, {len(matched)} new matches after filtering.")

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
        result["contact_email"] = extract_email(result.get("body", ""))
        scored.append(result)
        print(f"  -> {result['recommendation']} (clarity {result['clarity_score']}, ai {result['ai_deliverability_score']})")

    # Sort: BID first, then MAYBE, then SKIP
    order = {"BID": 0, "MAYBE": 1, "SKIP": 2}
    scored.sort(key=lambda p: order.get(p["recommendation"], 3))

    # Draft proposals for BID only; log BID + MAYBE to Airtable
    for post in scored:
        if post["recommendation"] == "BID":
            print(f"Drafting proposal for: {post['title'][:60]}...")
            post["proposal"] = draft_proposal(post)
            log_gig(post)

            # Create Gmail draft if we have a contact email (skip Freelancer — bids go through their platform)
            if GMAIL_AVAILABLE and post.get("contact_email") and post.get("source") != "freelancer":
                try:
                    subject = f"Re: {post['title'][:80]}"
                    create_draft(post["contact_email"], subject, post["proposal"])
                    post["gmail_draft"] = True
                    print(f"  [gmail] Draft created for {post['contact_email']}")
                except Exception as e:
                    print(f"  [gmail] Draft failed: {e}")
                    post["gmail_draft"] = False

        elif post["recommendation"] == "MAYBE":
            post["proposal"] = None
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
