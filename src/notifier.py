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
    elif source == "freelancer":
        source_line = "📌 Freelancer.com"
    elif source == "google_alerts":
        source_line = "📌 Google Alerts"
    else:
        source_line = f"📌 r/{post['subreddit']} | 👤 u/{post['author']}"

    lines = [
        f"{emoji} **{post['title']}**",
        source_line,
        f"🔗 {post['url']}",
        f"**Scores:** Clarity {post['clarity_score']}/10 | AI Deliverability {post['ai_deliverability_score']}/10 | QA Feasibility {post.get('qa_feasibility_score', 'N/A')}/10 | ~{post['estimated_dylan_hours']}h Dylan time",
        f"**Recommendation:** {rec} — {post['reasoning']}",
    ]
    if post["red_flags"]:
        lines.append(f"⚠️ Red flags: {', '.join(post['red_flags'])}")
    if post.get("proposal"):
        lines.append(f"\n📝 **Draft proposal:**\n```\n{post['proposal']}\n```")
    if post.get("gmail_draft"):
        lines.append("📧 Gmail draft created — check your Drafts folder")

    return "\n".join(lines)


def send_digest(scored_posts: list[dict]) -> None:
    if not scored_posts:
        payload = {"content": "✅ GigFlow ran — no new matches today."}
        requests.post(WEBHOOK_URL, json=payload)
        return

    bids = [p for p in scored_posts if p["recommendation"] == "BID"]
    maybes = [p for p in scored_posts if p["recommendation"] == "MAYBE"]
    skips = [p for p in scored_posts if p["recommendation"] == "SKIP"]

    header = f"## 🔍 GigFlow Digest — {len(bids)} BID, {len(maybes)} MAYBE, {len(skips)} SKIP ({len(scored_posts)} total scored)\n"
    requests.post(WEBHOOK_URL, json={"content": header})

    # Full detail for BID posts only
    for post in bids:
        requests.post(WEBHOOK_URL, json={"content": format_post(post)})

    # Compact one-liners for MAYBE posts (no proposals drafted)
    if maybes:
        maybe_lines = []
        for p in maybes:
            c = p.get("clarity_score", "?")
            a = p.get("ai_deliverability_score", "?")
            q = p.get("qa_feasibility_score", "?")
            reason = p.get("reasoning", "no reason given")
            title = p.get("title", "Untitled")[:60]
            maybe_lines.append(f"🟡 **{title}** — C:{c} A:{a} Q:{q} — {reason}")
        maybe_block = "**MAYBEs:**\n" + "\n".join(maybe_lines)
        while maybe_block:
            chunk, maybe_block = maybe_block[:1900], maybe_block[1900:]
            requests.post(WEBHOOK_URL, json={"content": chunk})

    # Compact one-liners for SKIP posts
    if skips:
        skip_lines = []
        for p in skips:
            c = p.get("clarity_score", "?")
            a = p.get("ai_deliverability_score", "?")
            q = p.get("qa_feasibility_score", "?")
            reason = p.get("reasoning", "no reason given")
            title = p.get("title", "Untitled")[:60]
            skip_lines.append(f"🔴 **{title}** — C:{c} A:{a} Q:{q} — {reason}")
        skip_block = "**SKIPs:**\n" + "\n".join(skip_lines)
        while skip_block:
            chunk, skip_block = skip_block[:1900], skip_block[1900:]
            requests.post(WEBHOOK_URL, json={"content": chunk})
