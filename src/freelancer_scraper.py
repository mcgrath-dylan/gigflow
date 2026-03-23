import requests
from datetime import datetime, timezone


# Freelancer.com job category IDs relevant to Dylan's profile
DEFAULT_JOB_IDS = [13, 116, 36, 43]  # Python, Web Scraping, Data Processing, Data Entry

API_BASE = "https://www.freelancer.com/api/projects/0.1/projects/active/"


def fetch_freelancer_projects(job_ids=None, limit=25, min_budget_usd=20):
    """
    Query the Freelancer.com public API for active fixed-price projects
    matching the given job category IDs.

    Returns a list of dicts in the standard GigFlow post shape:
      { id, title, body, url, source, created_utc }
    """
    if job_ids is None:
        job_ids = DEFAULT_JOB_IDS

    params = {
        "compact": "true",
        "job_details": "true",
        "full_description": "true",
        "limit": limit,
        "sort_field": "submitdate",
        "project_types[]": "fixed",
    }
    # Freelancer API wants repeated keys for array params
    for jid in job_ids:
        params.setdefault("jobs[]", [])
    # requests doesn't handle repeated keys well with a dict,
    # so build the query string manually
    query_parts = [
        ("compact", "true"),
        ("job_details", "true"),
        ("full_description", "true"),
        ("limit", str(limit)),
        ("sort_field", "submitdate"),
        ("project_types[]", "fixed"),
    ]
    for jid in job_ids:
        query_parts.append(("jobs[]", str(jid)))

    response = requests.get(API_BASE, params=query_parts)
    response.raise_for_status()
    data = response.json()

    projects = data.get("result", {}).get("projects", [])
    gigs = []

    for proj in projects:
        # Build budget string for context
        budget = proj.get("budget", {})
        currency = proj.get("currency", {})
        budget_min = budget.get("minimum", 0)
        budget_max = budget.get("maximum", 0)
        currency_code = currency.get("code", "USD")
        exchange_rate = currency.get("exchange_rate", 1.0)

        # Convert to USD for the min_budget filter
        budget_max_usd = budget_max * exchange_rate
        if budget_max_usd < min_budget_usd:
            continue

        # Skill tags from the jobs array
        skills = [j.get("name", "") for j in proj.get("jobs", [])]
        skills_str = ", ".join(skills)

        budget_str = f"{currency.get('sign', '$')}{budget_min:,.0f}–{budget_max:,.0f} {currency_code}"

        # Build body: description + metadata the scorer can use
        description = proj.get("description") or proj.get("preview_description", "")
        body = f"{description}\n\nBudget: {budget_str}\nSkills: {skills_str}"

        seo_url = proj.get("seo_url", "")
        proj_id = proj.get("id", 0)

        gigs.append({
            "id": f"fl_{proj_id}",
            "title": proj.get("title", "Untitled"),
            "body": body,
            "url": f"https://www.freelancer.com/projects/{seo_url}",
            "source": "freelancer",
            "created_utc": proj.get("submitdate", 0),
        })

    return gigs


def get_freelancer_gigs(config):
    """
    Entry point called by main.py. Reads settings from config dict,
    fetches projects, and returns the standard post list.
    """
    fl_config = config.get("freelancer", {})
    if not fl_config.get("enabled", False):
        return []

    job_ids = fl_config.get("job_ids", DEFAULT_JOB_IDS)
    limit = fl_config.get("limit", 25)
    min_budget_usd = fl_config.get("min_budget_usd", 20)

    print("Freelancer.com: Fetching active projects...")
    gigs = fetch_freelancer_projects(
        job_ids=job_ids,
        limit=limit,
        min_budget_usd=min_budget_usd,
    )
    print(f"Freelancer.com: {len(gigs)} projects passed budget filter.")
    return gigs
