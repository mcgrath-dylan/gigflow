# TIL — Today I Learned

Running log of what was built and understood each session.

---

## 2026-03-23 — Session 11

**What I built:** Stopped drafting proposals for MAYBE posts (BID-only now) to save tokens. Built a Gmail draft feature for auto-creating email drafts when BID posts have contact emails — but put it on ice since I can't access the project email right now. Also ran a full repo audit and cleaned up stale docs, dead dependencies, and config mismatches.

**What I learned:** The try/except import pattern for optional features ("feature flag via dependency") — the pipeline works fine whether or not Gmail packages are installed. Same idea as optional providers in Airflow. Also: repo audits are basically data governance for code — checking that docs match reality and cleaning up what drifted.

**What confused me:** Nothing blocked. Straightforward session.

---

## 2026-03-22 — Session 10

**What I built:** Added Freelancer.com as a new source (public API, no auth) and Google Alerts via RSS feeds. Also added SKIP visibility to Discord so I can actually see why posts get rejected instead of just "none actionable today." First test run scored 26 posts and produced 5 MAYBEs — more actionable results in one run than the previous 10 days combined.

**What I learned:** Adding a new data source to an existing pipeline is straightforward when the pipeline is designed around a common intermediate format. Both new scrapers output the same dict shape as Reddit and HN, so scoring, proposals, and notifications just work. Same idea as adding a new `source()` in dbt that feeds into an existing staging model.

**What confused me:** Nothing blocked. The `load_dotenv` override thing was mildly annoying — an empty system env var was shadowing the `.env` value — but the fix was one line.

---

## 2026-03-20 — Session 9

**What I built:** Nothing new. Reviewed 7 days of pipeline output (no actionable leads), widened keywords in config, added r/learnpython as a source, and added the AI case study to the backlog.

**What I learned:** Nothing that wasn't already known. This was a maintenance session — diagnosing low volume and adjusting config. The config-driven architecture made the change trivial, which is the point.

**What confused me:** Nothing. Worth noting: not every session produces a learning. This one produced a data point — the pipeline works, the market is thin, and systematic iteration (keywords → scoring → sources) is the right response.

---

## 2026-03-12 — Session 8

**What I built:** Diagnosed a market mismatch — the original gig types targeted non-technical buyers on gated platforms. Retuned the pipeline to target technical gigs (web scraping, Python scripts, API integrations) that are actually posted on Reddit/HN. Changed keywords, rewrote the scoring prompt, added a QA feasibility criterion, and created three new proposal templates.

**What I learned:** Config-driven architecture means pivoting your entire target market is a config change, not a rewrite. The same principle applies in dbt — separating profiles from model logic means you can change environments without touching code.

**What confused me:** Nothing technically — this was a strategic session. The hard part was being honest about what couldn't be automated (Facebook groups, LinkedIn) rather than trying to engineer around a market structure problem.

---

## 2026-03-12 — Session 7

**What I built:** [For Hire] post template (`docs/for_hire_template.md`) and confirmed the portfolio page was live on GitHub Pages.

**What I learned:** The inbound/outbound distinction. Passive monitoring has a structural ceiling when your target buyers are on gated platforms — no amount of scraper tuning fixes a market access problem. Outbound flips the model: instead of waiting for gigs to appear, you show up where clients look.

**What confused me:** Nothing blocked, but the realization that Reddit/HN might not surface enough volume even with better keywords was a legitimate surprise. That led directly to the Session 8 strategic pivot.

---

## 2026-03-12 — Session 6

**What I built:** `index.html` portfolio page, deployed via GitHub Pages.

**What I learned:** Reddit outbound ([For Hire] posts) is also likely to be low-ROI for non-technical gig types. And that GitHub Pages deploys automatically from an `index.html` in the root of the main branch — no build step, no config.

**What confused me:** Nothing blocked.

---

## 2026-03-12 — Session 5

**What I built:** HN scraper, expanded Reddit monitoring to 5 subreddits, evaluated and eliminated Craigslist, RemoteOK, Contra, and Discord as potential sources.

**What I learned:** Passive scrapers are unlikely to surface real opportunities when the market lives on platforms that require auth. Every dead-end source had a legitimate technical reason — 403s, wrong market fit, or TOS barriers. Evaluating and eliminating options is itself useful engineering work.

**What confused me:** How difficult it is to find high-quality, automatable sources for work that's allegedly in demand.

---

## 2026-03-11 — Session 4

**What I built:** Airtable tracking base with full schema, auto-logging wired into the pipeline via `airtable_logger.py`.

**What I learned:** How to create a table schema through the Airtable API and POST records to it programmatically. `setup_airtable.py` provisions the schema once — same concept as running `dbt run` to materialize models from code.

**What confused me:** The Airtable base ID issue — tried creating a new base via API, which isn't supported on free tier. Solution: build the table on an existing base instead.

---

## 2026-03-11 — Session 3

**What I built:** Proposal generation flow, two-tier filtering design (cheap pre-screen before Claude API), and a proposal template library.

**What I learned:** Use Claude Haiku for cheap, repetitive template fill-in and Sonnet for judgment-heavy scoring. The cost difference justifies routing by task type — same logic as using different compute tiers for different dbt model complexities.

**What confused me:** Whether generating proposals for MAYBE posts was worth the token cost. Conclusion at the time: yes. *Update (Session 11): Reversed this — after real data showed MAYBEs were never acted on, switched to BID-only proposal drafting.*

---

## 2026-03-11 — Session 2

**What I built:** Reddit scraper, keyword filtering, deduplication, Claude scoring, Discord notifications, Task Scheduler automation, and the README. Micro-tasks 1.2 through 1.11.

**What I learned:** Discord webhooks are trivially easy to set up — a single POST request with JSON, no auth beyond the URL itself. Same pattern as any other webhook integration.

**What confused me:** Reddit blocking GitHub Actions IPs (403 on all datacenter requests). Pivoted to Windows Task Scheduler running locally on a residential IP — the constraint forced a simpler, more reliable solution.

---

## 2026-03-11 — Session 1

**What I built:** Python virtual environment and repo scaffolding.

**What I learned:** How to use Claude Code within VSCode, and that virtual environments isolate project dependencies — the equivalent of separate dbt environments for dev vs. prod.

**What confused me:** `python` not being found in PATH — `py --version` worked instead. Windows installs Python through the `py` launcher by default.
