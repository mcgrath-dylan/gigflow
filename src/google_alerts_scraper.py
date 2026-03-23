import re
import hashlib
import feedparser


def strip_html(text):
    """Remove HTML tags from Google Alerts snippets."""
    text = re.sub(r"<br\s*/?>", "\n", text)
    text = re.sub(r"<[^>]+>", "", text)
    return text.strip()


def parse_alert_feed(feed_url):
    """
    Parse a single Google Alerts RSS feed and return posts in the
    standard GigFlow shape: { id, title, body, url, source, created_utc }
    """
    feed = feedparser.parse(feed_url)
    posts = []

    for entry in feed.entries:
        title = strip_html(entry.get("title", ""))
        # Google Alerts uses 'summary' for the snippet
        body = strip_html(entry.get("summary", "") or entry.get("content", [{}])[0].get("value", ""))
        link = entry.get("link", "")

        # Google Alerts wraps links in a redirect — extract the real URL
        if "google.com/url?" in link:
            import urllib.parse
            parsed = urllib.parse.urlparse(link)
            params = urllib.parse.parse_qs(parsed.query)
            link = params.get("url", [link])[0]

        # Generate a stable ID from the link
        url_hash = hashlib.md5(link.encode()).hexdigest()[:12]

        # published_parsed is a time.struct_time; convert to unix timestamp
        created = 0
        if entry.get("published_parsed"):
            import calendar
            created = calendar.timegm(entry.published_parsed)

        posts.append({
            "id": f"galert_{url_hash}",
            "title": title,
            "body": body,
            "url": link,
            "source": "google_alerts",
            "created_utc": created,
        })

    return posts


def get_google_alerts_gigs(config):
    """
    Entry point called by main.py. Reads feed URLs from config,
    parses each feed, and returns the combined post list.
    """
    ga_config = config.get("google_alerts", {})
    if not ga_config.get("enabled", False):
        return []

    feeds = ga_config.get("feeds", [])
    if not feeds:
        print("Google Alerts: enabled but no feed URLs configured. Skipping.")
        return []

    all_posts = []
    for url in feeds:
        posts = parse_alert_feed(url)
        all_posts.extend(posts)

    print(f"Google Alerts: {len(all_posts)} items from {len(feeds)} feed(s).")
    return all_posts
