# GigFlow

An end-to-end automated pipeline that discovers freelance gigs across 4 platforms, scores them for fit using AI, drafts tailored proposals, and delivers a ranked daily digest — built from scratch in Python over 13 sessions.

> Built by a Business Analyst on a Data Governance team, learning Python by shipping something real. This repo demonstrates data pipeline design, API integration, config-driven architecture, and AI-assisted automation.

---

## What I Built

```
Reddit (6 subreddits) + HN "Who is hiring?" + Freelancer.com + Google Alerts
        |
  Filter + Deduplicate        <- config-driven, state-tracked per source
        |
  Score with Claude API       <- Sonnet for structured scoring, JSON output
        |
  Draft Proposal (BID only)   <- Haiku + template library, MAYBE/SKIP skip this step
        |
  Discord Digest (daily)      <- BID full detail / MAYBE+SKIP compact one-liners
        |
  Log to Airtable             <- BID + MAYBE posts auto-tracked as CRM
```

Each run: fetch new posts from 4 sources, filter by keyword and recency, deduplicate against persistent state, score each match with a structured AI prompt, generate a tailored proposal for top-tier gigs, deliver a ranked digest, and log actionable gigs for tracking.

---

## Skills Demonstrated

| Skill | Where it shows up |
|---|---|
| Python data pipeline design | `main.py` orchestrates modular stages end-to-end |
| API integration (7 services) | Reddit JSON, HN Algolia, Freelancer.com REST, Google Alerts RSS, Claude API, Airtable API, Discord webhook |
| Config-driven architecture | `config.yaml` separates settings from logic — tune behavior without code changes |
| Incremental state management | `seen_posts.json` prevents reprocessing — only process new data each run |
| Data modeling | Airtable schema designed and provisioned via API (`setup_airtable.py`) |
| Prompt engineering | Structured scoring prompt returns consistent JSON for downstream parsing |
| Infrastructure as code | `setup_airtable.py` creates the table schema programmatically — repeatable, version-controlled |
| Scheduling + orchestration | Windows Task Scheduler triggers daily pipeline runs |

---

## Architecture Decisions

Key tradeoffs made during the build, with rationale:

| Decision | Why |
|---|---|
| Public Reddit JSON over PRAW | Reddit locked down script app registration; public JSON endpoint works without auth and is simpler |
| Discord over email for notifications | Zero-friction setup — no SMTP config, no 2FA, no OAuth |
| Windows Task Scheduler over GitHub Actions | Reddit blocks datacenter IPs with 403s; local residential IP works fine |
| Claude Sonnet for scoring, Haiku for proposals | Sonnet's reasoning quality is needed for nuanced scoring; Haiku is sufficient (and cheaper) for template-based proposal fill-in |
| Config-driven keyword/filter system | Allows tuning pipeline behavior without code changes — iterated through 5+ keyword expansions during the build |
| Separate pre-screen before AI scoring | Deterministic filters (word count, skip phrases) catch obvious non-matches before spending API tokens |

Full decision log with 25+ entries: [`docs/PROJECT_NORTH_STAR.md`](docs/PROJECT_NORTH_STAR.md)

---

## Results

Over the course of the build:

- **4 data sources** integrated (Reddit, HN, Freelancer.com, Google Alerts)
- **7 API services** connected end-to-end
- **9 proposal templates** built, matched to gig type by the scoring engine
- **40+ keywords** tuned across 5 iterations based on real pipeline output
- **27 skip phrases** added to pre-screen, each responding to a specific false-positive pattern
- **Scoring prompt** iterated 4 times with calibration guides, red flag tiers, and complexity penalties

The pipeline successfully automated the entire discovery-to-proposal workflow. Every component works as designed — scraping, filtering, deduplication, scoring, proposal generation, notifications, and CRM logging all run unattended.

---

## Lessons Learned

The pipeline solved the wrong bottleneck. Discovery and scoring worked well, but the freelance marketplace conversion problem turned out to be structural: a zero-reputation freelancer competing against established freelancers with hundreds of reviews can't win on speed or relevance alone. The actual bottleneck was credibility, not discovery.

This is the most valuable lesson in the project: **understanding the difference between building the right thing and building the thing right.** The engineering was sound. The strategy assumption — that better discovery leads to wins — was not validated early enough.

What I'd do differently: validate the riskiest assumption first (can I win a gig manually?) before automating the workflow around it.

---

## Project Structure

```
src/
  main.py              # Pipeline orchestrator — runs all stages in order
  reddit_scraper.py    # Fetch, filter, and deduplicate Reddit posts
  hn_scraper.py        # HN "Who is hiring?" thread discovery, Algolia keyword search
  freelancer_scraper.py # Freelancer.com public API — active fixed-price projects
  google_alerts_scraper.py # Google Alerts RSS feed parsing
  scorer.py            # Claude Sonnet scoring — returns BID / MAYBE / SKIP + rationale
  proposer.py          # Claude Haiku proposal generation from template library
  notifier.py          # Discord digest formatting and delivery
  airtable_logger.py   # Log BID/MAYBE gigs to Airtable automatically
  email_extractor.py   # Extract contact emails from post bodies
  setup_airtable.py    # One-time: create Gigs table schema via Airtable API

config/
  config.yaml          # Sources, keywords, filter settings, pre-screen rules
  scoring_prompt.txt   # Claude scoring instructions (edit to tune without code changes)
  templates/           # 9 proposal templates matched to gig_type from scoring

data/
  seen_posts.json      # Dedup state — processed post IDs across all sources
  hn_state.json        # HN state — last processed thread ID, enforces monthly-only runs

docs/
  PROJECT_NORTH_STAR.md  # Full project spec, architecture decisions, decision log
  TIL.md                 # Learning log — what was built and understood each session
```

---

## Stack

| Component | Tool |
|---|---|
| Language | Python 3.13 |
| Gig sources | Reddit JSON, HN Algolia, Freelancer.com REST, Google Alerts RSS |
| AI scoring | Claude API (Sonnet) |
| AI proposals | Claude API (Haiku) |
| Tracking | Airtable (free tier, schema provisioned via API) |
| Notifications | Discord webhook |
| Scheduling | Windows Task Scheduler |

---

## Documentation

- [`docs/TIL.md`](docs/TIL.md) — Session-by-session learning log covering every build decision
- [`docs/PROJECT_NORTH_STAR.md`](docs/PROJECT_NORTH_STAR.md) — Full project spec, 25+ architecture decisions, and session history
