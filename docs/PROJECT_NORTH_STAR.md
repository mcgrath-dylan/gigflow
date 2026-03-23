# Project North Star: AI-Assisted Freelance Pipeline

## Last Updated: March 23, 2026

---

## ⚡ SESSION STATE — READ THIS FIRST

> **Claude: When Dylan says "pick up where we left off," read this block and resume accordingly.**

**Current Phase:** 4 — Outbound + First Revenue
**Current Micro-Task:** 4.3 — First real proposal submitted
**Session Count:** 11
**Progression Level:** Supervised
**Last Session Date:** 2026-03-23
**Last Session Summary:** Token efficiency optimization — stopped drafting proposals for MAYBE posts (BID-only now), saving ~5 Haiku API calls per run. MAYBE posts now display as compact one-liners in Discord (like SKIPs) instead of full blocks with proposals. Built Gmail draft feature (email extraction, Gmail API drafter, OAuth setup script) for auto-creating Gmail drafts when BID posts contain contact emails — but put on ice pending email account access (no 2FA, forgot password). All code is in place with graceful degradation (GMAIL_AVAILABLE flag).
**Blockers / Open Issues:** Gmail draft feature on hold — Dylan needs to reset project email password and set up 2FA before running OAuth setup. Google Alerts feeds should be producing results by now (created 2026-03-22).
**Next Action:** 4.3 — Review tonight's Discord digest (5pm run). Token cost should be noticeably lower with MAYBE proposals eliminated. When a BID surfaces, submit first real proposal.

### How to resume

1. Greet Dylan briefly. State the current micro-task and what it involves.
2. If there were blockers from last session, address those first.
3. Follow the Learning Protocol (Section 6) at the current Progression Level.
4. At session end, run the Handoff Protocol (Section 6) and tell Dylan what to update in this block.

---

## 1. Project Identity

**Codename:** GigFlow
**Owner:** Dylan
**AI Partner:** Claude (Anthropic)
**Status:** Phases 1–3 complete — Phase 4 starting

### What This Is

An automated pipeline that finds freelance gigs, scores them for fit, drafts proposals, and streamlines delivery — with AI handling ~80% of production work and Dylan providing ~20% (judgment, QA, client communication).

### What This Is NOT

- A startup or product to sell
- A full-time freelancing career
- A replacement for Dylan's day job or AE career pivot goals

---

## 2. Strategic Context

### Two-Bucket Framework

This project exists within a broader personal strategy:

| | Bucket 1: Fund the Tools | Bucket 2: Build Toward AE |
|---|---|---|
| **Goal** | Self-sustaining AI subscription income | Portfolio, skills, visibility for Analytics Engineering growth |
| **Timeline** | Immediate | 6-18 months |
| **Overlap** | Building this pipeline IS an AE-relevant portfolio piece (data pipelines, APIs, Python, automation) |

**Critical rule:** Bucket 1 decisions should never compromise Bucket 2 goals. If a shortcut makes money but teaches nothing, skip it.

### Constraints

- **Time budget:** 2-3 hours/week until proven, then scale up
- **Financial budget:** Minimal. Claude API costs, free-tier tooling preferred
- **Dylan's current role:** Business Analyst, Data Governance team
- **Core skills to leverage:** Data standards/policy documentation, light analysis/reporting, stakeholder translation (technical ↔ business), spreadsheet/data cleanup
- **No existing freelance network** — cold-start problem is real and acknowledged

---

## 3. Architecture Overview

```
[Sources] → [Scraper/Monitor] → [Scoring Engine] → [Daily Digest] → [Dylan Reviews]
                                                                          ↓
                                                              [Proposal Drafting] → [Dylan QA + Submit]
                                                                                          ↓
                                                                                 [Deliverable Production]
                                                                                    (Claude does work)
                                                                                          ↓
                                                                                 [Dylan QA + Deliver]
                                                                                          ↓
                                                                                 [Tracking / Feedback Loop]
```

### Layer Breakdown

#### Layer 1: Gig Radar (Monitoring)
**Purpose:** Automatically discover relevant gig postings from multiple sources.

