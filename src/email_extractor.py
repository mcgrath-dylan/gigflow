import re


def extract_email(text: str) -> str | None:
    """Return the first email address found in text, or None."""
    match = re.search(r"[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}", text)
    return match.group(0) if match else None
