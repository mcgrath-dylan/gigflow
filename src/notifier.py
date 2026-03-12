import requests
import os
from dotenv import load_dotenv

load_dotenv()

WEBHOOK_URL = os.getenv("DISCORD_WEBHOOK_URL")


def format_post(post: dict) -> str:
    rec = post["recommendation"]
    emoji = {"BID": "🟢", "MAYBE": "🟡", "SKIP": "🔴"}.get(rec, "⚪")

    source = post.get("source", "reddit")
    if source == "hackernews":
        source_line = "📌 Hacker News — Who is hiring?"
    else:
        source_line = f"📌 r/{post['subreddit']} | 👤 u/{post['author']}"

    lines = [
        f"{emoji} **{post['title']}**",
        source_line,
        f"🔗 {post['url']}",
        f"**Scores:** Clarity {post['clarity_score']}/10 | AI Deliverability {post['ai_deliverability_score']}/10 | ~{post['estimated_dylan_hours']}h Dylan time",
        f"**Recommendation:** {rec} — {post['reasoning']}",
    ]
    if post["red_flags"]:
        lines.append(f"⚠️ Red flags: {', '.join(post['red_flags'])}")
    if post.get("proposal"):
        label = "📝 **Draft proposal:**" if rec == "BID" else "📝 **Draft proposal** *(MAYBE — review carefully before sending):*"
        lines.append(f"\n{label}\n```\n{post['proposal']}\n```")

    return "\n".join(lines)


def send_digest(scored_posts: list[dict]) -> None:
    if not scored_posts:
        payload = {"content": "✅ GigFlow ran — no new matches today."}
        requests.post(WEBHOOK_URL, json=payload)
        return

    bids = [p for p in scored_posts if p["recommendation"] == "BID"]
    maybes = [p for p in scored_posts if p["recommendation"] == "MAYBE"]

    header = f"## 🔍 GigFlow Digest — {len(scored_posts)} new match(es), {len(bids)} BID, {len(maybes)} MAYBE\n"

    # Discord has a 2000 char limit per message, so send one message per post
    requests.post(WEBHOOK_URL, json={"content": header})

    for post in scored_posts:
        requests.post(WEBHOOK_URL, json={"content": format_post(post)})