**Sources (active):**
1. Reddit (r/forhire, r/slavelabour, r/freelance_forhire, r/WorkOnline, r/HireaWriter, r/learnpython) — public JSON endpoint, no auth required; daily cadence
2. Hacker News "Who is hiring?" — monthly thread, Algolia search API, no auth required; runs once per month via state file
3. Freelancer.com — public REST API, no auth required; daily cadence; filters by job category (Python, Web Scraping, Data Processing, Data Entry) and fixed-price projects with min $20 USD budget
4. Google Alerts — RSS feeds from custom alert queries; daily cadence; wide-net discovery across forums, job boards, and niche sites indexed by Google
5. LinkedIn job alerts — passive input, no automation

**Sources evaluated and eliminated:** Contra (design/product skew), Discord (auth required), Craigslist (RSS 403 from all endpoints), RemoteOK (90% full-time engineering roles), Jobicy (zero freelance/contract dev jobs in API).

**Structural note (updated 2026-03-12):** Original gig types (data cleanup, SOPs, spreadsheets) hit a ceiling — posted by non-technical people on gated platforms. Pipeline retuned to target technical gig types (web scraping, Python scripts, API integrations) which ARE posted in high volume on Reddit/HN. Hard constraint: manual platform browsing is a failure condition — all discovery must be automated.

**Output:** Raw list of candidate gigs with metadata (source, title, description, budget if stated, post date, poster history).

**Tech:** Python script, scheduled via Windows Task Scheduler (local). Cloud scheduling deferred — Reddit blocks datacenter IPs.

#### Layer 2: Gig Scoring (Filtering)
**Purpose:** Use Claude API to evaluate each gig against Dylan's profile and constraints.

**Scoring prompt should evaluate:**
- Clarity of scope (1-10): Is the deliverable well-defined?
- AI-deliverability (1-10): Can Claude do 80%+ of this?
- Estimated time for Dylan (hours): Including QA and client comms
- Budget-to-effort ratio: Is this worth the time?
- Red flags: Vague scope, "test project" language, no budget mentioned, brand-new poster with no history
- Recommendation: BID / MAYBE / SKIP

**Output:** Scored and ranked shortlist pushed to Dylan via Discord.

**Critical design decision:** Over-filter aggressively early. Better to surface 2 strong matches than 10 mediocre ones. Dylan's time is the bottleneck.

#### Layer 3: Proposal Drafting
**Purpose:** Generate ready-to-send (or near-ready) proposals tailored to each gig.

**Template library (7 templates, matched to gig_type from scoring):**
- `web-scraping`: Extract data from sites, deliver as CSV/JSON
- `python-script`: Build automation scripts, data processing
- `api-integration`: Connect services, pull/push data
- `data-cleanup`: Restructure and standardize messy datasets
- `analysis`: Analyze data and deliver report with insights
- `doc-writing`: Turn notes/requirements into polished documents
- `general-short`: Catch-all for small tasks

**Each proposal must:**
- Reference specific details from the gig posting (no generic spam)
- Be concise (under 150 words for Reddit/Discord, longer for platforms)
- Include a realistic timeline
- State a clear price or ask for budget

**Output:** Draft proposal for Dylan to review/edit/send. Target: <5 min review time.

#### Layer 4: Deliverable Production
**Purpose:** Claude produces the actual work product.

**This is the existing workflow — no special tooling needed.** Dylan takes client input, passes to Claude with context, QAs the output, delivers.

**Quality gates:**
- Dylan reviews every deliverable before delivery (non-negotiable)
- For data work: spot-check formulas, row counts, edge cases
- For documents: read fully, check tone/formatting, verify requirements met
- For analysis: validate conclusions against the data

#### Layer 5: Tracking & Feedback Loop
**Purpose:** Track what's working, what's not, and feed learnings back into the system.

