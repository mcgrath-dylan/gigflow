# GigFlow

A real, running pipeline that finds freelance gigs, scores them for fit, drafts proposals, and logs everything to Airtable — built as a practical Python learning project for an Analytics Engineering career pivot.

> Built by a Business Analyst learning to think like an Analytics Engineer. The pipeline is live and runs daily. This repo is both a working tool and a portfolio artifact.

---

## What it does

```
Reddit (5 subreddits, daily) + Hacker News "Who is hiring?" (monthly)
        ↓
  Filter + Deduplicate        ← config-driven, state-tracked per source
        ↓
  Score with Claude API       ← structured prompt, JSON output
        ↓
  Draft Proposal              ← template library + Claude customization
        ↓
  Discord Digest (5pm daily)  ← BID / MAYBE / SKIP ranked output
        ↓
  Log to Airtable             ← BID + MAYBE posts auto-tracked
```

Each run: fetches new posts → filters by keyword and recency → deduplicates against state → scores each match → generates a tailored proposal → delivers a ranked digest → logs actionable gigs for tracking.

---

## Skills demonstrated

This project was built deliberately to practice Analytics Engineering-adjacent skills:

| Skill | Where it shows up |
|---|---|
| Python data pipeline design | `main.py` orchestrates modular stages end-to-end |
| API integration | Reddit JSON, HN Algolia search API, Anthropic (Claude), Airtable, Discord webhook |
| Config-driven architecture | `config.yaml` separates settings from logic (like dbt profiles) |
| Incremental state management | `seen_posts.json` prevents reprocessing (like dbt incremental models) |
| Data modeling | Airtable schema designed and provisioned via API (`setup_airtable.py`) |
| Prompt engineering | Structured scoring prompt returns consistent JSON for downstream parsing |
| Infrastructure as code | `setup_airtable.py` creates the table schema programmatically — repeatable, version-controlled |
| Scheduling | Windows Task Scheduler (local runner; Reddit blocks datacenter IPs) |

---

## Stack

| Component | Tool | Why |
|---|---|---|
| Language | Python 3.13 | AE-standard, good API ecosystem |
| Gig sources | Reddit JSON API (5 subreddits, daily) + HN Algolia API (monthly) | No auth required on either; HN runs once per month via state file |
| AI scoring + proposals | Claude API (Sonnet) | Structured output, ~$5/mo at current volume |
| Tracking | Airtable | Visual CRM, free tier, schema provisioned via API |
| Notifications | Discord webhook | Zero-friction, no SMTP config required |
| Scheduling | Windows Task Scheduler | Local residential IP bypasses Reddit's datacenter blocks |

---

## Project structure

```
src/
  main.py              # Pipeline orchestrator — runs all stages in order
  reddit_scraper.py    # Fetch, filter, and deduplicate Reddit posts
  hn_scraper.py        # HN "Who is hiring?" thread discovery, Algolia keyword search, monthly state
  scorer.py            # Claude API scoring — returns BID / MAYBE / SKIP + rationale
  proposer.py          # Claude API proposal generation from template library
  notifier.py          # Discord digest formatting and delivery
  airtable_logger.py   # Log BID/MAYBE gigs to Airtable automatically
  setup_airtable.py    # One-time: create Gigs table schema via Airtable API

config/
  config.yaml          # Subreddits, keywords, filter settings, HN config, pre-screen rules
  scoring_prompt.txt   # Claude scoring instructions (edit to tune without code changes)
  templates/           # Proposal templates: web-scraping, python-script, api-integration, data-cleanup, analysis, general-short

data/
  seen_posts.json      # Reddit state — processed post IDs (gitignored, generated at runtime)
  hn_state.json        # HN state — last processed thread ID, enforces monthly-only runs (gitignored)

docs/
  PROJECT_NORTH_STAR.md  # Full project spec, architecture decisions, session state
  TIL.md                 # Learning log — what was built and understood each session
```

---

## Setup

**Prerequisites:** Python 3.13, Anthropic API key, Discord webhook URL, Airtable API key

```bash
git clone https://github.com/your-username/gigflow
cd gigflow
python -m venv venv
source venv/Scripts/activate  # Windows

pip install -r requirements.txt

cp .env.example .env
# Fill in: ANTHROPIC_API_KEY, DISCORD_WEBHOOK_URL, AIRTABLE_API_KEY, AIRTABLE_BASE_ID
```

**First run — provision Airtable:**
```bash
python src/setup_airtable.py   # creates the Gigs table schema
```

**Run the pipeline:**
```bash
python src/main.py
```

**Schedule it:** Point Windows Task Scheduler at `run_pipeline.bat` to run daily at your preferred time.

---

## Scoring output

Each gig is evaluated on:
- **Clarity** (1–10): Is the deliverable well-defined?
- **AI deliverability** (1–10): Can Claude handle 80%+ of the work?
- **QA feasibility** (1–10): Can the output be verified by running the code and spot-checking results?
- **Estimated hours**: QA, communication, and delivery time only
- **Red flags**: Vague scope, no budget, "build me an app", requires server access
- **Recommendation**: `BID` / `MAYBE` / `SKIP`

BID and MAYBE posts get a draft proposal appended to the Discord notification and are automatically logged to Airtable.

---

## Why this exists

I'm a Business Analyst on a Data Governance team, teaching myself Python with the goal of moving into Analytics Engineering. This pipeline is Bucket 1 (generate enough freelance income to fund AI subscriptions) and Bucket 2 (build real, demonstrable engineering skills) at the same time.

Everything in this repo is production code running on my machine daily — not a tutorial exercise.

See `docs/PROJECT_NORTH_STAR.md` for full architecture, decision log, and build phases.
