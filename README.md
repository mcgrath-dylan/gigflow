# GigFlow

An automated freelance gig discovery and scoring pipeline. Monitors Reddit for relevant freelance postings, scores them using the Claude API, and delivers a daily digest to Discord.

## What it does

1. **Fetches** new posts from r/forhire, r/slavelabour, r/dataengineering, and r/analytics
2. **Filters** to hiring posts from the last 24 hours that match target keywords
3. **Deduplicates** against previously seen posts so nothing surfaces twice
4. **Scores** each match using Claude — clarity, AI-deliverability, estimated time, red flags
5. **Delivers** a ranked digest to a Discord channel at 5pm daily

## Setup

**Prerequisites:** Python 3.13, a Discord webhook URL, an Anthropic API key

```bash
# Clone and create virtual environment
git clone https://github.com/your-username/gigflow
cd gigflow
python -m venv venv
source venv/Scripts/activate  # Windows

# Install dependencies
pip install -r requirements.txt

# Configure credentials
cp .env.example .env
# Edit .env with your ANTHROPIC_API_KEY and DISCORD_WEBHOOK_URL
```

## Running

```bash
python src/main.py
```

To run on a schedule, use Windows Task Scheduler pointed at `run_pipeline.bat`.

## Project structure

```
src/
  main.py           # Pipeline orchestrator
  reddit_scraper.py # Fetch, filter, and deduplicate Reddit posts
  scorer.py         # Claude API scoring
  notifier.py       # Discord digest delivery
config/
  config.yaml       # Subreddits, keywords, filter settings
  scoring_prompt.txt # Claude scoring instructions
data/
  seen_posts.json   # State file — tracks processed post IDs
docs/
  PROJECT_NORTH_STAR.md  # Full project spec and session state
  TIL.md                 # Learning log
```

## Scoring criteria

Each gig is evaluated on:
- **Clarity** (1-10): Is the deliverable well-defined?
- **AI deliverability** (1-10): Can Claude handle 80%+ of the work?
- **Estimated Dylan hours**: QA, comms, and delivery time only
- **Red flags**: Vague scope, no budget, test projects, requires meetings
- **Recommendation**: BID / MAYBE / SKIP