**Track in Airtable:**
- Gig source, type, budget, status (applied / won / lost / completed)
- Time spent (Dylan's hours only)
- Revenue
- Scoring accuracy (did the score predict win/quality?)
- Client satisfaction / repeat potential

**Monthly review:** Calculate effective hourly rate, identify best-performing gig types and sources, refine scoring prompts accordingly.

---

## 4. Tech Stack

| Component | Tool | Cost | Why |
|---|---|---|---|
| Scripting | Python 3.13 | Free | AE-relevant, good API support |
| Reddit data | `requests` + public JSON API | Free | Reddit locked down script app registration; public endpoint requires no auth |
| HN data | Algolia search API + HN Firebase API | Free | No auth required; monthly cadence; searches within HN thread by keyword |
| Freelancer.com data | `requests` + public REST API | Free | No auth required; daily cadence; filters by job category and project type |
| Google Alerts data | `feedparser` + RSS feeds | Free | Wide-net discovery; Google indexes forums, job boards, niche sites |
| AI Engine | Claude API (Sonnet for scoring, Haiku for BID proposals only) | ~$5/mo | Already in ecosystem |
| Scheduling | Windows Task Scheduler (local) | Free | Reddit blocks GitHub Actions/datacenter IPs; local runner on residential IP works fine |
| CRM/Tracker | Airtable | Free tier | Visual, no-code, fast to set up; auto-logged via airtable_logger.py |
| Notifications | Discord webhook | Free | Zero-friction setup; Gmail app passwords require 2FA |
| Version Control | GitHub (private repo) | Free | Portfolio-ready, good practice |

**Explicitly not using:** Upwork (connect costs, bot competition), Fiverr (20% fee), praw (Reddit locked down API registration), GitHub Actions for scheduling (Reddit 403 block), Craigslist (RSS 403 from all IPs), RemoteOK (wrong market — full-time eng roles), Jobicy (zero freelance/contract dev jobs).

---

## 5. Tooling Context: Claude Code vs Cowork

| Activity | Tool | Why |
|---|---|---|
| Building the pipeline (Python, APIs, git) | Claude Code | Terminal-native, full dev environment, teaches AE-relevant skills |
| Iterating on scoring/proposal prompts | Claude Code or Chat | Conversational prompt engineering |
| Producing client deliverables (file-in → file-out) | Cowork | Non-technical, folder-based, fast for repetitive production tasks |
| Ad hoc analysis or tracking | Either | Depends on complexity |

**Build phase (Phases 1–3):** Complete. Claude Code remains available for Phase 4 portfolio work and pipeline maintenance.

**Operational phase (Phase 4+):** Cowork takes over deliverable production. Claude Code stays for new features and the portfolio page build.

**Key principle:** Claude Code is where the learning happens. Cowork is where the earning happens.

---

## 6. Learning Protocol

This section exists to prevent the most likely failure mode: Claude Code builds everything, Dylan learns nothing, and Bucket 2 gets zero value.

### Rules for Claude Code Sessions

> **LEARNING MODE — ACTIVE**
>
> Dylan prefers fast-forward mode: Claude builds, explains key concepts at a high level, Dylan does not need to execute every individual step unless it's genuinely non-trivial. Teaching happens through explanation and AE parallels, not hand-holding.
>
> 1. **Explain before writing.** Before producing any code, explain in plain English what you're about to build and why.
>
> 2. **Name the transferable concept.** After each micro-task, explicitly state what AE-relevant skill was just practiced.
>
> 3. **Never auto-fix silently.** If Dylan's code has an error, show the error message first and ask what he thinks it means before fixing it.
>
> 4. **Vocabulary building.** When introducing a new term, define it once in plain language and use it naturally going forward.

### TIL (Today I Learned) Log

After every Claude Code session, Dylan writes 2-3 sentences in a running log. Format:

```
## 2026-03-XX — Session N
**What I built:** [one sentence]
**What I learned:** [one concept or skill]
**What confused me:** [one thing, or "nothing" if clear]
```

This log lives in the repo at `/docs/TIL.md`.

### Progression Model

Tied to phases, not calendar weeks. Dylan moves fast — don't artificially slow down.

**Phase 1 (complete) — Collaborative:** Claude builds, explains at a high level. Dylan follows along, asks questions, understands what was built even if he didn't type it.

**Phase 2 — Supervised:** Dylan drives more decisions. Claude handles unfamiliar syntax and complex integrations. Dylan should be able to read any file in the repo and explain it.

**Phase 3+ — Independent with support:** Dylan can make small changes solo. Claude handles new features and debugging. Dylan can explain the full architecture to someone else.

### Session Handoff Protocol

**Run this at the end of every Claude Code session.**

1. **State what was completed.**
2. **State what's next** — next micro-task, one-sentence preview.
3. **Log any blockers.**
4. **Prompt the TIL entry.**
5. **Generate the Session State update** — ready-to-paste replacement for the `⚡ SESSION STATE` block.

**Dylan's job after each session:**
1. Write the TIL entry in `/docs/TIL.md`
2. Copy the generated Session State block into the top of this document
3. Save the file

---

## 7. Build Phases

### Phase 1: Reddit Scraper + Scoring Pipeline ✅ COMPLETE

**Goal:** Automatically surface scored gig recommendations from Reddit.

**Deliverables:**
- [x] Python script that polls target subreddits for new posts matching keywords
- [x] Keyword/filter config (editable without code changes)
- [x] Claude API integration for scoring each post
- [x] Output: scored digest sent via Discord webhook
- [x] Scheduled via Windows Task Scheduler (5pm daily)

**Success criteria:** Pipeline runs reliably. At least 1 gig surfaces that Dylan would actually bid on. ✅

#### Phase 1 Micro-Tasks

- [x] **1.1** — Project setup and environment
- [x] **1.2** — Reddit data access *(Note: Reddit locked down script app registration. Used public JSON endpoint `reddit.com/r/sub/new.json` via `requests` — no auth required. praw not used.)*
- [x] **1.3** — Fetch posts from one subreddit
- [x] **1.4** — Parse and filter posts
- [x] **1.5** — Multi-subreddit support + config file *(Note: r/dataengineering and r/analytics removed — discussion communities, not job boards; [Hiring] tag filter screens out almost everything)*
- [x] **1.6** — Deduplication and state
- [x] **1.7** — Claude API integration for scoring
- [x] **1.8** — Scoring prompt development
- [x] **1.9** — Output formatting + Discord notification *(Note: Email dropped due to Gmail 2FA friction. Discord webhook used instead.)*
- [x] **1.10** — Scheduling *(Note: GitHub Actions blocked by Reddit 403 on datacenter IPs. Replaced with Windows Task Scheduler at 5pm daily.)*
- [x] **1.11** — README and documentation

---

### Phase 2: Proposal System + Airtable ✅ COMPLETE

**Goal:** End-to-end flow from scored gig → draft proposal → tracking.

**Deliverables:**
- [x] Proposal template library (7 templates)
- [x] Claude API integration for proposal customization
- [x] Airtable base with gig tracking schema
- [x] Discord notification includes draft proposal for BID gigs (MAYBE shows as compact one-liners)
- [x] Simple "log this gig" workflow (airtable_logger.py auto-logs BID+MAYBE posts)

**Success criteria:** Pipeline built and functional — per-gig time target achievable. First proposal submission is now the Phase 4 operational target.

---

### Phase 3: Expand Sources + Refine ✅ COMPLETE

**Goal:** Add non-Reddit sources and tune the system based on real data.

**Deliverables:**
- [x] At least 1 additional source integrated — HN "Who is hiring?" added (monthly, Algolia); Reddit expanded to 5 subreddits
- [x] Scoring keywords tightened — false positives ("report", "analysis") replaced with compound terms; "sop", "data quality", "process documentation" added
- [x] Template library expanded to 7 templates covering technical gig types (web-scraping, python-script, api-integration, data-cleanup, analysis, doc-writing, general-short)
- [ ] First monthly review — deferred: pipeline needs a full month of live runs first

**Success criteria:** Two sources operational. Keywords tightened — measurably fewer false positives. Structural ceiling identified: inbound alone won't meet Bucket 1 target. Phase 4 outbound warranted.

---

### Phase 4: Outbound + First Revenue

**Goal:** Complement inbound monitoring with proactive outreach. Generate the first actual client engagement and first dollar of revenue.

**Context:** Phase 3 confirmed that inbound monitoring alone hits a structural ceiling. Session 8 pivot: target gig types shifted from non-technical (data cleanup, SOPs, spreadsheets) to technical (web scraping, Python scripts, API integrations). Non-technical gigs are posted on gated platforms that can't be automated; technical gigs are posted on Reddit/HN in high volume and can be fully delivered by Claude with Dylan QAing by running the code.

**Deliverables:**
- [x] GitHub Pages portfolio page — "Data & Automation Specialist" 1-pager live on GitHub Pages *(Session 6)*
- [x] [For Hire] post template for relevant subreddits — `docs/for_hire_template.md` *(Session 7)*
- [ ] First proposal submitted and logged in Airtable
- [ ] First monthly pipeline review: source performance, scoring accuracy, time spent

**Success criteria:** At least 1 proposal submitted. At least 1 reply or inquiry from any outbound channel.

**Possible later additions (evaluate after first month of outbound):**
- Auto-response templates for common client follow-up questions
- Client relationship tracking (repeat clients flagged in Airtable)
- Rate optimization based on win/loss data
- Cloud scheduling revisit if a Reddit-unblocked data source is added

---

## 8. Gig Type Fit Matrix

### Good Fits (high AI-leverage, clear scope, Dylan can QA by running code)
- Web scraping — extract data from specific sites, deliver as CSV/JSON
- Python scripts — automate file processing, data transformation, scheduled tasks
- API integrations — connect services, pull/push data between platforms
- Data cleanup — restructure, de-dupe, standardize messy datasets
- Data analysis with written summary
- ETL / data pipeline scripts

### Acceptable Fits (moderate AI-leverage, some judgment needed)
- Technical writing / documentation
- Report generation from raw data
- Bot development (Discord, Telegram, etc.)
- CSV/JSON parsing and transformation

### Bad Fits (avoid — time sinks or unverifiable)
- Full application development ("build me an app")
- Anything requiring live calls or meetings
- Ongoing maintenance contracts (scope creep)
- Anything requiring access to client servers/credentials
- Ambiguously scoped projects with no clear deliverable
- Creative/subjective work (marketing copy, branding)
- Work requiring proprietary tools Dylan doesn't have

---

## 9. Decision Log

| Date | Decision | Rationale |
|---|---|---|
| 2026-03-10 | Skip Upwork | Bot competition, connect costs, race-to-the-bottom in our gig types. |
| 2026-03-10 | Start with Reddit as primary source | Free, low friction, direct client contact, no platform fees |
| 2026-03-10 | Airtable over Notion for CRM | More structured, better for tracking metrics, free tier sufficient |
| 2026-03-10 | 2-3 hrs/week hard cap until proven | Protect against sunk cost. Scale only with evidence of ROI. |
| 2026-03-11 | Claude Code for building, Cowork for operating | Claude Code teaches AE-relevant skills. Cowork handles deliverable production once pipeline is live. |
| 2026-03-11 | Session State + Handoff Protocol | Enables "pick up where we left off" across sessions. |
| 2026-03-11 | Use requests + public Reddit JSON instead of praw | Reddit locked down script app registration; public JSON endpoint works without auth and is simpler |
| 2026-03-11 | Discord webhook for notifications instead of email | Gmail app passwords require 2FA Dylan didn't want to set up; Discord webhook is zero-friction |
| 2026-03-11 | Windows Task Scheduler instead of GitHub Actions | Reddit blocks requests from datacenter IPs (403); local runner on residential IP works fine |
| 2026-03-11 | Run pipeline once daily at 5pm instead of 2x/day | Token efficiency; Dylan's schedule means 5pm is the only actionable time anyway |
| 2026-03-11 | Compress timeline from weeks to days | Dylan motivated to move fast; Phase 1 completed in one session with no quality loss |
| 2026-03-11 | Remove r/dataengineering and r/analytics from config | Discussion communities, not job boards; [Hiring] tag filter screens out nearly everything there |
| 2026-03-12 | Add HN as second source (monthly, "Who is hiring?" thread) | Free, no auth, Algolia search API. Require_terms filter keeps only contract/freelance posts to avoid full-time job noise. |
| 2026-03-12 | Eliminate Craigslist | RSS returns 403 from all endpoints including residential IP. Dead end. |
| 2026-03-12 | Eliminate RemoteOK | Free API but 90% full-time engineering roles. Wrong market for Dylan's gig types. |
| 2026-03-12 | Expand Reddit to 5 subreddits | Added r/freelance_forhire, r/WorkOnline, r/HireaWriter. tag_exempt_subreddits config bypasses [Hiring] tag check for subs that don't use it. |
| 2026-03-12 | Tighten keywords — remove "report" and "analysis" | Too broad — catching journalism and research writing posts. Replaced with "data report", "data analysis". Added "sop", "standard operating procedure", "data quality", "process documentation". |
| 2026-03-12 | Acknowledge inbound ceiling; pivot to Phase 4 outbound | High AI-deliverability gigs are posted on non-developer platforms. Passive monitoring alone won't fund the tools — outbound needed. |
| 2026-03-12 | Retune pipeline from non-technical to technical gig types | Non-technical gigs (spreadsheets, SOPs) are posted on gated platforms (Facebook, LinkedIn) that can't be automated. Technical gigs (web scraping, Python scripts, API integration) ARE posted on Reddit/HN in high volume. Claude can deliver these; Dylan can QA by running code and checking output. Same pipeline, different keywords. |
| 2026-03-12 | Hard constraint: manual platform browsing is a failure condition | If the pipeline requires Dylan to manually browse Reddit/Facebook/LinkedIn to find leads, the project has failed. All discovery must be automated. Retuning keywords is the fix — not adding manual steps. |
| 2026-03-12 | Add QA feasibility as scoring criterion | New `qa_feasibility_score` in scoring prompt ensures Dylan only bids on gigs where he can verify the output by running code locally. Avoids landing gigs he can't QA. |
| 2026-03-20 | Widen keywords after 7 days of no actionable leads | 5 posts scored across 7 runs, all SKIP. Diagnosed as insufficient keyword coverage (pipeline working correctly). Added: selenium, pandas, google sheets, excel, sql, airtable, parse, parsing. |
| 2026-03-20 | Add r/learnpython as source | Mix of help requests and paid work postings; common source of "I need someone to build X" requests that fit Dylan's technical gig profile. |
| 2026-03-20 | Exempt r/freelance_forhire from [hiring] tag filter | That sub has more freeform post formats than r/forhire — the tag filter was blocking real gigs. Added to tag_exempt_subreddits alongside WorkOnline and HireaWriter. |
| 2026-03-22 | Add Freelancer.com as a source (public API, no auth) | Reddit/HN confirmed low-signal after 10+ days. Freelancer.com public API returns 25 active fixed-price projects per run with budgets, skill tags, and full descriptions — first run produced 5 MAYBE results. No auth needed. |
| 2026-03-22 | Reject Jobicy as a source | Tested API — zero freelance/contract dev jobs returned. Only full-time positions. Dead end. |
| 2026-03-22 | Add Google Alerts RSS as a source | Wide-net discovery via Google indexing. 4 alert feeds created. Zero auth, `feedparser` library, trivially parseable. Alerts take 24-48h to start producing results. |
| 2026-03-22 | Add SKIP visibility to Discord digest | SKIP posts were being suppressed — no way to see WHY posts were rejected. Added compact one-liners showing title, 3 scores, and reasoning for every SKIP. Critical for diagnosing scoring thresholds. |
| 2026-03-22 | Fix load_dotenv to use override=True from project root | Empty system env var for ANTHROPIC_API_KEY was shadowing the .env value. Fixed in main.py entry point. |
| 2026-03-23 | Stop drafting proposals for MAYBE posts (BID-only) | MAYBE proposals were never submitted — wasted Haiku API calls and Discord space. MAYBEs now show as compact one-liners. Saves ~5 API calls per run. |
| 2026-03-23 | Build Gmail draft feature for BID proposals (on ice) | Code complete: email extraction, Gmail API drafter, OAuth setup script. Graceful degradation via GMAIL_AVAILABLE flag. On hold — Dylan needs to reset project email password and set up 2FA for Google Cloud OAuth. |

---

## 10. Guiding Principles

1. **Dylan's time is the scarcest resource.** Every design decision should minimize Dylan's hours per dollar earned.

2. **Working > perfect.** Ship the ugly MVP. Refine based on real data, not hypothetical optimization.

3. **Over-filter, under-commit.** Better to bid on 1 great gig than 5 mediocre ones. Quality of match > quantity of proposals.

4. **Every piece builds the portfolio.** The pipeline itself, the scripts, the process — all of this is demonstrable AE-relevant work. Treat the repo accordingly.

5. **Fail fast, learn cheap.** If after Phase 3 there are zero wins, diagnose honestly and pivot or kill. Don't zombie. *Applied at end of Phase 3: inbound ceiling diagnosed, Phase 4 pivot to outbound chosen over killing the project.*

6. **Automate the boring, keep the judgment.** Claude handles production. Dylan handles decisions. Never let AI auto-submit anything without human review.

7. **Revenue is the metric that matters for Bucket 1.** Not proposal count, not pipeline volume, not tech sophistication. Dollars in minus costs out.

8. **If Dylan can't explain it, it doesn't count.** Code that works but isn't understood is technical debt and a missed learning opportunity.

---

## 11. How to Use This Document

### Starting a Claude Code session ("Pick up where we left off")

1. Open Claude Code
2. Say: **"Pick up where we left off"**
3. Claude reads the `⚡ SESSION STATE` block at the top and resumes at the current micro-task

### After every Claude Code session

1. Write TIL entry in `/docs/TIL.md`
2. Copy the generated Session State block into the top of this document
3. Check off completed micro-tasks in Section 7
4. Save the file

---

## 12. Backlog (Deprioritized — Revisit After First Revenue)

- [ ] **Automated client/job acquisition research agent** — Evaluate whether a dedicated research agent could automate discovery on non-developer platforms (Facebook groups, LinkedIn, etc.) where the actual buyers for Dylan's gig types post. Reddit/HN passive monitoring hits a structural ceiling. The hypothesis: an agent that proactively searches and surfaces opportunities on these channels could replace or supplement manual monitoring. Requires evaluating platform APIs, scrapeability, and whether automation is even feasible given bot detection. *Context: surfaced during Phase 4 strategic review; deprioritized in favor of manual outbound first.*

- [ ] **Google Alerts expansion** — Google Alerts proved easy to integrate (RSS feed, zero auth, parseable with `feedparser`). Explore additional alert queries beyond freelance gig discovery: industry trend monitoring, competitor tracking, keyword-based lead generation for specific niches. The infrastructure is source-agnostic — any well-crafted alert query feeds into the same scoring pipeline. *Context: surfaced during Session 10 source diversification. Low effort to experiment — just add new alert queries in the browser and paste RSS URLs into config.*

- [ ] **AI-Assisted Development Case Study** — Write a standalone markdown document (`docs/case_study.md`) documenting the GigFlow build process as a portfolio piece. Audience: hiring managers and technical interviewers evaluating ability to scope, build, and ship with AI-assisted tooling. Tone: honest and specific — no inflation. Should cover: (1) **Problem statement** — what GigFlow solves and why it was built, including the two-bucket framework and the AE career pivot context; (2) **AI-assisted workflow** — how Claude Code was used throughout: scoping and architecture decisions, implementation, debugging, iteration, and the pivot (technical gig types replacing non-technical ones); (3) **Technical decisions** — stack choices (Python, requests over praw, Windows Task Scheduler over GitHub Actions, Discord over email, etc.), tradeoffs made, and honest "what I'd do differently"; (4) **Output** — what the tool does end-to-end, with code snippets or a short demo walkthrough. *Not user-facing docs — career portfolio only. No revenue gate — the build story, architectural decisions, and operational data are the outcome. Can be written any time after the keyword-widening iteration in Phase 4.*

---

## 13. Open Questions (Resolve As You Go)

- [x] Reddit API: Which auth method? → Resolved: no auth, public JSON endpoint
- [x] Notifications: Slack or email? → Resolved: Discord webhook
- [x] Additional sources beyond Reddit? → Resolved: HN (monthly), Freelancer.com (daily API), Google Alerts (RSS). Evaluated and eliminated: Craigslist (403), RemoteOK (wrong market), Contra (design/product skew), Discord (auth required), Jobicy (zero freelance dev jobs).
- [ ] Scoring prompt: token cost at scale? Monitor after first 30 days of real runs.
- [ ] Pricing strategy: Undercut market to win first gigs, or price fair from day one?
- [ ] Legal: Do we need a simple freelance contract template? Payment terms?
- [ ] Tax implications: At what income level does this need formal tracking? (Consult accountant, not Claude.)
